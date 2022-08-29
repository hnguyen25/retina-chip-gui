import numpy as np
import time
from ..data.preprocessing import *
from ..data.filters import *
import warnings

class DC1DataContainer():
    """
    Container for holding recording data for the DC1 retina chip. Each container is designed to hold all
    the relevant information extracted from data collected from a SINGLE recording, of any particular type.

    This container holds three main data objects (in addition to calculated statistics based on this data):
    (1) raw data -> (2) recorded_data -> (3) filtered_data
    raw_data: the data as-is extracted directly from the .mat files
    recorded_data: the data within raw_data with minimal pre-processing necessary to fix hardware related
        issues (i.e. double counts), as well as managed into a more helpful format
    filtered_data: the data which has been filtered, can be rerun multiple times with different filter types

    To-Dos:
    ----------
    TODO figure out time alignment of the data / the actual sampling rate / check for dropped packets
    TODO fuse code in identify_relevant_channels with this file
    TODO figure out time budget for data processing + filtering
    TODO make filtering of data async -> specifically, only filter the data that is directly needed for the analysis gui
    TODO decompose update_array_stats() to make it more readable
    """

    # data processing settings
    data_processing_settings = {
        "filter": None, # for use in filtered_data, see full list in filters.py
        "spikeThreshold": 4,  # How many standard deviations above noise to find spikes
        "binSize": 1, # 1ms
        "simultaneousChannelsRecordedPerPacket": 4
    }

    # metadata information
    recording_info = {
        "recording_full_path": "",
        "recording_data": "",
        "recording_piece": "",
        "recording_type": "",
        "numChannelsRecordedPerPacket": None
    }

    recording_type_dict = {
        "full_bandwidth_1_channel": {"num_channels_at_once": 1,
                                     "compression": False},
        "full_bandwidth_2_channels": {"num_channels_at_once": 2,
                                      "compression": False},
        "full_bandwidth_4_channels": {"num_channels_at_once": 4,
                                      "compression": False},
        "full_bandwidth_8_channels": {"num_channels_at_once": 8,
                                      "compression": False},
        "full_bandwidth_16_channels": {"num_channels_at_once": 16,
                                       "compression": False},
        "full_bandwidth_32_channels": {"num_channels_at_once": 32,
                                       "compression": False}
    }

    # +++++ CONSTANTS +++++
    # DC1/RC1.5 is a multi-electrode array (MEA) with 32 x 32 channels (1024 total)
    ARRAY_NUM_ROWS, ARRAY_NUM_COLS = 32, 32

    # number of samples that numpy arrays containing preprocessed_data and filtered_data can hold
    # once the capacity has been reached, DATA_CONTAINER_MAX_SAMPLES will double, this variable
    # capacity is designed to limit the maximum memory taken up by these data containers
    DATA_CONTAINER_MAX_SAMPLES = 1000

    # (1) raw_data <> data loaded directly from .mat files
    # Split into three different related data containers:
    # - 'raw_data':
    # - 'counts':
    # - 'times':
    raw_data = None
    counts = None
    times = None
    count_track = None
    time_track = None

    # (2) preprocessed_data <> raw data which has been converted to a more easily accessible format
    #   A list of dictionaries, where each dictionary contains all necessary data related to
    #   the recording at ONE electrode at ONE point in time, ordered chronologically by
    #   recording time.
    #   Each dictionary has the following keys:
    #   - 'channel_idx': the channel from which the 'data' in this dictionary is recorded from
    #   - 'start_idx': TODO figure out what this is
    #   - 'data':
    #   - 'times':
    preprocessed_data = []
    count_track_processed = None
    time_track_processed = None

    # (3) filtered_data <> data container which holds all raw data that has been filtered
    #   A list of dictionaries, structured exactly as in preprocessed_data (see above), however,
    #   the 'data' is filtered with a filter specified by the user. Moreover, the data must
    #   be filtered based off of recorded_data, so the number of items in filtered_data may
    #   lag behind.
    filtered_data = []
    count_track_filtered = None
    time_track_filtered = None

    # calculated statistics
    spike_data = {
        'times': np.zeros((32, 32)),  # np.array with dims 32 x 32 x num_bins
        'amplitude': np.zeros((32, 32))
    }

    array_stats = {}

    def __init__(self, recording_info={}, data_processing_settings={}):
        self.time_track = 0
        self.count_track = 0
        self.count_track_processed = 0
        self.time_track_processed = 0

        self.raw_data = np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS,
                                  self.DATA_CONTAINER_MAX_SAMPLES))
        self.counts = np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS,
                                self.DATA_CONTAINER_MAX_SAMPLES))
        self.times = np.zeros((self.DATA_CONTAINER_MAX_SAMPLES,))

        self.array_stats = {
            "size": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS, 0)),  # For each dot, size by # of samples
            "num_sam": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS, 1)),  # Temp variable to allow sample counting
            "colors": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS, 0)),  # For each dot, color by avg amplitude
            "avg_val": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS, 1)),  # Temp variable for calculating average amplitude
            "noise_mean": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
            "noise_std": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
            "noise_cnt": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
            "spike_avg": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
            "spike_std": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
            "spike_cnt": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
            "size": None,
            "times": None,
            "array spike rate times": [],  # x
            "array spike rate": []  # y
        }

    def setSpikeThreshold(self, threshold):
        self.data_processing_settings["spikeThreshold"] = threshold

    def setNumChannels(self, numChannels):
        self.data_processing_settings["simultaneousChannelsRecordedPerPacket"] =  numChannels

    def extend_data_containers(self):
        """Change data containers dynamically to accommodate longer time windows of data
        by doubling the capacity of data containers when the max has been reached
        """
        padding_data = np.zeros(self.raw_data.shape)
        padding_cnt = np.zeros(self.counts.shape)
        padding_times = np.zeros(self.times.shape)
        self.raw_data = np.concatenate((self.raw_data, padding_data), axis=2)
        self.counts = np.concatenate((self.counts, padding_cnt), axis=2)
        self.times = np.concatenate((self.times, padding_times))
        self.DATA_CONTAINER_MAX_SAMPLES *= 2

    def append_raw_data(self, data_real, cnt_real, N, sampling_period=0.05, filtType = "Modified Hierlemann", debug = False):
        """
        appends raw data in buffer to end of data container, append nonzero data to recorded_data

        Args:
            data_real:
            cnt_real:
            N:
            sampling_period:

        Returns:

        """
        while self.raw_data.shape[2] < self.count_track + N:
            self.extend_data_containers()

        self.raw_data[:, :, self.count_track:self.count_track + N] = data_real[:, :, :N]
        self.counts[:, :, self.count_track:self.count_track + N] = cnt_real[:, :, :N]

        # Determine time estimate and sample counts for the total combined buffers
        # ===============================
        # (note this does not take into account communication delays - hence an estimate)
        end_time = N * sampling_period  # 20kHz sampling rate, means time_recording (ms) = num_sam * 0.05ms

        # For the first buffer, we assume the first sample comes in at time 0
        if self.time_track == 0:
            new_times = np.linspace(0, end_time, N + 1)
            self.times[0:len(new_times)] = new_times
        # For buffers after the first, we place these values directly after the previous buffer
        else:
            new_times = np.linspace(self.time_track, self.time_track + end_time, N)
            self.times[self.count_track:self.count_track + N] = new_times

        # identify relevant, nonzero channels, and then append only this data into recorded_data
        num_channels, channel_map, channel_id, start_idx, find_coords, recorded_channels = identify_relevant_channels(data_real)

        for i in range(recorded_channels.shape[0]):
            channel_idx = int(recorded_channels[i][0])
            start_idx = recorded_channels[i][0]
            x, y = idx2map(channel_idx)

            # prune the times in the packet where nothing is recorded aka when data = 0
            channel_data = data_real[x, y, start_idx:N]
            channel_times = self.times[self.count_track + start_idx: self.count_track+N]
            # actual_recording_times = (channel_data != 0)
            #
            # channel_times = channel_times[actual_recording_times]
            # channel_data = channel_data[actual_recording_times]

            channel_data = {
                'channel_idx': channel_idx,
                'start_idx': int(self.count_track + start_idx),  # start_idx is based only on buffer, so need to add time from previous buffers
                'data': channel_data,
                'times': channel_times
            }
            #  Add this data to preprocessed data
            self.preprocessed_data.append(channel_data)

            # Filter data, run spike detection
            self.update_filtered_data(filtType)
            self.filtered_data[-1] = self.calculate_realtime_spike_info_for_channel_in_buffer(self.filtered_data[-1])

            # add spike count to array stats
            self.array_stats["spike_cnt"][x][y] += sum(self.filtered_data[-1]["spikeBins"])

            if debug:
                print("spike cnt: " + str(self.array_stats["spike_cnt"]))
                print("sum of spike cnt: " + str(sum(self.array_stats["spike_cnt"])))

        self.time_track += end_time
        self.count_track += N

        # TODO this shouldn't call update_filtered_data -> should be async, and threaded

    def calculate_realtime_spike_info_for_channel_in_buffer(self, channel_data, filtered=True, debug = False):

        row, col = idx2map(channel_data['channel_idx'])

        if filtered is True:
            noise_mean = 0
            noise_std = np.std(channel_data['data'])
            if debug:
                print("filtered is true activated, std : " + str(noise_std))
        else:
            noise_mean = self.array_stats["noise_mean"][row, col]
            noise_std = self.array_stats["noise_std"][row, col]
            if debug:
                print("filtered is FALSE activated, std : " + str(noise_std) + "row: " + str(row) + " col: " + str(col))


        incom_spike_times, incom_spike_amplitude = self.getAboveThresholdActivity(channel_data['data'],
                                                                                  channel_data['times'],
                                                                                  noise_mean, noise_std,
                                                                                  self.data_processing_settings['spikeThreshold'],
                                                                                  filtered)
        channel_data["incom_spike_times"] = incom_spike_times
        channel_data["incom_spike_amp"] = incom_spike_amplitude

        spikeBins, spikeBinsMaxAmp, NUM_BINS_IN_BUFFER = self.binSpikeTimes(channel_data['times'], incom_spike_times, incom_spike_amplitude)
        channel_data["spikeBins"] = spikeBins
        channel_data["spikeBinsMaxAmp"] = spikeBinsMaxAmp
        channel_data["num_bins_in_buffer"] = NUM_BINS_IN_BUFFER

        if debug:
            print("channel idx: " + str(channel_data["channel_idx"]))
            print("noise mean: " + str(noise_mean))
            print("noise std: " + str(noise_std))
            print("threshold: " + str (self.data_processing_settings["spikeThreshold"]))
            print("num spikes for channel " + str(channel_data["channel_idx"]) + ": " + str(sum(channel_data['spikeBins'])))
            print("incoming spike times: " + str(incom_spike_times))
            print('spikeBins', channel_data['spikeBins'])
            print("channel data: " + str(channel_data))

        return channel_data

    def getAboveThresholdActivity(self, data, times, channel_noise_mean, channel_noise_std, spike_threshold, filtered=False):
        if filtered:
            below_threshold = 0 + spike_threshold * channel_noise_std # filtered data -> makes mean 0
        else:
            below_threshold = channel_noise_mean + (spike_threshold * channel_noise_std)

        above_threshold_activity = (data <= -below_threshold)
        incom_spike_idx = np.argwhere(above_threshold_activity).flatten()
        incom_spike_times = times[incom_spike_idx]
        incom_spike_amplitude = data[incom_spike_idx]

        return incom_spike_times, incom_spike_amplitude

    # TODO vectorize binning, this is not the most efficient way of doing this
    def binSpikeTimes(self, times, incom_spike_times, incom_spike_amps):
        start_time = times[0]
        end_time = times[-1]
        buf_recording_len = end_time - start_time
        binSize = self.data_processing_settings["binSize"]
        import math
        NUM_BINS_IN_BUFFER = math.floor(buf_recording_len / binSize)

        # initialize an array of spike bins, with no spikes detected
        spikeBins = np.zeros(NUM_BINS_IN_BUFFER, dtype=bool)
        spikeBinsMaxAmp = np.zeros(NUM_BINS_IN_BUFFER, dtype=float)

        for bin_idx in range(int(buf_recording_len / binSize)):
            bin_start = start_time + bin_idx * binSize
            bin_end = start_time + (bin_idx + 1) * binSize

            spikes_within_bin = (bin_start <= incom_spike_times) & (
                        incom_spike_times < bin_end)

            if np.count_nonzero(spikes_within_bin) != 0:
                spikeBins[bin_idx] = True
                spiking_amps = incom_spike_amps[spikes_within_bin]
                spikeBinsMaxAmp[bin_idx] = np.max(spiking_amps)

        return spikeBins, spikeBinsMaxAmp, NUM_BINS_IN_BUFFER

    def update_filtered_data(self, filtType='Modified Hierlemann', num_threads=4, debug = False ):
        # subtract recorded_data by filtered_data
        len_preprocessed_data = len(self.preprocessed_data)
        len_filtered_data = len(self.filtered_data)
        # TODO parallelize filtering
        if len_filtered_data < len_preprocessed_data:
            while len_filtered_data < len_preprocessed_data:
                to_filter_idx = len_filtered_data
                to_filter_data = self.preprocessed_data[to_filter_idx]['data']
                filtered_data = applyFilterToChannelData(to_filter_data, filtType=filtType)
                filtered_data = {
                    'channel_idx': self.preprocessed_data[to_filter_idx]['channel_idx'],
                    'start_idx': self.preprocessed_data[to_filter_idx]['start_idx'],
                    # start_idx is based only on buffer, so need to add time from previous buffers
                    'data': filtered_data,  # TODO make this accurate
                    'times': self.preprocessed_data[to_filter_idx]['times']
                }

                self.filtered_data.append(filtered_data)
                len_filtered_data += 1
            if debug and (len_filtered_data > 1):
                print("Filtered data: " + str(filtered_data))

    def update_array_stats(self, data_real, N, individualChannel = False, row =0, col = 0):
        """

        @param data_real:
        @param N:
        @param individualChannel: True if function called from gui_individualchannel for debugging purposes
        @param row, col: When individual channel is true, row and col ar used to access array stats for a row and col
        @return:
        """
        # AX1,AX3,AX4) Finding average ADC of samples per electrode

        # only some of the channels are actually recording, check for all which are false
        mask = np.copy(data_real)
        mask[mask == 0] = np.nan

        incom_cnt, incom_mean, incom_std = self.calculate_incoming_noise_statistics(data_real, mask)
        self.update_array_noise_statistics(incom_cnt, incom_mean, incom_std, individualChannel, row, col)
        incom_spike_cnt, incom_spike_avg, incom_spike_std = self.calculate_incoming_array_spike_statistics(data_real, mask)
        self.update_array_spike_statistics(incom_spike_cnt, incom_spike_avg, incom_spike_std, N)

    def calculate_incoming_noise_statistics(self, data_real, mask):
        # AX1,AX3,AX4) Sample Counting (Note: Appends are an artifact from previous real time codes)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            self.array_stats['num_sam'][:, :, 0] = np.count_nonzero(data_real, axis=2)
            incom_cnt = self.array_stats['num_sam'][:, :, 0]

            self.array_stats['avg_val'][:, :, 0] = np.nanmean(mask, axis=2)
            avg_val = np.nan_to_num(self.array_stats['avg_val'], nan=0)
            incom_mean = avg_val[:, :, 0]

            # AX3,AX4) Finding standard deviation ADC of samples per electrode
            incom_std = np.nanstd(mask, axis=2)
            incom_std = np.nan_to_num(incom_std, nan=0)
            print("incom_cnt: " + str(incom_cnt))
        return incom_cnt, incom_mean, incom_std

    def update_array_noise_statistics(self, incom_cnt, incom_mean, incom_std, individualChannel, row, col):
        # AX3,AX4) Building standard deviation of samples per electrode as buffers come in
        pre_mean = np.copy(self.array_stats["noise_mean"])
        pre_std = np.copy(self.array_stats["noise_std"])
        pre_cnt = np.copy(self.array_stats["noise_cnt"])
        cnt_div = pre_cnt + incom_cnt
        cnt_div[cnt_div == 0] = np.nan

        # Update noise mean, std using previous values and new values
        self.array_stats["noise_mean"] = np.nan_to_num((pre_cnt * pre_mean + incom_cnt * incom_mean) / (cnt_div), nan=0)
        self.array_stats["noise_std"] = np.sqrt(
            np.nan_to_num((pre_cnt * (pre_std ** 2 + (pre_mean - self.array_stats["noise_mean"]) ** 2) + incom_cnt * (
                    incom_std ** 2 + (incom_mean - self.array_stats["noise_mean"]) ** 2)) / (cnt_div), nan=0))
        self.array_stats["noise_cnt"] = np.nan_to_num(pre_cnt + incom_cnt, nan=0)
        print("noise cnt: " + str(self.array_stats["noise_cnt"]))

        if individualChannel:
            print(self.array_stats["noise_std"][row][col])

    def calculate_incoming_array_spike_statistics(self, data_real, mask):
        chan_cnt = np.count_nonzero(self.array_stats['num_sam'])
        chan_elec = np.zeros((chan_cnt, 2))
        chan_ind = np.argsort(self.array_stats['num_sam'].flatten())[-chan_cnt:]
        chan_elec[:, 0] = (chan_ind[:] / 32).astype(int)
        chan_elec[:, 1] = chan_ind[:] - (chan_elec[:, 0] * 32)
        chan_elec = chan_elec.astype(int)

        incom_spike_cnt = np.zeros((32, 32))
        incom_spike_avg = np.zeros((32, 32))
        incom_spike_std = np.zeros((32, 32))
        mask2 = np.copy(data_real)

        for x in range(len(chan_ind)):
            row = chan_elec[x, 0]
            col = chan_elec[x, 1]

            incom_spike_cnt[row][col] = self.array_stats["spike_cnt"][row][col]
            #print("row: " + str(row) + " col: " + str(col) + " " + str(incom_spike_cnt))

            # above_threshold = self.array_stats["noise_mean"][row, col] + \
            #                   self.data_processing_settings["spikeThreshold"] * self.array_stats["noise_std"][row, col]
            # above_threshold_activity = (mask[row, col, :] >= above_threshold)
            #
            # incom_spike_cnt[row, col] = np.count_nonzero(above_threshold_activity)
            #
            # #print("incom spike cnt: " + str(incom_spike_cnt[row,col]) + " ,r: " + str(row) + " ,c: " + str(col))
            # mask2[row, col, mask2[row, col, :] <= above_threshold] = np.nan

        self.array_stats["incom_spike_cnt"] = incom_spike_cnt

        #self.array_stats["incom_spike_times"] = incom_spike_times
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            incom_spike_avg = np.nanmean(mask2, axis=2)
            incom_spike_avg = np.nan_to_num(incom_spike_avg, nan=0)
            incom_spike_std = np.nanstd(mask2, axis=2)
            incom_spike_std = np.nan_to_num(incom_spike_std, nan=0)

        return incom_spike_cnt, incom_spike_avg, incom_spike_std

    def update_array_spike_statistics(self, incom_spike_cnt, incom_spike_avg, incom_spike_std, N, debug = False):
        pre_spike_avg = np.copy(self.array_stats["spike_avg"])
        pre_spike_std = np.copy(self.array_stats["spike_std"])
        pre_spike_cnt = np.copy(self.array_stats["spike_cnt"])

        new_spike_cnt = pre_spike_cnt + incom_spike_cnt
        new_spike_cnt[new_spike_cnt == 0] = np.nan

        self.array_stats["spike_avg"] = np.nan_to_num(
            (pre_spike_cnt * pre_spike_avg + incom_spike_cnt * incom_spike_avg) / (new_spike_cnt),
            nan=0)
        self.array_stats["spike_std"] = np.sqrt(np.nan_to_num((pre_spike_cnt * (
                pre_spike_std ** 2 + (pre_spike_avg - self.array_stats["spike_avg"]) ** 2) + incom_spike_cnt * (
                                                                       incom_spike_std ** 2 + (
                                                                       incom_spike_avg - self.array_stats[
                                                                   "spike_avg"]) ** 2)) / (
                                                                  new_spike_cnt), nan=0))
        self.array_stats["spike_cnt"] = np.nan_to_num(new_spike_cnt, nan=0)


        # AX2) Determine the Time of Each Sample
        total_time = N * 0.05  # Sampling rate 1/0.05 ms
        self.array_stats["times"] = np.linspace(0, total_time, N)

        self.array_stats["array spike rate times"].append(total_time)

        # Buffer time is ~500 ms, divided by number of channels to give time recorded for the last set of packets
        # Divide the total number of spikes from the last recorded channels by this time, x1000 --> spikes/sec
        self.array_stats["array spike rate"].append(
            1000*(np.sum(incom_spike_cnt)/(500/int(self.data_processing_settings["simultaneousChannelsRecordedPerPacket"]))))

        if debug:
            print(self.array_stats["spike_cnt"])

        return incom_spike_cnt, incom_spike_avg, incom_spike_std