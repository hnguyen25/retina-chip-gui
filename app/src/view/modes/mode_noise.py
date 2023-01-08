from src.controller.plots.array_map import *
from src.controller.plots.spike_rate import *
from src.controller.plots.mini_map import *
from src.controller.plots.noise_histogram import *
from src.controller.plots.channel_trace import *
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