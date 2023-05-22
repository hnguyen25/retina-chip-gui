"""
This is the code to start the visualization of the compression mode, which will be used
to view compressed spike traces.
"""

from src.controller.plots.array_map import *
from src.controller.plots.spike_rate import *
from src.controller.plots.mini_map import *
from src.controller.plots.noise_histogram import *
from src.controller.plots.realtime_channel_trace import *

from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PyQt5.QtWidgets import *

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from natsort import natsorted, index_natsorted, order_by_index
import pandas as pd
import numpy as np
import pyqtgraph as pg
import os

def setup_compression(app, CURRENT_THEME, themes, NUM_CHANNELS_PER_BUFFER):
    """

    Args:
        app:
        CURRENT_THEME:
        themes:
        NUM_CHANNELS_PER_BUFFER:

    Returns:

    """
    # (1) load the Qt Designer template
    uic.loadUi("./src/view/layouts/Compression.ui", app)

    # (2) set the functions to continually update charts in the GUI

    # We need to define each trace plot individually.
    # Notes: channelTracesGrid is a QGridLayout, top-left of grid layout is (0,0)
    if NUM_CHANNELS_PER_BUFFER < 8:
        channel_traces = [pg.PlotWidget() for _ in range(NUM_CHANNELS_PER_BUFFER)]
        for i in range(NUM_CHANNELS_PER_BUFFER):
            app.channelTracesGrid.addWidget(channel_traces[i], i, 0)

    else:
        channel_traces = [pg.PlotWidget() for _ in range(8)]
        for i in range(4):
            app.channelTracesGrid.addWidget(channel_traces[i], i, 0)
            app.channelTracesGrid.addWidget(channel_traces[i+4], i, 1)

    """
    # add a signal function for mouse click
    for i in range(NUM_CHANNELS_PER_BUFFER):
        # https://stackoverflow.com/questions/58526980/how-to-connect-mouse-clicked-signal-to-pyqtgraph-plot-widget
        from app.src.controller.input_mouse import pause_trace_updating
        print('updating signal function', i)
        # TODO Bug -> all the buttons when clicked only trigger the last trace plot
        channel_traces[i].scene().sigMouseClicked.connect(lambda: pause_trace_updating(channel_traces[i], i))
    """


    app.charts = {
        "arrayMap": app.arrayMap,
        "miniMap": app.miniMap,
        "spikeRatePlot": app.spikeRatePlot,
        "noiseHistogram": app.noiseHistogram,
        "channelTraces": channel_traces,
        "channelTracesLayout": app.channelTracesGrid
    }
    app.chart_update_function_mapping = {
        "miniMap": update_mini_map_plot,
        "spikeRatePlot": update_spike_rate_plot,
        "noiseHistogram": update_noise_histogram_plot,
        "channelTraces": update_channel_trace_plot,
        "arrayMap": update_array_map_plot
    }
    app.chart_update_extra_params = {
        "miniMap": None,
        "spikeRatePlot": None,
        "noiseHistogram": None,
        "channelTraces": channel_traces,  # should be trace plots
        "arrayMap": None,
        "noiseHeatMap": None,
    }

    app.CHART_MIN_TIME_TO_REFRESH = {
        "miniMap": 2,
        "spikeRatePlot": 0.5,
        "noiseHistogram": 2,
        "channelTraces": 1,
        "arrayMap": 4,  # 4
        "noiseHeatMap": 0.5,
        "spikeSearch": 0.5
    }


    setupArrayMap(app, app.charts["arrayMap"], CURRENT_THEME, themes)
    setupMiniMapPlot(app, app.charts["miniMap"], CURRENT_THEME, themes)
    setupSpikeRatePlot(app.charts["spikeRatePlot"], CURRENT_THEME, themes)
    setupNoiseHistogramPlot(app.charts["noiseHistogram"], CURRENT_THEME, themes)
    setupSpikeTrace(app.charts["channelTraces"], CURRENT_THEME, themes)

    # (3) Set up additional functionality
    app.charts["arrayMapHover"] = HoverRegion(app.charts["arrayMap"], app.showArrayLocOnStatusBar,
                                              app.onArrayMapClick)
    app.RewindButton = QPushButton("⏪")
    app.RewindButton.setToolTip('REWIND plotting to the very first recording')
    app.RewindButton.setStyleSheet("background-color: " + themes[CURRENT_THEME]['background_borders'])

    app.TogglePlayButton = QPushButton("⏸︎")
    app.TogglePlayButton.setToolTip('PAUSE plotting on the current packet')
    app.TogglePlayButton.setStyleSheet("background-color: " + themes[CURRENT_THEME]['background_borders'])

    app.FastForwardButton = QPushButton("⏩")
    app.FastForwardButton.setToolTip('FAST FORWARD plotting to the latest processed packet')
    app.FastForwardButton.setStyleSheet("background-color: " + themes[CURRENT_THEME]['background_borders'])

    # app.ModeButton = QPushButton("Summary vs. Real-Time")
    # app.ModeButton.setToolTip('Toggle between summary and real-time viewing.')
    # app.ModeButton.setStyleSheet("background-color: white")

    app.statusBar().addPermanentWidget(app.RewindButton)
    app.statusBar().addPermanentWidget(app.TogglePlayButton)
    app.statusBar().addPermanentWidget(app.FastForwardButton)

    # app.modeButton.clicked.connect(ChangeMode)
    # app.statusBar().addPermanentWidget(app.ModeButton)

    from src.controller.modes.mode_compression import OnRewind, OnPlay, OnFastForward #, ChangeMode
    app.RewindButton.clicked.connect(OnRewind)
    app.TogglePlayButton.clicked.connect(OnPlay)
    app.FastForwardButton.clicked.connect(OnFastForward)
    app.ModeButton.clicked.connect(ChangeMode)

    app.actionUpdateSession.triggered.connect(app.OnNewSession)

def OnRewind(app):
    """

    Args:
        app:

    Returns:

    """
    print('<<')
    pass

def OnPlay(app):
    """

    Args:
        app:

    Returns:

    """
    print('play')
    app.is_paused = not app.is_paused
    if app.is_paused is True:
        app.statusBar().showMessage("Paused!")
    else:
        app.statusBar().showMessage("Un-paused!")
    pass

def OnFastForward(app):
    """

    Args:
        app:

    Returns:

    """
    print('>>')
    pass

def ChangeMode(app):
    """
    """
    print("Compression")
    app.modeButton.setText("Real-Time")
    # print(app.modeButton.text())
    # app.modeButton.setText("Real-Time") if app.modeButton.text() == "Compression" else app.modeButton.setText("Compression-Time")
    pass