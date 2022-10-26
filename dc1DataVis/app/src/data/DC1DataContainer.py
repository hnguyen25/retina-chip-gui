import numpy as np
import time

from dc1DataVis.app.src.data.data_loading import *

from ..data.filters import *
import warnings
import queue

class DC1DataContainer:
    """
    Container for holding recording data for the DC1 retina chip. Each container is designed to hold all
    the relevant information extracted from data collected from a SINGLE recording, of any particular type.

    To-Dos:
    ----------
    TODO figure out time alignment of the data / the actual sampling rate / check for dropped packets
    TODO figure out time budget for data processing + filtering
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

    # new data structs
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
        self.array_indexed = {
            "start_time": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
            "start_count": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
            "packet_idx": [([] for i in range(self.ARRAY_NUM_ROWS)) for j in range(self.ARRAY_NUM_COLS)],
            "size": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS, 0)),  # For each dot, size by # of samples
            "stats_cnt": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS, 1)),  # sample counting
            "colors": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS, 0)),  # For each dot, color by avg amplitude
            "avg_amp": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS, 1)),  # for calculating avg amp
            "stats_noise+mean": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
            "stats_noise+std": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
            "stats_buf+recording+len": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
            "stats_avg+unfiltered+amp": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
            "stats_spikes+avg+amp": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
            "stats_spikes+std": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
            "stats_spikes+cnt": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
            "stats_num+spike+bins+in+buffer": np.zeros((self.ARRAY_NUM_ROWS, self.ARRAY_NUM_COLS)),
            "spike_bins": [([] for i in range(self.ARRAY_NUM_ROWS)) for j in range(self.ARRAY_NUM_COLS)],
            "spike_bins_max_amps": [([] for i in range(self.ARRAY_NUM_ROWS)) for j in range(self.ARRAY_NUM_COLS)]

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
        channel_idxs = []  # for buffer_indexed data struct

        # calculate times
        N = buf["packet_data"][0]["N"]
        len_packet_time = N * 0.05  # 20kHz sampling rate, means time_recording (ms) = num_sam*0.05ms
        next_times = np.linspace(self.time_track, self.time_track + len_packet_time, N)
        self.time_track += len_packet_time
        self.count_track += N

        avg_packet_spike_count = 0
        packet_data = buf['packet_data']
        for packet in packet_data:

            # load data
            # packet keys: 'data_real', 'cnt_real', 'N',
            #   'channel_idx', 'preprocessed_data', 'filtered_data',
            #   'stats_cnt', 'stats_noise+mean', 'stats_noise+std'
            this_channel_idx = packet['channel_idx']

            # for buffer_indexed data struct
            channel_idxs.append(this_channel_idx)

            # reformatting packet for to_show data struct
            packet["times"] = next_times

            # for array_indexed data struct
            r, c = idx2map(this_channel_idx)

            # TODO make this adapt for when multiple packets record from the same channel
            # use formula Maddy gave
            self.array_indexed["stats_cnt"][r][c] += packet["stats_cnt"]
            self.array_indexed["stats_avg+unfiltered+amp"][r][c] = packet["stats_avg+unfiltered+amp"] # of unfiltered data
            self.array_indexed["stats_noise+mean"][r][c] = packet["stats_noise+mean"]
            self.array_indexed["stats_noise+std"][r][c] = packet["stats_noise+std"]
            self.array_indexed["stats_buf+recording+len"][r][c] = packet["stats_buf+recording+len"]
            self.array_indexed["stats_spikes+cnt"][r][c] = packet["stats_spikes+cnt"]
            self.array_indexed["stats_spikes+avg+amp"][r][c] = packet["stats_spikes+avg+amp"]
            self.array_indexed["stats_spikes+std"][r][c] = packet["stats_spikes+std"]
            self.array_indexed["stats_num+spike+bins+in+buffer"][r][c] = packet["stats_num+spike+bins+in+buffer"]
            # TODO bug with generator object
            #self.array_indexed["spike_bins"][r][c] = packet["spike_bins"]
            #self.array_indexed["spike_bins_max_amps"][r][c] = packet["spike_bins_max_amps"]
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

        print('avg spike rate before division', avg_spike_rate)
        avg_spike_rate /= time_elapsed

        x = self.time_track
        y = avg_spike_rate

        self.avg_spike_rate_x.append(x)
        self.avg_spike_rate_y.append(y)
