"""
Contains functions for detecting spikes

Includes Gaussian Mixture Model (GMM) and Thresholding

Huy Nguyen, John Bailey, Maddy Hays (2022)

"""

from ..gui.setup_charts import *
import numpy as np
import math
from sklearn.mixture import GaussianMixture

def findSpikesGMM(electrode_data, channel_idx, debug = False):
    """
    @param electrode_data: Data to apply GMM to
    (i.e. self.electrode_data in individual channels file)

    @param chan_idx: Index of electrode channel

    @param debug: Prints data if True

    @return: spikeMeanGMM, spikeStdGMM, noiseMeanGMM, noiseStdGMM
    """

    spikeMeanGMM = 0
    noiseMeanGMM = 0
    spikeStdGMM = 0
    noiseStdGMM = 0

    # Get data and perform GM
    y = electrode_data
    gmSam = np.reshape(y,(len(y),1))
    gm = GaussianMixture(n_components = 2).fit(gmSam)

    # Get means, weights, st devs
    means = gm.means_.flatten()
    weights = gm.weights_.flatten()
    stanDevs = np.sqrt(gm.covariances_).flatten()

    # Assign means and standard deviations by finding which index
    # represents spikes and which noise (noise should have 0 mean)
    noiseIdx = 0
    spikesIdx = 0
    for i in range(len(means)):
        if means[i] == np.min(np.abs(means)):
            noiseMeanGMM = means[i]
            noiseIdx = i
        else:
            spikeMeanGMM = means[i]
            spikesIdx = i

    spikeStdGMM = stanDevs[spikesIdx]
    noiseStdGMM = stanDevs[noiseIdx]
    if debug:
        print("Channel for GMM: " + str(channel_idx))
        print("spike mean: "  + str(spikeMeanGMM) +
              "| spike std: " + str(spikeStdGMM) +
              "| noise mean: " + str(noiseMeanGMM) +
              "| noise std: " + str(noiseStdGMM))

    return spikeMeanGMM, spikeStdGMM, noiseMeanGMM, noiseStdGMM

def getAboveThresholdActivity(data,
                              channel_noise_mean, channel_noise_std,
                              spiking_threshold):

    below_threshold = channel_noise_mean - (spiking_threshold * channel_noise_std)
    above_threshold_activity = (data <= below_threshold)

    incom_spike_idx = np.argwhere(above_threshold_activity).flatten()
    incom_spike_amplitude = data[incom_spike_idx]
    return incom_spike_idx, incom_spike_amplitude

def binSpikeTimes(buf_recording_len, incom_spike_idx, incom_spike_amps, BIN_SIZE):
    NUM_BINS_IN_BUFFER = math.floor(buf_recording_len / BIN_SIZE)

    # initialize an array of spike bins, with no spikes detected
    spikeBins = np.zeros(NUM_BINS_IN_BUFFER, dtype=bool)
    spikeBinsMaxAmp = np.zeros(NUM_BINS_IN_BUFFER, dtype=float)

    for bin_idx in range(int(buf_recording_len / BIN_SIZE)):
        bin_start = bin_idx * BIN_SIZE
        bin_end = (bin_idx + 1) * BIN_SIZE

        spikes_within_bin = (bin_start <= incom_spike_idx) & (
                    incom_spike_idx < bin_end)

        if np.count_nonzero(spikes_within_bin) != 0:
            spikeBins[bin_idx] = True
            spiking_amps = incom_spike_amps[spikes_within_bin]
            spikeBinsMaxAmp[bin_idx] = np.max(spiking_amps)

    return spikeBins, spikeBinsMaxAmp, NUM_BINS_IN_BUFFER



