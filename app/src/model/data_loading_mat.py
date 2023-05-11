"""
Functions for loading model files into form that can be read by GUI
"""''

import os
import scipy.io as sio

from .spike_detection import *
from ..model.filters import *

from PyQt5.QtWidgets import QMessageBox, QDialog, QLabel, QPushButton, QVBoxLayout
import sys


def load_first_buffer_info(app):
    """

    Args:
        app: MainWindow

    Returns:

    """
    wait_for_data_msg = QMessageBox()
    wait_for_data_msg.setWindowTitle("Waiting for data.")
    wait_for_data_msg.setText("Click \"OK\" to continue waiting for data. GUI will pop up when data is loaded. ")
    wait_for_data_msg.setIcon(QMessageBox.Information)

    wait_for_data_msg.exec ()
    while len(os.listdir(app.settings["path"])) == 0:
        continue
    wait_for_data_msg.close ()


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
    """

    Args:
        params:

    Returns:

    """
    # this is designed to be multi-processed
    file_dir = params["file_dir"]
    filter_type = params["filter_type"]
    SPIKING_THRESHOLD = params["SPIKING_THRESHOLD"]
    BIN_SIZE = params["BIN_SIZE"]

    mat_contents = sio.loadmat(file_dir)
    dataRaw = mat_contents['gmem1'][0][:]

    from app.src.model.raw_data_helpers import removeMultipleCounts
    data_real, cnt_real, N = removeMultipleCounts(dataRaw)

    # Note: this code does not timestamp model bc that cannot be parallelized properly
    packet_data = preprocess_raw_data(data_real, cnt_real, N)
    packet = {
        "packet_data": packet_data,
        "packet_idx": params["packet_idx"],
        "file_dir": params["file_dir"],
        "filter_type": params["filter_type"]
    }

    from app.src.model.filters import filter_preprocessed_data
    packet = filter_preprocessed_data(packet, filter_type=filter_type)

    from app.src.model.statistics import calculate_channel_stats
    packet = calculate_channel_stats(packet, SPIKING_THRESHOLD, BIN_SIZE)

    return packet

def preprocess_raw_data(data_real, cnt_real, N, SAMPLING_PERIOD=0.05):
    """

    Args:
        data_real:
        cnt_real:
        N:
        SAMPLING_PERIOD:

    Returns:

    """
    # Determine time estimate and sample counts for the total combined buffers
    # (note this does not take into account communication delays - hence an estimate)
    end_time = N * SAMPLING_PERIOD  # 20kHz sampling rate, means time_recording (ms) = num_sam * 0.05ms

    # we are not determining absolute time, because we want to parallelize this,
    # and time tracking must be done in sequence
    times = np.linspace(0, end_time, N + 1)

    # identify relevant, nonzero channels, and then append only this model into recorded_data
    from src.model.raw_data_helpers import identify_relevant_channels
    num_channels, channel_map, channel_id, start_idx, find_coords, recorded_channels = identify_relevant_channels(data_real)

    packet_data = []
    for i in range(recorded_channels.shape[0]):

        # process each channel index
        channel_idx = int(recorded_channels[i][0])
        x, y = idx2map(channel_idx)
        start_idx = recorded_channels[i][0]

        channel_data = data_real[x, y, start_idx:N]
        # channel_times = self.times[self.count_track + start_idx: self.count_track+N] can't do
        # prune the times in the packet where nothing is recorded (aka when model == 0)
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
    """

    Args:
        path:

    Returns:

    """
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

def map2idx(ch_row: int, ch_col: int):
    """ Given a channel's row and col, return channel's index

    Args:
        ch_row: row index of channel in array (up to 32)
        ch_col: column index of channel in array (up to 32)

    Returns: numerical index of array
    """
    if ch_row > 31 or ch_row < 0: print('Row out of range')
    elif ch_col > 31 or ch_col < 0: print('Col out of range')
    else: ch_idx = int(ch_row * 32 + ch_col)
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



