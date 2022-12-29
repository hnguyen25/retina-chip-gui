import numpy as np
import time

from app.src.model.data_loading import *
from ..model.filters import *
import warnings
import queue
import pandas as pd  # TODO make a pandas dataframe for array info

class DC1DataContainer:
    """
    Container for holding recording model for the DC1 retina chip. Each container is designed to hold all
    the relevant information extracted from model collected from a SINGLE recording, of any particular type.

    To-Dos:
    ----------
    TODO figure out time alignment of the model / the actual sampling rate / check for dropped packets
    TODO figure out time budget for model processing + filtering
    """

    # +++++ CONSTANTS +++++
    # DC1/RC1.5 is a multi-electrode array (MEA) with 32 x 32 channels (1024 total)
    ARRAY_NUM_ROWS, ARRAY_NUM_COLS = 32, 32

    count_track, time_track = None, None

    # calculated statistics
    spike_data = {
        'times': np.zeros((32, 32)),  # np.array with dims 32 x 32 x num_bins
        'amplitude': np.zeros((32, 32))
    }

    # new model structs
    to_serialize, to_show = None, None

    avg_spike_rate_x = []
    avg_spike_rate_y = []

    def __init__(self, app, recording_info={}, data_processing_settings={}):
        self.app = app  # reference to MainWindow
        self.time_track, self.count_track = 0, 0
        self.time_track_processed, self.count_track_processed = 0, 0

        # channel-level information
        # indexed via row, col of array
        # value: a dict containing all info for a certain electrode
        # self.array_indexed_df = pd.Dataframe() # TODO make array-indexed pandas df to replace below

        df_columns = ["row", "col", # indexing
                      "avg_filtered_amp", "avg_unfiltered_amp", "channel_noise_mean", "channel_noise_std", # noise
                      "start_time", "start_count", "buf_recording_len", "N", "packet_idx", # timing
                      "spikes_avg_amp", "spikes_cnt", "spikes_std", "spikes_cum_cnt", "num_bins_per_buffer", #spikes
                      "array_dot_color", "array_dot_size"  # specific plot info
                      ]

        initial_data = []
        for i in range(32):
            for j in range(32):
                initial_data.append([i, j,
                                     0., 0., 0., 0.,
                                     0., 0., 0., 0., 0.,
                                     0., 0., 0., 0., 0.,
                                     0., 0.])
        self.df = pd.DataFrame(initial_data, columns=df_columns)

        self.stats = {"largest_spike_cnt": 0}

        self.array_spike_times = {
            "spike_bins": [[] for i in range(self.ARRAY_NUM_ROWS * self.ARRAY_NUM_COLS)],
            "spike_bins_max_amps": [[] for i in range(self.ARRAY_NUM_ROWS * self.ARRAY_NUM_COLS)]
        }

        # =====================
        # buffer-level information
        # indexed via key: buffer number (0 - MAX_NUMBER_OF_BUFFERS)
        # value:
        self.buffer_indexed = []
        self.to_serialize = queue.Queue()
        self.to_show = queue.Queue()

    def append_buf(self, buf):
        packet_idx = buf['packet_idx']
        channel_idxs = []  # for buffer_indexed model struct

        # calculate times
        N = buf["packet_data"][0]["N"]
        len_packet_time = N * 0.05  # 20kHz sampling rate, means time_recording (ms) = num_sam*0.05ms
        next_times = np.linspace(self.time_track, self.time_track + len_packet_time, N)
        self.time_track += len_packet_time
        self.count_track += N

        avg_packet_spike_count = 0
        packet_data = buf['packet_data']
        for packet in packet_data:

            # load model
            # packet keys: 'data_real', 'cnt_real', 'N',
            #   'channel_idx', 'preprocessed_data', 'filtered_data',
            #   'stats_cnt', 'stats_noise+mean', 'stats_noise+std'
            this_channel_idx = packet['channel_idx']

            # for buffer_indexed model struct
            channel_idxs.append(this_channel_idx)

            # reformatting packet for to_show model struct
            packet["times"] = next_times

            # for array_indexed model struct
            r, c = idx2map(this_channel_idx)

            # TODO make this adapt for when multiple packets record from the same channel
            # use formula Maddy gave

            df_columns = ["row", "col",  # indexing
                          "avg_filtered_amp", "avg_unfiltered_amp", "noise_mean", "noise_std",  # noise
                          "start_time", "start_count", "buf_recording_len", "N", "packet_idx",  # timing
                          "spikes_avg_amp", "spikes_cnt", "spikes_std", "spikes_cum_cnt",
                          "num_bins_per_buffer"]  # spikes


            self.df.at[this_channel_idx, "N"] += packet["stats_cnt"]
            self.df.at[this_channel_idx, "avg_unfiltered_amp"] = packet["stats_avg+unfiltered+amp"]
            self.df.at[this_channel_idx, "noise_mean"] = packet["stats_noise+mean"]
            self.df.at[this_channel_idx, "noise_std"] = packet["stats_noise+std"]

            self.df.at[this_channel_idx, "buf_recording_len"] = packet["stats_buf+recording+len"]
            self.df.at[this_channel_idx, "avg_unfiltered_amp"] = packet["stats_avg+unfiltered+amp"]

            self.df.at[this_channel_idx, "spikes_cnt"] = packet["stats_spikes+cnt"]
            self.df.at[this_channel_idx, "spikes_cum_cnt"] += packet["stats_spikes+cnt"]
            self.df.at[this_channel_idx, "spikes_avg_amp"] += packet["stats_spikes+avg+amp"]
            self.df.at[this_channel_idx, "spikes_std"] += packet["stats_spikes+std"]


            """
            self.array_indexed = {
                "stats_num+spike+bins+in+buffer": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
                "spike_bins": [([] for i in range(self.ARRAY_NUM_ROWS)) for j in range(self.ARRAY_NUM_COLS)],
                "spike_bins_max_amps": [([] for i in range(self.ARRAY_NUM_ROWS)) for j in range(self.ARRAY_NUM_COLS)]
            }   
            """
            # TODO put spike bins here
            #print('array spike times -> spike_bins', packet["spike_bins"])
            #print('array spike times -> spike_bins_max_amp', packet["spike_bins_max_amps"])
            self.array_spike_times["spike_bins"][this_channel_idx] = packet["spike_bins"]
            self.array_spike_times["spike_bins_max_amps"][this_channel_idx] = packet["spike_bins_max_amps"]


            avg_packet_spike_count += packet["stats_spikes+cnt"]
        # buffer-level information
        buffer_indexed_dict = {
            "file_dir": buf["file_dir"],
            "filter_type": buf["filter_type"],
            "N": N,
            "time_elapsed": len_packet_time, # TODO check if this is accurate for all recording types
            "channel_idxs": channel_idxs,
            "num_detected_spikes": avg_packet_spike_count / len(packet_data) # for spike rate plot
        }
        self.buffer_indexed.append(buffer_indexed_dict)

        self.calculate_moving_spike_rate_avg()

        self.to_show.put(buf)

        # return the channels in the buffer
        return buffer_indexed_dict["channel_idxs"]

    def calculate_moving_spike_rate_avg(self):
        avg_spike_rate = 0
        time_elapsed = 0

        SPIKE_RATE_WINDOW_SIZE = 4
        if len(self.buffer_indexed) < SPIKE_RATE_WINDOW_SIZE:
            for buffer in self.buffer_indexed:
                avg_spike_rate += buffer["num_detected_spikes"]
                time_elapsed += buffer["time_elapsed"]
        else:
            for buffer in self.buffer_indexed[-1 - SPIKE_RATE_WINDOW_SIZE: -1]:
                avg_spike_rate += buffer["num_detected_spikes"]
                time_elapsed += buffer["time_elapsed"]

        #print('avg spike rate before division', avg_spike_rate)
        avg_spike_rate /= time_elapsed

        x = self.time_track
        y = avg_spike_rate

        self.avg_spike_rate_x.append(x)
        self.avg_spike_rate_y.append(y)

def map2idx(ch_row: int, ch_col: int):
    """ Given a channel's row and col, return channel's index

    Args:
        ch_row: row index of channel in array (up to 32)
        ch_col: column index of channel in array (up to 32)

    Returns: numerical index of array
    """
    if ch_row > 31 or ch_row < 0:
        print('Row out of range')
    elif ch_col > 31 or ch_col < 0:
        print('Col out of range')
    else:
        ch_idx = int(ch_row*32 + ch_col)
    return ch_idx