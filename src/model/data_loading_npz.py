import numpy as np
import pandas as pd
from collections import deque
import queue

def load_npz_file(app):
    print('Loading offline data! This may take several seconds...')

    data = np.load(app.settings["path"])
    print(data.files)
    modified_data = data['modified_data'] # 32 x 32 x N
    #print("modified data", modified_data.shape)

    # list_of_bufs: num buffers x 8 channels per buf x normal sample length of each channel recorded
    #list_of_bufs = np.reshape(modified_data, (32*4, 8, modified_data.shape[2]))
    q = queue.Queue()

    offline_data = OfflineDataLoader(app)

    buf_data = []
    buf_chan_idxs = []
    buf_times = []
    for r in range(32):
        for c in range(32):
            nonzero_data_idx = np.where(modified_data[r,c,:] != 0.)
            if len(nonzero_data_idx[0]) == 0:
                continue

            if len(buf_data) == 8:
                packet = load_one_simulated_mat_file(app, buf_data, buf_chan_idxs)
                offline_data.append_offline_buf(packet, buf_times, buf_chan_idxs)
                buf_data = []
                buf_chan_idxs = []
                buf_times = []

            CUTOFF = 500
            data = modified_data[r,c,nonzero_data_idx[0]][:CUTOFF]
            times = nonzero_data_idx[0][:CUTOFF]

            from src.model.data_loading_mat import map2idx
            chan_idx = map2idx(r,c)

            buf_data.append(data)
            buf_times.append(times)
            buf_chan_idxs.append(chan_idx)

    return offline_data

# mirrors load_one_mat_file in data_loading_mat.py
def load_one_simulated_mat_file(app, data, chan_idxs):
    #print("load one simulated mat file data", data)
    filter_type = app.settings["filter"]
    SPIKING_THRESHOLD = app.settings["spikeThreshold"]
    BIN_SIZE = app.settings["binSize"]

    packet_data = []
    for i in range(len(data)):
        channel_data = {
            "N": len(data[i]),
            "channel_idx": chan_idxs[i],
            "preprocessed_data": data[i]
        }
        packet_data.append(channel_data)

    packet = {
        "packet_data": packet_data,
        "packet_idx": 0,
        "file_dir": "",
        "filter_type": app.settings["filter"]
    }

    from src.model.filters import filter_preprocessed_data
    packet = filter_preprocessed_data(packet, filter_type=filter_type)
    from src.model.statistics import calculate_channel_stats
    packet = calculate_channel_stats(packet, SPIKING_THRESHOLD, BIN_SIZE)
    return packet

# mirrors DC1DataContainer
class OfflineDataLoader():
    to_show = None
    ARRAY_NUM_ROWS = 32
    ARRAY_NUM_COLS = 32
    avg_spike_rate_x = []
    avg_spike_rate_y = []

    def __init__(self, app):
        self.app = app
        self.time_track, self.count_track = 0, 0
        self.time_track_processed, self.count_track_processed = 0, 0

        # channel-level information
        # indexed via row, col of array
        # value: a dict containing all info for a certain electrode
        # self.array_indexed_df = pd.Dataframe() # TODO make array-indexed pandas df to replace below

        df_columns = ["row", "col",  # indexing
                      "avg_filtered_amp", "avg_unfiltered_amp", "channel_noise_mean", "channel_noise_std",  # noise
                      "start_time", "start_count", "buf_recording_len", "N", "packet_idx",  # timing
                      "spikes_avg_amp", "spikes_cnt", "spikes_std", "spikes_cum_cnt", "num_bins_per_buffer",  # spikes
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

        self.buffer_indexed = []
        self.to_show = queue.Queue()

    def append_offline_buf(self, buf, times, idx):
        # data: 1 x 8 channels per buf x normal sample length of each channel recorded

        packet_idx = buf['packet_idx']
        channel_idxs = []  # for buffer_indexed model struct

        """
        # calculate times
        N = buf["packet_data"][0]["N"]
        len_packet_time = N * 0.05  # 20kHz sampling rate, means time_recording (ms) = num_sam*0.05ms
        next_times = np.linspace(self.time_track, self.time_track + len_packet_time, N)
        self.time_track += len_packet_time
        self.count_track += N
        """
        N = len(times)
        #print("times", times)
        next_times = times[0].astype(float) * 0.05 #hack need to fix
        len_packet_time = N * 0.05
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
            from src.model.data_loading_mat import idx2map
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
            # print('array spike times -> spike_bins', packet["spike_bins"])
            # print('array spike times -> spike_bins_max_amp', packet["spike_bins_max_amps"])
            self.array_spike_times["spike_bins"][this_channel_idx] = packet["spike_bins"]
            self.array_spike_times["spike_bins_max_amps"][this_channel_idx] = packet["spike_bins_max_amps"]

            avg_packet_spike_count += packet["stats_spikes+cnt"]
        # buffer-level information
        buffer_indexed_dict = {
            "file_dir": buf["file_dir"],
            "filter_type": buf["filter_type"],
            "N": N,
            "time_elapsed": len_packet_time,  # TODO check if this is accurate for all recording types
            "channel_idxs": channel_idxs,
            "num_detected_spikes": avg_packet_spike_count / len(packet_data)  # for spike rate plot
        }
        self.buffer_indexed.append(buffer_indexed_dict)

        self.calculate_moving_spike_rate_avg()
        self.to_show.put(buf)

        # return the channels in the buffer
        return buffer_indexed_dict["channel_idxs"]

    def calculate_moving_spike_rate_avg(self):
        """

        Returns:

        """
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