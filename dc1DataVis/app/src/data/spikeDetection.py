"""
Contains functions for detecting spikes

Includes Gaussian Mixture Model (GMM) and Thresholding

Huy Nguyen, John Bailey, Maddy Hays (2022)

"""
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import uic
import pyqtgraph as pg
import random
import matplotlib as plt
import sys, os

from ..data.data_loading import *
from ..data.preprocessing import *
from ..data.filters import *
from ..data.DC1DataContainer import *
from ..analysis.PyqtGraphParams import *
from ..gui.worker import *  # multithreading

from ..gui.default_vis import Ui_mainWindow # layout
from ..gui.gui_guipreferences import *
from ..gui.gui_charts_helper import *

from sklearn.mixture import GaussianMixture


spikeMeanGMM = 0
noiseMeanGMM = 0
spikeStdGMM = 0
noiseStdGMM = 0

def findSpikesGMM(filtered_data, chan_idx):
    """
    @param filtered_data: Data to apply GMM to
    (self.LoadedData.filtered_data in gui_base.py)
    @param chan_idx: Index of electrode channel
    @return: spikeMeanGMM, spikeStdGMM, noiseMeanGMM, noiseStdGMM
    """

    # Get data and perform GM
    y = filtered_data[chan_idx]['data']
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

    return spikeMeanGMM, spikeStdGMM, noiseMeanGMM, noiseStdGMM







