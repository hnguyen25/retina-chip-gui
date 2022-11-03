from PyQt5.QtWidgets import QPushButton
import PyQt5.uic as uic
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import os, sys

from pyqtgraph import PlotWidget

from dc1DataVis.app.src.gui.plot_arraymap import *
from dc1DataVis.app.src.gui.plot_spikerate import *
from dc1DataVis.app.src.gui.spike_search import *
from dc1DataVis.app.src.gui.plot_noise import *
from dc1DataVis.app.src.gui.plot_minimap import *
from dc1DataVis.app.src.gui.plot_noise import *
from dc1DataVis.app.src.gui.plot_traces import *

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
    """
    app.buttons = {}

    # Load layout based on QtDesigner .ui file
    if layout == "Spike Finding": setup_spike_finding(app, CURRENT_THEME, themes, NUM_CHANNELS_PER_BUFFER)
    elif layout == "Trace Search": setup_trace_search(app, CURRENT_THEME, themes)
    elif layout == "Noise": setup_noise_plots(app)
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
    uic.loadUi("./src/layouts/SpikeFinding.ui", app)

    # channelTracesGrid is a QGridLayout
    # note: top-left of grid layout is (0,0)
    if NUM_CHANNELS_PER_BUFFER < 8:
        channel_traces = [PlotWidget() for _ in range(NUM_CHANNELS_PER_BUFFER)]
        for i in range(NUM_CHANNELS_PER_BUFFER):
            app.channelTracesGrid.addWidget(channel_traces[i], i, 0)
    else:
        channel_traces = [PlotWidget() for _ in range(8)]
        for i in range(4):
            app.channelTracesGrid.addWidget(channel_traces[i], i, 0)
            app.channelTracesGrid.addWidget(channel_traces[i+4], i, 1)

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
        "noiseHeatMap": None
    }

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

    app.charts["arrayMapHover"] = HoverRegion(app.charts["arrayMap"], app.showArrayLocOnStatusBar,
                                              app.setMiniMapLoc)
    setupArrayMap(app, app.charts["arrayMap"], CURRENT_THEME, themes)
    setupMiniMapPlot(app, app.charts["miniMap"], CURRENT_THEME, themes)
    setupSpikeRatePlot(app.charts["spikeRatePlot"], CURRENT_THEME, themes)
    setupNoiseHistogramPlot(app.charts["noiseHistogram"], CURRENT_THEME, themes)
    setupSpikeTrace(app.charts["channelTraces"], CURRENT_THEME, themes)

def setup_trace_search(app):
    uic.loadUi("./src/layouts/TraceSearch.ui", app)

    app.chart_update_function_mapping = {
        "miniMap": update_mini_map_plot,
        "spikeRatePlot": update_spike_rate_plot,
        "noiseHistogram": update_noise_histogram_plot,
        "channelTraces": update_channel_trace_plot,
        "arrayMap": update_array_map_plot,
        "noiseHeatMap": update_noise_heat_map
    }

    # app.buttons["ResetButton"] = app.resetButton
    # app.buttons["nextFigButton"] = app.nextFigButton
    # app.buttons["yScaleButton"] = app.yScaleButton
    # app.buttons["backButton"] = app.backButton
    # app.buttons["nextButton"] = app.nextButton
    # app.buttons["atTimeWindowButton"] = app.atTimeWindowButton

    app.charts.clear()
    app.FigureLabel.setText("Figure: " + str(app.pageNum))
    CURRENT_THEME = 'light'

    for i in range(0, 6):
        for j in range(0, 6):
            chart_name = "r" + str(i) + "c" + str(j)
            app.charts[chart_name] = eval("app." + chart_name)

    app.update_spike_search_plots()

def setup_noise_plots(app ):
    app.chart_update_function_mapping = {
        "miniMap": app.update_mini_map_plot,
        "spikeRatePlot": app.update_spike_rate_plot, "noiseHistogram": app.update_noise_histogram_plot,
        "channelTraces": app.update_channel_trace_plot, "arrayMap": app.update_array_map_plot,
        "noiseHeatMap": app.update_noise_heat_map
    }

    uic.loadUi("./src/gui/NoiseWindow.ui", app)

    app.charts["noiseHeatMap"] = app.noiseHeatMap
    app.charts["noiseHistogram"] = app.noiseHistogramPlot
    setupNoiseHistogramPlot(app.charts["noiseHistogram"])

    app.charts["channelTraceVerticalLayout"] = app.channelTraceLayout
    app.charts["channelTraces"] = [app.channelTrace1, app.channelTrace2, app.channelTrace3, app.channelTrace4]
    setupSpikeTrace(app.charts["channelTraces"])
    app.charts["noiseHeatMap"].setTitle("Noise Heat Map", size="12pt")

def setup_diagnostic_plots():
    pass



def map2idx(ch_row: int, ch_col: int):
    """ Given a channel's row and col, return channel's index

    Args:
        ch_row: row index of channel in array (up to 32)
        ch_col: column index of channel in array (up to 32)

    Returns: numerical index of array
    """
    if ch_row > 31 or ch_row <0:
        print('Row out of range')
    elif ch_col >31 or ch_col<0:
        print('Col out of range')
    else:
        ch_idx = int(ch_row*32 + ch_col)
    return ch_idx

