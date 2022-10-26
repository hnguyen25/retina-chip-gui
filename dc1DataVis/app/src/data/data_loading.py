"""
@authors Maddy Hays, Huy Nguyen, John Bailey (2022)
Functions for loading data files into form that can be read by GUI
"""''
import os
import scipy.io as sio

from .spike_detection import *
from ..data.filters import *

def load_first_buffer_info(app):
    data_run = os.path.basename(app.settings["path"])
    file_dir = app.settings["path"] +  "/" + data_run + "_" + str(0) + ".mat"
    first_file_params = {
        "file_dir": file_dir,
        "filter_type": app.settings["filter"],
        "packet_idx": 0,
        "SPIKING_THRESHOLD": app.settings["spikeThreshold"],
        "BIN_SIZE": app.settings["binSize"]
    }
    packet = load_one_mat_file(first_file_params)
    app.data.to_serialize.put(packet)
    app.curr_buf_idx = 1

    NUM_CHANNELS_PER_BUFFER = len(packet["packet_data"])

    return NUM_CHANNELS_PER_BUFFER


def load_one_mat_file(params):
    # this is designed to be multi-processed
    file_dir = params["file_dir"]
    filter_type = params["filter_type"]
    SPIKING_THRESHOLD = params["SPIKING_THRESHOLD"]
    BIN_SIZE = params["BIN_SIZE"]

    mat_contents = sio.loadmat(file_dir)
    dataRaw = mat_contents['gmem1'][0][:]
    data_real, cnt_real, N = removeMultipleCounts(dataRaw)

    # Note: this code does not timestamp data bc that cannot be parallelized properly
    packet_data = preprocess_raw_data(data_real, cnt_real, N)

    packet = {
        "packet_data": packet_data,
        "packet_idx": params["packet_idx"],
        "file_dir": params["file_dir"],
        "filter_type": params["filter_type"]
    }

    packet = filter_preprocessed_data(packet, filter_type=filter_type)
    packet = calculate_channel_stats(packet, SPIKING_THRESHOLD, BIN_SIZE)

    return packet

def calculate_channel_stats(packet, SPIKING_THRESHOLD, BIN_SIZE):
    for idx, channel_data in enumerate(packet["packet_data"]):
        channel_data["stats_avg+unfiltered+amp"] = np.mean(channel_data["preprocessed_data"])
        channel_data["stats_cnt"] = len(channel_data["filtered_data"])
        channel_data["stats_noise+mean"] = np.mean(channel_data["filtered_data"])
        channel_data["stats_noise+std"] = np.std(channel_data["filtered_data"])
        channel_data["stats_buf+recording+len"] = channel_data["stats_cnt"] * 0.05 # assuming 20 khZ sampling rate

        # TODO [later] add GMM spikes
        SPIKE_DETECTION_METHOD = "threshold"
        if SPIKE_DETECTION_METHOD == "threshold":
            incom_spike_idx, incom_spike_amplitude = getAboveThresholdActivity(channel_data["filtered_data"],
                                                                               channel_data["stats_noise+mean"],
                                                                               channel_data["stats_noise+std"],
                                                                               SPIKING_THRESHOLD)
            spikeBins, spikeBinsMaxAmp, NUM_BINS_IN_BUFFER = binSpikeTimes(channel_data["stats_buf+recording+len"],
                                                                           incom_spike_idx,
                                                                           incom_spike_idx,
                                                                           BIN_SIZE)

            channel_data["stats_spikes+cnt"] = sum(spikeBins)
            channel_data["stats_spikes+avg+amp"] = np.mean(spikeBinsMaxAmp)
            channel_data["stats_spikes+std"] = np.std(spikeBinsMaxAmp)
            channel_data["spike_bins"] = spikeBins
            channel_data["spike_bins_max_amps"] = spikeBinsMaxAmp
            channel_data["stats_num+spike+bins+in+buffer"] = NUM_BINS_IN_BUFFER

    return packet

def filter_preprocessed_data(packet, filter_type="Modified Hierlemann"):
    for idx, channel_data in enumerate(packet["packet_data"]):
        filtered_data = applyFilterToChannelData(channel_data['preprocessed_data'], filtType=filter_type)
        packet["packet_data"][idx]["filtered_data"] = filtered_data
    return packet

def preprocess_raw_data(data_real, cnt_real, N, SAMPLING_PERIOD=0.05):
    # Determine time estimate and sample counts for the total combined buffers
    # (note this does not take into account communication delays - hence an estimate)
    end_time = N * SAMPLING_PERIOD  # 20kHz sampling rate, means time_recording (ms) = num_sam * 0.05ms

    # we are not determining absolute time, because we want to parallelize this,
    # and time tracking must be done in sequence
    times = np.linspace(0, end_time, N + 1)

    # identify relevant, nonzero channels, and then append only this data into recorded_data
    num_channels, channel_map, channel_id, start_idx, find_coords, recorded_channels = identify_relevant_channels(data_real)

    packet_data = []
    for i in range(recorded_channels.shape[0]):

        # process each channel index
        channel_idx = int(recorded_channels[i][0])
        x, y = idx2map(channel_idx)
        start_idx = recorded_channels[i][0]

        channel_data = data_real[x, y, start_idx:N]
        # channel_times = self.times[self.count_track + start_idx: self.count_track+N] can't do
        # prune the times in the packet where nothing is recorded (aka when data == 0)
        # TODO turn on
        # actual_recording_times = (channel_data != 0]
        # channel_times = channel_times[actual_recording_times]
        # channel_data = channel_data[actual_recording_times]

        channel_data = {
            "data_real": data_real,
            "cnt_real": cnt_real,
            "N": N,
            "channel_idx": channel_idx,
            "preprocessed_data": channel_data
        }

        packet_data.append(channel_data)

    return packet_data

