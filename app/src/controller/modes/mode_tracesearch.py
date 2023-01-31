"""
This is the code to start the visualization of the trace search mode, which will be used
to view large amounts of trace data to search for spikes in non-live data.
"""

import math
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

def setup_trace_search(app, CURRENT_THEME, themes, NUM_CHANNELS_PER_BUFFER):
    """

    Args:
        app: MainWindow
        CURRENT_THEME:
        themes:
        NUM_CHANNELS_PER_BUFFER:

    Returns:

    """
    # (1) load the Qt Designer template
    uic.loadUi("./src/view/layouts/TraceSearch.ui", app)

    # (2) set the functions to continually update charts in the GUI
    for i in range(0, 6):
        for j in range(0, 6):
            chart_name = "r" + str(i) + "c" + str(j)
            app.charts[chart_name] = eval("app." + chart_name)

    app.chart_update_function_mapping = {
        "traceSearch": update_trace_search_plots,
        #"channelTraces": update_channel_trace_plot
    }
    app.chart_update_extra_params = {
        "traceSearch": None
    }

    app.CHART_MIN_TIME_TO_REFRESH = {
        "traceSearch": 2
    }

    # (3) Set up additional functionality
    # app.buttons["ResetButton"] = app.resetButton
    # app.buttons["nextFigButton"] = app.nextFigButton
    # app.buttons["yScaleButton"] = app.yScaleButton
    # app.buttons["backButton"] = app.backButton
    # app.buttons["nextButton"] = app.nextButton
    # app.buttons["atTimeWindowButton"] = app.atTimeWindowButton
    app.FigureLabel.setText("Figure: " + str(app.pageNum))
    app.actionIndividualChannelInfo.triggered.connect(app.viewNewIndividualChannelInformation)
    app.actionListElectrodesInfo.triggered.connect(app.viewChannelListInformation)
    app.actionAnalysisParameters.triggered.connect(app.viewGUIPreferences)
    app.actionGUIProfiler.triggered.connect(app.viewGUIProfiler)

    from src.controller.modes.mode_tracesearch import resetSpikeSearchPlotParams, nextPage, backPage, switchTimeZoom, \
        timeStepUp, timeStepDown

    """todo reconnect these
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
    """

    font_color = themes[CURRENT_THEME]["font_color"]
    button_color = themes[CURRENT_THEME]["button"]
    button_style = "color:" + font_color + ";" + \
                   "background-color:" + button_color + ";"
    app.resetButton.setStyleSheet(button_style)
    app.nextButton.setStyleSheet(button_style)
    app.backButton.setStyleSheet(button_style)
    app.timeZoomToggle.setStyleSheet(button_style)
    app.nextTimeStep.setStyleSheet(button_style)
    app.lastTimeStep.setStyleSheet(button_style)

def clearTraceSearchPlots(app):
    """

    Args:
        app: MainWindow

    Returns:

    """
    for chart in app.charts:
        app.charts[chart].clear()

def setupOneSpikeTrace(plot_widget, label: int, CURRENT_THEME: str, themes: dict):
    """function to set up trace plots in the spike search gui

    Args:
        plot_widget: reference to pyqtgraph widget
        label:
        CURRENT_THEME: current GUI theme
        themes: dictionary of theme colors

    Returns:

    """
    color = themes[CURRENT_THEME]["font_color"]
    if label > 1023: label = "####"

    plot_widget.setTitle('Ch #  ' + str(label),
                         color = color,
                         size = '10pt')

    plot_widget.setLabel('bottom', 'time')

