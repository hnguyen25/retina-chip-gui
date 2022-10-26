"""
PyqtGraphParams
-----------------
this is the general class from which all the different GUI analysis graphs/tools will inherit from

contains basic parameters and variables associated with making a pyqtgraph, as well as relevant functions
to update parameters and the graph in the GUI

@authors Huy Nguyen (2022)

"""
piece_no = 1
time_win = 190 #The amount of time (ms) you want to view in each frame
spike_t = 3 #How many standard deviations above noise to find spikes
max_dot = 300 #Saturation point for dot size

import numpy as np
class PyqtGraphParams():

    # pyqtwidget that this parameter data is attached to
    window_reference = None

    parameters = {
        'graph_label':'',
        'left_label': '',
        'bottom_label': '',
        'center_x': 0,
        'center_y': 0,
        'font_size': 12
    }
    graph_data = {
        "size": np.zeros((32, 32, 0)),  # For each dot, size by # of samples
        "num_sam": np.zeros((32, 32, 1)),  # Temp variable to allow sample counting
        "colors": np.zeros((32, 32, 0)),  # For each dot, color by avg amplitude
        "avg_val": np.zeros((32, 32, 1)), # Temp variable for calculating average amplitude
        "noise_mean" : np.zeros((32, 32)),
        "noise_std" : np.zeros((32, 32)),
        "noise_cnt" : np.zeros((32, 32)),
        "spike_avg" : np.zeros((32, 32)),
        "spike_std" : np.zeros((32, 32)),
        "spike_cnt" : np.zeros((32, 32)),
        "size":None,
        "times":None
    }


    def __init__(self, param_dict : dict):
        # initialize with passed through parameters
        for key in param_dict.keys():
            if key in self.parameters:
                self.parameters[key] = param_dict[key]

    def update_parameters(self, param_dict : dict):
        for key in param_dict.keys():
            if key in self.parameters:
                self.parameters[key] = param_dict[key]

    def update_gui_reference(self, window):
        self.window_reference = window

    def update_graph(self):
        pass


    def update_general_graph_data(self, data_real, N):
        # AX1,AX3,AX4) Sample Counting (Note: Appends are an artifact from previous real time codes)
        self.graph_data['num_sam'][:, :, 0] = np.count_nonzero(data_real, axis=2)
        incom_cnt = self.graph_data['num_sam'][:, :, 0]

        # AX2) Time Domain Electrodes to Plot
        fig_rows = np.count_nonzero(self.graph_data['num_sam'])
        if fig_rows == 0:
            fig_rows = 1
        if fig_rows > 4:
            fig_rows = 4
        fig_elec = np.zeros((fig_rows, 2))

        fig_ind = np.argsort(self.graph_data['num_sam'].flatten())[-fig_rows:]
        fig_elec[:, 0] = (fig_ind[:] / 32).astype(int)
        fig_elec[:, 1] = fig_ind[:] - (fig_elec[:, 0] * 32)
        fig_elec = fig_elec.astype(int)

        # AX1,AX3,AX4) Finding average ADC of samples per electrode
        mask = np.copy(data_real)
        mask[mask == 0] = np.nan
        self.graph_data['avg_val'][:, :, 0] = np.nanmean(mask, axis=2)
        avg_val = np.nan_to_num(self.graph_data['avg_val'], nan=0)
        incom_mean = avg_val[:, :, 0]

        # AX3,AX4) Finding standard deviation ADC of samples per electrode
        incom_std = np.nanstd(mask, axis=2)
        incom_std = np.nan_to_num(incom_std, nan=0)

        # AX3,AX4) Building standard deviation of samples per electrode as buffers come in
        pre_mean = np.copy(self.graph_data["noise_mean"])
        pre_std = np.copy(self.graph_data["noise_std"])
        pre_cnt = np.copy(self.graph_data["noise_cnt"])
        cnt_div = pre_cnt + incom_cnt
        cnt_div[cnt_div == 0] = np.nan

        self.graph_data["noise_mean"] = np.nan_to_num((pre_cnt * pre_mean + incom_cnt * incom_mean) / (cnt_div), nan=0)
        self.graph_data["noise_std"] = np.sqrt(np.nan_to_num((pre_cnt * (pre_std ** 2 + (pre_mean - self.graph_data["noise_mean"]) ** 2) + incom_cnt * (
                    incom_std ** 2 + (incom_mean - self.graph_data["noise_mean"]) ** 2)) / (cnt_div), nan=0))
        self.graph_data["noise_cnt"] = np.nan_to_num(pre_cnt + incom_cnt, nan=0)

        # NEW AX1)
        chan_cnt = np.count_nonzero(self.graph_data['num_sam'])
        chan_elec = np.zeros((chan_cnt, 2))
        chan_ind = np.argsort(self.graph_data['num_sam'].flatten())[-chan_cnt:]
        chan_elec[:, 0] = (chan_ind[:] / 32).astype(int)
        chan_elec[:, 1] = chan_ind[:] - (chan_elec[:, 0] * 32)
        chan_elec = chan_elec.astype(int)

        incom_spike_cnt = np.zeros((32, 32))
        incom_spike_avg = np.zeros((32, 32))
        incom_spike_std = np.zeros((32, 32))
        mask2 = np.copy(data_real)

        for x in range(len(chan_ind)):
            self.graph_data["noise_std"] = self.graph_data["noise_std"]
            incom_spike_cnt[chan_elec[x, 0], chan_elec[x, 1]] = np.count_nonzero(
                mask[chan_elec[x, 0], chan_elec[x, 1], :] >= self.graph_data["noise_mean"][chan_elec[x, 0], chan_elec[x, 1]] + spike_t *
                self.graph_data["noise_std"][chan_elec[x, 0], chan_elec[x, 1]])
            mask2[chan_elec[x, 0], chan_elec[x, 1], mask2[chan_elec[x, 0], chan_elec[x, 1], :] <= self.graph_data["noise_mean"][
                chan_elec[x, 0], chan_elec[x, 1]] + spike_t * self.graph_data["noise_std"][chan_elec[x, 0], chan_elec[x, 1]]] = np.nan

        incom_spike_avg = np.nanmean(mask2, axis=2)
        incom_spike_avg = np.nan_to_num(incom_spike_avg, nan=0)
        incom_spike_std = np.nanstd(mask2, axis=2)
        incom_spike_std = np.nan_to_num(incom_spike_std, nan=0)

        pre_spike_avg = np.copy(self.graph_data["spike_avg"])
        pre_spike_std = np.copy(self.graph_data["spike_std"])
        pre_spike_cnt = np.copy(self.graph_data["spike_cnt"])

        new_spike_cnt = pre_spike_cnt + incom_spike_cnt
        new_spike_cnt[new_spike_cnt == 0] = np.nan

        self.graph_data["spike_avg"] = np.nan_to_num((pre_spike_cnt * pre_spike_avg + incom_spike_cnt * incom_spike_avg) / (new_spike_cnt),
                                  nan=0)
        self.graph_data["spike_std"] = np.sqrt(np.nan_to_num((pre_spike_cnt * (
                    pre_spike_std ** 2 + (pre_spike_avg - self.graph_data["spike_avg"]) ** 2) + incom_spike_cnt * (
                                                       incom_spike_std ** 2 + (incom_spike_avg - self.graph_data["spike_avg"]) ** 2)) / (
                                              new_spike_cnt), nan=0))
        self.graph_data["spike_cnt"] = np.nan_to_num(new_spike_cnt, nan=0)

        # AX1) Colors by Average Electrode Amplitude
        self.graph_data["colors"] = np.copy(self.graph_data["spike_avg"])

        # AX1) Size by Number of Samples
        scale1 = (max_dot - 15) / (np.max(self.graph_data["spike_cnt"]) - np.min(self.graph_data["spike_cnt"][self.graph_data["spike_cnt"]!=0]))
        b_add = max_dot - (np.max(self.graph_data["spike_cnt"]) * scale1)
        self.graph_data["size"] = np.round(self.graph_data["spike_cnt"] * scale1 + b_add)
        self.graph_data["size"][self.graph_data["size"] < 15] = 10

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
        self.graph_data["times"] = np.linspace(0, total_time, N)