"""
========================================
DATA LOADING FUNCTIONS TO PULL MATLAB FILES FROM A COMPLETE RECORDING IN A FOLDER
=========================================
HOW TO USE
loadingDict = initDataLoading('/Volumes/Lab/Users/mads/dc1DataVis/debugData', '2022-02-18-1', 'data000', 'gmem1'):
dataAll, cntAll, times = processData(loadingDict, dataIdentifierString='gmem1', buffer_num=0)
"""
def init_data_loading(path : str):
    bufDir = os.listdir(path)
    num_of_buf = len(bufDir)
    bramdepth = 65536

    datarun = os.path.basename(path)
    datapiece = os.path.basename(os.path.dirname(path))

    # initialize variables
    dataAll = np.zeros((32, 32, int(bramdepth * num_of_buf / 2)))  # Largest possible value of dataAll, perfect recording, only double cnt
    cntAll = np.zeros((32, 32, int(bramdepth * num_of_buf / 2)))
    times = np.zeros((int(bramdepth * num_of_buf / 2)))

    loadingDict = {
        "path": path,
        "datarun": datarun,
        "datapiece": datapiece,
        "bufDir": bufDir,
        "num_of_buf": num_of_buf,
        "bramDepth": bramdepth,
        "dataAll": dataAll,
        "cntAll": cntAll,
        "times": times
    }
    return loadingDict

def removeMultipleCounts(dataRaw):
    # Initialize Variables Needed for Each Buffer
    chan_index_pre = 1025  # Check for chan changes, double cnt
    cnt_pre = 0  # Check for cnt changes, double cnt
    N = 0  # Sample times (DOES NOT ALLOW NON-COLLISION FREE SAMPLES)
    data_real = np.zeros(
        (32, 32, len(dataRaw) - 2))  # Initialize to max possible length. Note: Throw out first two values b/c garbo
    cnt_real = np.zeros((32, 32, len(dataRaw) - 2))

    # Convert data and remove double/triple counts
    for i in range(2, len(dataRaw) - 1):
        # Convert bit number into binary
        word = (np.binary_repr(dataRaw[i], 32))

        # Break that binary into it's respective pieces and convert to bit number
        cnt = int(word[12:14], 2)
        col = int(word[27:32], 2)
        row = int(word[22:27], 2)
        chan_index = row * 32 + col

        # Only record the unique non-double count sample
        if (i == 2 or (cnt_pre != cnt or chan_index != chan_index_pre)):

            # Sample time only changes when cnt changes
            if cnt != cnt_pre:
                N += 1
            # On the occurance the first cnt is not 0, make sure sample time is 0
            if i == 2:
                N = 0

            # Update variables
            cnt_pre = cnt
            chan_index_pre = chan_index

            # Record pertinent data
            data_real[row][col][N] = int(word[14:22], 2)
            cnt_real[row][col][N] = cnt

    return data_real, cnt_real, N

def identify_relevant_channels(raw_data: np.array):
    """ Only n number of channels can be recorded at a given time due to bandwidth concerns--the rest are shut off.
    For given data recorded at during a certain window, find which channels were recorded.

    Args:
        raw_data_all: unprocessed data in a given time window (num_channels_X x num_channels_Y x time_len)

    Returns:
        num_channels: number of channels that were found to have been recorded for given data
        channel_map: list of channels that were recorded, i.e. nonzero (x/y_coords, num_channels)
        channel_id: list of channels that were recorded, but identified by a single numerical ID
        start_idx:

    @param raw_data: all the raw data loaded thus far from files
    """
    # This bit takes the longest. ~ 30 sec for whole array 4 channel recording
    num_samples = np.count_nonzero(raw_data, axis=2)
    num_channels = np.count_nonzero(num_samples)

    # Map and Identify recorded channels
    find_coords = np.nonzero(num_samples)
    channel_map = np.array(find_coords)
    channel_id = np.zeros(num_channels)
    start_idx = np.zeros(num_channels)

    for k in range(0,num_channels):
        channel_id[k] = map2idx(channel_map[0,k],channel_map[1,k])
        start_idx[k] = (raw_data[channel_map[0, k], channel_map[1, k], :] != 0).argmax(axis=0)

    recorded_channels = np.stack((channel_id, start_idx), axis=1).astype(int)

    #return recorded_channels
    return num_channels, channel_map, channel_id, start_idx, find_coords, recorded_channels

def map2idx(ch_row: int, ch_col: int):
    """ Given a channel's row and col, return channel's index

    Args:
        ch_row: row index of channel in array (up to 32)
        ch_col: column index of channel in array (up to 32)

    Returns: numerical index of array
    """
    if ch_row > 31 or ch_row <0:
        print('Row out of range')
    elif ch_col >31 or ch_col<0:
        print('Col out of range')
    else:
        ch_idx = int(ch_row*32 + ch_col)
    return ch_idx

def idx2map(ch_idx: int):
    """ Given a channel index, return the channel's row and col

    Args:
        ch_idx: single numerical index for array (up to 1024)

    Returns:
        channel row and channel index
    """
    if ch_idx > 1023 or ch_idx < 0:
        print('Chan num out of range')
        return -1
    else:
        ch_row = int(ch_idx/32)
        ch_col = int(ch_idx - ch_row*32)
    return ch_row, ch_col



