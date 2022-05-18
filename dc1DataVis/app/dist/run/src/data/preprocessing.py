"""
@authors Maddy Hays, Huy Nguyen (2022)

"""
import numpy as np
import time

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

"""
======================
HELPER FUNCTIONS
======================
"""
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
    else:
        ch_row = int(ch_idx/32)
        ch_col = int(ch_idx - ch_row*32)
    return ch_row, ch_col




