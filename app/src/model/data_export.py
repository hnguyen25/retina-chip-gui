"""
Functions to save processed data to a folder for later preprocessing
"""
import pickle
import os
import numpy as np

def export_packet_data(processed_data_folder_dir, run_name, packet,
                       include_times=True,
                       include_unfiltered=True,
                       include_filtered=True,
                       include_spikes=True,
                       include_stats=True):
    packet_idx = packet["packet_idx"]
    filter_type = packet["filter_type"]

    packet_folder_name = "packet" + str(packet_idx)
    folder_dir = processed_data_folder_dir + "/" + run_name + "/" + packet_folder_name
    if not os.path.exists(folder_dir):
        os.makedirs(folder_dir)

    for i in range(len(packet["packet_data"])):
        channel_data = packet["packet_data"][i]
        channel_idx = channel_data["channel_idx"]
        save_filename_prefix = folder_dir + "/" + "packet" + str(packet_idx) + "_p" + str(channel_idx)

        if include_times:
            save_filename_times = save_filename_prefix + "_times" + ".npy"
            np.save(save_filename_times, channel_data["times"])
        if include_unfiltered:
            save_filename_unfiltered = save_filename_prefix + "_unfiltered" + ".npy"
            np.save(save_filename_unfiltered, channel_data["preprocessed_data"])
        if include_filtered:
            save_filename_filtered = save_filename_prefix + "_f+" + filter_type.replace(" ", "") + ".npy"
            np.save(save_filename_filtered, channel_data["filtered_data"])
        if include_spikes:
            save_filename_spikes = save_filename_prefix + "_spikes" + ".pkl"
            spikes_dict = {
                'spike_bins': channel_data['spike_bins'],
                'spike_bins_max_amps': channel_data['spike_bins_max_amps'],
                'spikes+cnt': channel_data['stats_spikes+cnt'],
                'spikes+avg+amp': channel_data['stats_spikes+avg+amp'],
                'spikes+std': channel_data['stats_spikes+std']
            }
            with open(save_filename_spikes, 'wb') as file:
                pickle.dump(spikes_dict, file, protocol=pickle.HIGHEST_PROTOCOL)

        if include_stats:
            save_filename_stats = save_filename_prefix + "_stats" + ".pkl"
            stats_dict = {
                "N": channel_data["N"],
                "channel_idx": channel_data["channel_idx"],
                'avg+unfiltered+amp': channel_data['stats_avg+unfiltered+amp'],
                'cnt': channel_data['stats_cnt'],
                'noise+mean': channel_data['stats_noise+mean'],
                'noise+std': channel_data['stats_noise+std'],
                'buf+recording+len': channel_data['stats_buf+recording+len'],
                'spikes+cnt': channel_data['stats_spikes+cnt'],
                'spikes+avg+amp': channel_data['stats_spikes+avg+amp'],
                'spikes+std': channel_data['stats_spikes+std'],
                'num+spike+bins+in+buffer': channel_data['stats_num+spike+bins+in+buffer']
            }
            with open(save_filename_stats, 'wb') as file:
                pickle.dump(stats_dict, file, protocol=pickle.HIGHEST_PROTOCOL)

def save_stats_to_csv(processed_data_folder_dir, run_name, df):
    fp = processed_data_folder_dir + "/" + run_name + ".csv"
