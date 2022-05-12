import numpy as np
import time
from ..data.preprocessing import *
from ..data.filters import *

piece_no = 1
time_win = 190  # The amount of time (ms) you want to view in each frame
spike_t = 3  # How many standard deviations above noise to find spikes
max_dot = 300  # Saturation point for dot size

class DC1DataContainer():
    """
    Container for holding all different types of data.
    """
    # raw_data --> recorded_data --> filtered_data
    # raw_data: data loader from .mat files
    raw_data, counts, times = None, None, None
    count_track, time_track = None, None
    container_length = None

    # recorded_data: nonzero data
    # each element in recorded_data is data for one channel recorded
    recorded_data = []
    count_track_processed, time_track_processed = None, None

    # filtered_data: recorded_data gone through a filter
    # each element in filtered_data is filtered data for one channel
    filtered_data = []

    # array_statistics: overall array stats
    array_stats = {
        "size": np.zeros((32, 32, 0)),  # For each dot, size by # of samples
        "num_sam": np.zeros((32, 32, 1)),  # Temp variable to allow sample counting
        "colors": np.zeros((32, 32, 0)),  # For each dot, color by avg amplitude
        "avg_val": np.zeros((32, 32, 1)),  # Temp variable for calculating average amplitude
        "noise_mean": np.zeros((32, 32)),
        "noise_std": np.zeros((32, 32)),
        "noise_cnt": np.zeros((32, 32)),
        "spike_avg": np.zeros((32, 32)),
        "spike_std": np.zeros((32, 32)),
        "spike_cnt": np.zeros((32, 32)),
        "size": None,
        "times": None
    }

    # TODO combine with identity_relevant_channels
    def __init__(self):
        self.time_track = 0
        self.count_track = 0
        self.count_track_processed = 0
        self.time_track_processed = 0

        self.raw_data = np.zeros((32, 32, 1000))
        self.counts = np.zeros((32, 32, 1000))
        self.times = np.zeros((1000,))
        self.container_length = 1000

    def extend_data_containers(self, mode='double'):
        """Change data containers dynamically to accommodate longer time windows of data

        Args:
            mode: how to expand data containers

        Returns:
            Nothing
        """

        if mode == 'double':
            padding_data = np.zeros(self.raw_data.shape)
            padding_cnt = np.zeros(self.counts.shape)
            padding_times = np.zeros(self.times.shape)

        self.raw_data = np.concatenate((self.raw_data, padding_data), axis=2)
        self.counts = np.concatenate((self.counts, padding_cnt), axis=2)
        self.times = np.concatenate((self.times, padding_times))
        self.container_length *= 2

    def append_raw_data(self, data_real, cnt_real, N, sampling_period=0.05):
        """ appends raw data in buffer to end of data container, append nonzero data to recorded_data

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
        end_time = N * sampling_period  # 20kHz sampling rate, means time_recording (ms) = num_sam*0.05ms

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
            channel_data = {
                'channel_idx': channel_idx,
                'start_idx': int(self.count_track + start_idx),  # start_idx is based only on buffer, so need to add time from previous buffers
                'data': data_real[x, y, start_idx:N], # TODO make this accurate
                'times': self.times[self.count_track + start_idx:self.count_track+N]
            }
            self.recorded_data.append(channel_data)
        self.time_track += end_time
        self.count_track += N

        # TODO this shouldn't call update_filtered_data -> should be async, and threaded


    def update_filtered_data(self, num_threads=4, filtType='modHierlemann'):
        # subtract recorded_data by filtered_data
        len_recorded_data = len(self.recorded_data)
        len_filtered_data = len(self.filtered_data)

        # TODO parallelize filtering
        if len_filtered_data < len_recorded_data:
            while len_filtered_data < len_recorded_data:
                to_filter_idx = len_filtered_data
                to_filter_data = self.recorded_data[to_filter_idx]['data']
                filtered_data = applyFilterToChannelData(to_filter_data, filtType=filtType)
                filtered_data = {
                    'channel_idx': self.recorded_data[to_filter_idx]['channel_idx'],
                    'start_idx': self.recorded_data[to_filter_idx]['start_idx'],
                    # start_idx is based only on buffer, so need to add time from previous buffers
                    'data': filtered_data,  # TODO make this accurate
                    'times': self.recorded_data[to_filter_idx]['times']
                }
                self.filtered_data.append(filtered_data)
                len_filtered_data += 1

    def update_array_stats(self, data_real, N):
        """

        Args:
            data_real:
            N:

        Returns:

        """
        # AX1,AX3,AX4) Sample Counting (Note: Appends are an artifact from previous real time codes)
        self.array_stats['num_sam'][:, :, 0] = np.count_nonzero(data_real, axis=2)
        incom_cnt = self.array_stats['num_sam'][:, :, 0]

        # AX2) Time Domain Electrodes to Plot
        fig_rows = np.count_nonzero(self.array_stats['num_sam'])
        if fig_rows == 0:
            fig_rows = 1
        if fig_rows > 4:
            fig_rows = 4
        fig_elec = np.zeros((fig_rows, 2))

        fig_ind = np.argsort(self.array_stats['num_sam'].flatten())[-fig_rows:]
        fig_elec[:, 0] = (fig_ind[:] / 32).astype(int)
        fig_elec[:, 1] = fig_ind[:] - (fig_elec[:, 0] * 32)
        fig_elec = fig_elec.astype(int)

        # AX1,AX3,AX4) Finding average ADC of samples per electrode
        mask = np.copy(data_real)
        mask[mask == 0] = np.nan
        self.array_stats['avg_val'][:, :, 0] = np.nanmean(mask, axis=2)
        avg_val = np.nan_to_num(self.array_stats['avg_val'], nan=0)
        incom_mean = avg_val[:, :, 0]

        # AX3,AX4) Finding standard deviation ADC of samples per electrode
        incom_std = np.nanstd(mask, axis=2)
        incom_std = np.nan_to_num(incom_std, nan=0)

        # AX3,AX4) Building standard deviation of samples per electrode as buffers come in
        pre_mean = np.copy(self.array_stats["noise_mean"])
        pre_std = np.copy(self.array_stats["noise_std"])
        pre_cnt = np.copy(self.array_stats["noise_cnt"])
        cnt_div = pre_cnt + incom_cnt
        cnt_div[cnt_div == 0] = np.nan

        self.array_stats["noise_mean"] = np.nan_to_num((pre_cnt * pre_mean + incom_cnt * incom_mean) / (cnt_div), nan=0)
        self.array_stats["noise_std"] = np.sqrt(np.nan_to_num((pre_cnt * (pre_std ** 2 + (pre_mean - self.array_stats["noise_mean"]) ** 2) + incom_cnt * (
                    incom_std ** 2 + (incom_mean - self.array_stats["noise_mean"]) ** 2)) / (cnt_div), nan=0))
        self.array_stats["noise_cnt"] = np.nan_to_num(pre_cnt + incom_cnt, nan=0)

        # NEW AX1)
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
            self.array_stats["noise_std"] = self.array_stats["noise_std"]
            incom_spike_cnt[chan_elec[x, 0], chan_elec[x, 1]] = np.count_nonzero(
                mask[chan_elec[x, 0], chan_elec[x, 1], :] >= self.array_stats["noise_mean"][chan_elec[x, 0], chan_elec[x, 1]] + spike_t *
                self.array_stats["noise_std"][chan_elec[x, 0], chan_elec[x, 1]])
            mask2[chan_elec[x, 0], chan_elec[x, 1], mask2[chan_elec[x, 0], chan_elec[x, 1], :] <= self.array_stats["noise_mean"][
                chan_elec[x, 0], chan_elec[x, 1]] + spike_t * self.array_stats["noise_std"][chan_elec[x, 0], chan_elec[x, 1]]] = np.nan

        incom_spike_avg = np.nanmean(mask2, axis=2)
        incom_spike_avg = np.nan_to_num(incom_spike_avg, nan=0)
        incom_spike_std = np.nanstd(mask2, axis=2)
        incom_spike_std = np.nan_to_num(incom_spike_std, nan=0)

        pre_spike_avg = np.copy(self.array_stats["spike_avg"])
        pre_spike_std = np.copy(self.array_stats["spike_std"])
        pre_spike_cnt = np.copy(self.array_stats["spike_cnt"])

        new_spike_cnt = pre_spike_cnt + incom_spike_cnt
        new_spike_cnt[new_spike_cnt == 0] = np.nan

        self.array_stats["spike_avg"] = np.nan_to_num((pre_spike_cnt * pre_spike_avg + incom_spike_cnt * incom_spike_avg) / (new_spike_cnt),
                                  nan=0)
        self.array_stats["spike_std"] = np.sqrt(np.nan_to_num((pre_spike_cnt * (
                    pre_spike_std ** 2 + (pre_spike_avg - self.array_stats["spike_avg"]) ** 2) + incom_spike_cnt * (
                                                       incom_spike_std ** 2 + (incom_spike_avg - self.array_stats["spike_avg"]) ** 2)) / (
                                              new_spike_cnt), nan=0))
        self.array_stats["spike_cnt"] = np.nan_to_num(new_spike_cnt, nan=0)

        # AX1) Colors by Average Electrode Amplitude
        self.array_stats["colors"] = np.copy(self.array_stats["spike_avg"])

        # AX1) Size by Number of Samples
        scale1 = (max_dot - 15) / (np.max(self.array_stats["spike_cnt"]) - np.min(self.array_stats["spike_cnt"][self.array_stats["spike_cnt"]!=0]))
        b_add = max_dot - (np.max(self.array_stats["spike_cnt"]) * scale1)
        self.array_stats["size"] = np.round(self.array_stats["spike_cnt"] * scale1 + b_add)
        self.array_stats["size"][self.array_stats["size"] < 15] = 10

        #     max_sam = np.max(num_sam[:,:,0])
        #     min_sam = np.min(num_sam[num_sam!=0])
        #     if max_sam == min_sam:
        #         min_sam = 0
        #     scale = (max_dot - 15) / (max_sam - min_sam)
        #     b_add = max_dot - (max_sam*scale)
        #     size = np.append(size,np.round(num_sam*scale+b_add),axis=2)
        #     size[size<15] = 10

        # AX2) Determine the Time of Each Sample
        total_time = N * 0.05  # Sampling rate 1/0.05 ms
        self.array_stats["times"] = np.linspace(0, total_time, N)


