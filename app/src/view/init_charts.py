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

from src.view.plots.array_map import *
from src.view.plots.spike_rate import *
from src.view.plots.mini_map import *
from src.view.plots.noise_histogram import *
from src.view.plots.channel_trace import *
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
    if layout == "Spike Finding": setup_spike_finding(app, CURRENT_THEME, themes, NUM_CHANNELS_PER_BUFFER)
    elif layout == "Trace Search": setup_trace_search(app, CURRENT_THEME, themes, NUM_CHANNELS_PER_BUFFER)
    elif layout == "Noise": setup_noise_plots(app, CURRENT_THEME, themes, NUM_CHANNELS_PER_BUFFER)
    else: return False

    app.update_theme(CURRENT_THEME)

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

def setup_spike_finding(app, CURRENT_THEME, themes, NUM_CHANNELS_PER_BUFFER):
    # (1) load the Qt Designer template
    uic.loadUi("./src/view/layouts/SpikeFinding.ui", app)

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

    app.statusBar().addPermanentWidget(app.RewindButton)
    app.statusBar().addPermanentWidget(app.TogglePlayButton)
    app.statusBar().addPermanentWidget(app.FastForwardButton)

    app.RewindButton.clicked.connect(app.OnRewind)
    app.TogglePlayButton.clicked.connect(app.OnPlay)
    app.FastForwardButton.clicked.connect(app.OnFastForward)

    app.actionUpdateSession.triggered.connect(app.OnNewSession)

def setup_noise_plots(app, CURRENT_THEME, themes, NUM_CHANNELS_PER_BUFFER):
    # (1) load the Qt Designer template
    uic.loadUi("./src/view/layouts/NoiseWindow.ui", app)

    # (2) set the functions to continually update charts in the GUI
    app.charts = {

    }
    app.chart_update_function_mapping = {
        "channelTraces": update_channel_trace_plot,
        "arrayMap": update_array_map_plot,
        "noiseHeatMap": update_noise_heat_map
    }
    app.chart_update_extra_params = {
        "channelTraces": None,
        "arrayMap": None,
        "noiseHeatMap": None
    }

    app.charts["noiseHeatMap"] = app.noiseHeatMap
    app.charts["noiseHistogram"] = app.noiseHistogramPlot

    app.charts["channelTraceVerticalLayout"] = app.channelTraceLayout
    app.charts["channelTraces"] = [app.channelTrace1, app.channelTrace2, app.channelTrace3, app.channelTrace4]

    app.charts["noiseHeatMap"].setTitle("Noise Heat Map", size="12pt")

    setupSpikeTrace(app.charts["channelTraces"], CURRENT_THEME, themes)
    setupNoiseHistogramPlot(app.charts["noiseHistogram"], CURRENT_THEME, themes)

    # (3) Set up additional functionality
    pass


def setup_trace_search(app, CURRENT_THEME, themes, NUM_CHANNELS_PER_BUFFER):
    # (1) load the Qt Designer template
    uic.loadUi("./src/view/layouts/TraceSearch.ui", app)
    from src.view.modes.mode_spikesearch import update_spike_search_plots

    # (2) set the functions to continually update charts in the GUI
    for i in range(0, 6):
        for j in range(0, 6):
            chart_name = "r" + str(i) + "c" + str(j)
            app.charts[chart_name] = eval("app." + chart_name)

    app.chart_update_function_mapping = {
        "spikeSearch": update_spike_search_plots,
        #"channelTraces": update_channel_trace_plot
    }
    app.chart_update_extra_params = {
        "spikeSearch": None
    }

    # (3) Set up additional functionality
    # app.buttons["ResetButton"] = app.resetButton
    # app.buttons["nextFigButton"] = app.nextFigButton
    # app.buttons["yScaleButton"] = app.yScaleButton
    # app.buttons["backButton"] = app.backButton
    # app.buttons["nextButton"] = app.nextButton
    # app.buttons["atTimeWindowButton"] = app.atTimeWindowButton
    app.FigureLabel.setText("Figure: " + str(app.pageNum))




def setup_diagnostic_plots():
    pass
