"""
init_charts
Huy Nguyen (Nov 2022)
----------------
This is boilerplate code for the initial setup of the GUI plots, once a specific type of plot has been chosen.
Note that chart-specific update logic within each type of plot is specified in its own corresponding file.

For instance:
For spike rate plots, refer to python file such as view > plot > spike_rate.py

Contains one main function setup_layout, and a supporting function for each type of GUI layout, i.e.
(1) Spike Finding - a combination of different plots
(2) Noise - only electrode noise related plots
(3) Spike Search - only channel trace plots
(4) Diagnostic (not developed yet)
"""

from src.controller.plots.array_map import *
from src.controller.plots.spike_rate import *
from src.controller.plots.mini_map import *
from src.controller.plots.noise_histogram import *
from src.controller.plots.channel_trace import *
from src.view.gui_themes import *
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWidgets import *
import os
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pandas as pd
from natsort import natsorted, index_natsorted, order_by_index

def setup_layout(app, layout: str, CURRENT_THEME: str, themes: dict, NUM_CHANNELS_PER_BUFFER: int):
    """ Runs initial setup to load all the charts and their basic information for a given layout
    (i.e. Spike Finding, Trace Search, Noise, etc.)

    Args:
        app: reference to the MainWindow container
        layout: name of window type (list specified by SessionStartupGUI.settings["visStyle"])
        CURRENT_THEME:
        themes:

    Returns:
        (bool) whether set up was successful
        (int) NUM_CHANNELS_PER_BUFFER:
    """
    app.buttons = {}

    # Load layout based on QtDesigner .ui file
    if layout == "Spike Finding":
        from src.view.modes.mode_spikefinding import setup_spike_finding
        setup_spike_finding(app, CURRENT_THEME, themes, NUM_CHANNELS_PER_BUFFER)

    elif layout == "Trace Search":
        from src.view.modes.mode_tracesearch import setup_trace_search
        setup_trace_search(app, CURRENT_THEME, themes, NUM_CHANNELS_PER_BUFFER)

    elif layout == "Noise":
        from src.view.modes.mode_noise import setup_noise_plots
        setup_noise_plots(app, CURRENT_THEME, themes, NUM_CHANNELS_PER_BUFFER)

    else: return False
    update_theme(app, CURRENT_THEME)

    # Because we needed to call app.setupInteractivity separately in
    # the case that Spike Search is called, we don't want to call it twice (causes a bug)
    if app.settings["visStyle"] != "Spike Search":
        """ Connects all the different buttons with their respective actions. Also set up multithreading."""

        app.actionIndividualChannelInfo.triggered.connect(app.viewNewIndividualChannelInformation)
        app.actionListElectrodesInfo.triggered.connect(app.viewChannelListInformation)
        app.actionAnalysisParameters.triggered.connect(app.viewGUIPreferences)
        app.actionGUIProfiler.triggered.connect(app.viewGUIProfiler)

        # TODO what is this? app.actionGUIProfiler.triggered.connect(app.viewGUIProfiler)
        if app.settings["visStyle"] == "Spike Search":
            app.resetButton.clicked.connect(app.resetSpikeSearchPlotParams)
            app.nextButton.clicked.connect(app.nextPage)
            app.backButton.clicked.connect(app.backPage)
            app.timeZoomToggle.clicked.connect(app.switchTimeZoom)
            app.nextTimeStep.clicked.connect(app.timeStepUp)
            app.lastTimeStep.clicked.connect(app.timeStepDown)
            app.yMin.valueChanged.connect(app.update_spike_search_plots)
            app.yMax.valueChanged.connect(app.update_spike_search_plots)
            app.yMax.setValue(20)
            app.yMin.setValue(30)  # note: pyqt spin boxes don't support negative values (for some reason)
            # so yMin is the distance below the mean we display
    return True