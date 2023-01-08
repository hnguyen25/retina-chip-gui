import numpy as np
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
            from src.model.spike_detection import getAboveThresholdActivity, binSpikeTimes
            incom_spike_idx, incom_spike_amplitude = getAboveThresholdActivity(channel_data["filtered_data"],
                                                                               channel_data["stats_noise+mean"],
                                                                               channel_data["stats_noise+std"],
                                                                               SPIKING_THRESHOLD)
            spikeBins, spikeBinsMaxAmp, NUM_BINS_IN_BUFFER = binSpikeTimes(channel_data["stats_buf+recording+len"],
                                                                           incom_spike_idx,
                                                                           incom_spike_amplitude,
                                                                           BIN_SIZE)

            channel_data["stats_spikes+cnt"] = sum(spikeBins)
            channel_data["stats_spikes+avg+amp"] = np.mean(spikeBinsMaxAmp)
            channel_data["stats_spikes+std"] = np.std(spikeBinsMaxAmp)
            channel_data["spike_bins"] = spikeBins
            channel_data["spike_bins_max_amps"] = spikeBinsMaxAmp
            channel_data["stats_num+spike+bins+in+buffer"] = NUM_BINS_IN_BUFFER

    return packet