def update_trace_search_plots(app, next_packet, CURRENT_THEME: str, themes: dict, extra_params):
    """

    Args:
        app: MainWindow
        next_packet: data contained in next buffer
        CURRENT_THEME: current GUI theme
        themes: dictionary of theme colors
        extra_params:

    Returns:

    """
    # First, clear the plots
    clearTraceSearchPlots(app)

    # Second, set up the plot figures for every electrode on the page
    # TODO make this code work
    for elec in getTracesToPlot(app):
        row, col = electrodeToPlotGrid(app, elec)
        setupOneSpikeTrace(app.charts["r" + str(row) + "c" + str(col)], elec, CURRENT_THEME, themes)

    pen = pg.mkPen(color=themes[CURRENT_THEME]['tracePlotting'])

    """why is this here
    from src.controller.windows.window_individualchannel import IndividualChannelInformation
    individualChannel = IndividualChannelInformation()
    individualChannel.setSessionParent(app)
    """

    # Third, fill in plots with what model you have
    for elec in getTracesToPlot(app):
        individualChannel.current_elec = elec
        individualChannel.updateElectrodeData()

        # The Y range we display is [mean-app.yMin, mean+app.yMax]
        mean = np.nanmean(individualChannel.electrode_data)
        if math.isnan(mean):
            mean = 0
        lowerYBound = mean - int(app.yMin.value())
        upperYBound = mean + int(app.yMax.value())

        # If timeZoom, we want to zoom in on specific time windows of each trace
        if app.timeZoom:
            # The X range we display is based on which time step the user is on
            totalTime = len(individualChannel.electrode_times)
            if totalTime == 0:
                xRange = [0, 0]
            else:
                windowLength = int(totalTime / app.numberOfTimeSteps)
                startIdx = app.timeStep * windowLength
                xRange = [individualChannel.electrode_times[startIdx],
                          individualChannel.electrode_times[startIdx + windowLength - 1]]
            row, col = app.electrodeToPlotGrid(elec)
            gridToPlot = "r" + str(row) + "c" + str(col)
            app.charts[gridToPlot].plot(individualChannel.electrode_times,
                                        individualChannel.electrode_data, pen=pen)
            app.charts[gridToPlot].setYRange(lowerYBound, upperYBound, padding=0)
            app.charts[gridToPlot].setXRange(xRange[0], xRange[1], padding=0)

        # If timeZoom is false, we just want to display the whole trace, not zoomed in portions
        else:
            row, col = app.electrodeToPlotGrid(elec)
            gridToPlot = "r" + str(row) + "c" + str(col)
            app.charts[gridToPlot].plot(individualChannel.electrode_times,
                                         individualChannel.electrode_data, pen=pen)
            app.charts[gridToPlot].setYRange(lowerYBound, upperYBound, padding=0)
            app.charts[gridToPlot].enableAutoRange(axis='x', enable=True)

        # Spike highlighting
        if len(individualChannel.electrode_times) > 25:
            for spike in individualChannel.electrode_spike_times:
                lr = pg.LinearRegionItem([spike - 2, spike + 2])
                lr.setBrush(pg.mkBrush(themes[CURRENT_THEME]["spikeHighlighting"]))
                lr.setZValue(-5)
                app.charts[gridToPlot].addItem(lr)

    def updateElectrodeData(self, debug = False):
        self.electrode_packets.clear()
        self.electrode_spikes.clear()
        self.electrode_spike_times.clear()
        self.electrode_data.clear()
        self.electrode_times.clear()

        match = False

        X, Y = self.session_parent.data.get_last_trace_with_electrode_idx(self.current_elec)

        # TODO hook this data with rest of GUI

        """
        # Create a list of dictionaries of model packets for the selected electrode
        for i in range(len_filtered_data):
            if self.session_parent.LoadedData.filtered_data[i]['channel_idx'] == self.current_elec:
                self.electrode_packets.append(self.session_parent.LoadedData.filtered_data[i])
                match = True
        if debug:
            if not match:
                print("No model from this electrode yet")

        filtered = True
        if self.session_parent.settings["filter"] == "None":
            filtered = False

        # Get lists of times and model from each packet for the selected electrode
        for i in range(len(self.electrode_packets)):
            self.session_parent.LoadedData.\
                calculate_realtime_spike_info_for_channel_in_buffer(self.electrode_packets[i], filtered)
            self.electrode_spikes.extend(self.electrode_packets[i]["spikeBins"])
            self.electrode_spike_times.extend(self.electrode_packets[i]["incom_spike_times"])
            self.electrode_times.extend(self.electrode_packets[i]['times'])
            self.electrode_data.extend(self.electrode_packets[i]['model'])

        self.recordedTime = round((len(self.electrode_data)) * 0.05, 2)
        """
# ================
# HELPER FUNCTIONS
# ================
def electrodeToPlotGrid(app, electrodeNum):
    """

    Args:
        app: MainWindow
        electrodeNum:

    Returns:
        None

    """
    """
    Args:
        electrodeNum: electrode number on RC array (0-1023)

    Returns: row, col (each between 0 and 5) for the 6x6 plot grid

    """
    electrodeNum = electrodeNum - 36 * app.pageNum
    row = int(electrodeNum / 6)
    col = int(electrodeNum - row * 6)
    return row, col

def getTracesToPlot(app):
    """Function to determine which electrodes to plot given what page of spike
    search GUI user is on

    Args:
        app: MainWindow

    Returns:
        36 electrodes #s in a list
    """
    app.tracesToPlot.clear()
    for i in range(36):
        app.tracesToPlot.append(app.pageNum * 36 + i)
        app.FigureLabel.setText("Figure " + str(app.pageNum)
                                 + ": Ch " + str(app.tracesToPlot[0]) + " to Ch " + str(app.tracesToPlot[-1]))
    return app.tracesToPlot

def resetSpikeSearchPlotParams(app):
    """

    Args:
        app: MainWindow

    Returns:
        None
    """
    app.yMax.setValue(20)
    app.yMin.setValue(30)
    app.timeZoom = True
    app.timeStep = 0
    app.update_spike_search_plots()

def switchTimeZoom(app):
    """

    Args:
        app: MainWindow

    Returns:
        None

    """
    app.timeZoom = not app.timeZoom
    app.timeStep = 0
    app.update_spike_search_plots()

def nextPage(app):
    """

    Args:
        app: MainWindow

    Returns:
        None

    """
    if app.pageNum < 28:
        app.pageNum += 1
        app.FigureLabel.setText("Page: " + str(app.pageNum))
        app.timeStep = 0
        app.update_spike_search_plots()

def backPage(app):
    """

    Args:
        app: MainWindow

    Returns:
        None

    """
    if app.pageNum > 0:
        app.pageNum -= 1
        app.FigureLabel.setText("Page: " + str(app.pageNum))
        app.timeStep = 0
        app.update_spike_search_plots()

def timeStepUp(app):
    """

    Args:
        app: MainWindow

    Returns:
        None

    """
    if app.timeStep < app.numberOfTimeSteps - 1:
        app.timeStep += 1
        app.update_spike_search_plots()

def timeStepDown(app):
    """

    Args:
        app: MainWindow

    Returns:
        None

    """
    if app.timeStep > 0:
        app.timeStep -= 1
        app.update_spike_search_plots()
