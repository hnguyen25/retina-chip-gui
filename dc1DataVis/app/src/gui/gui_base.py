"""
Huy Nguyen, John Bailey (2022)
Contains the base app framework for loading up the GUI.

Note: To regenerate gui_layout.py, in terminal do
pyuic5 layout.ui -o gui_layout.py
"""
import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import uic
import pyqtgraph as pg
import random
import matplotlib as plt
import sys, os

from ..data.data_loading import *
from ..data.preprocessing import *
from ..data.filters import *
from ..data.spikeDetection import *
from ..data.DC1DataContainer import *
from ..analysis.PyqtGraphParams import *
from ..gui.worker import *  # multithreading

from ..gui.default_vis import Ui_mainWindow # layout
from ..gui.gui_individualchannel import IndividualChannelInformation
from ..gui.gui_guipreferences import *
from ..gui.gui_charts_helper import *

CURRENT_THEME = 'light'

light_theme_colors = {
    'dark1': '#2E3440',
    'dark2': '#3B4252',
    'dark3': '#434C5E',
    'dark4': '#4C566A',
    'light1': '#ECEFF4',
    'light2': '#E5E9F0', # '#'
    'light3': '#D8DEE9', # '#'
    'blue1': '#5E81AC',
    'blue2': '#81A1C1',
    'blue3': '#88C0D0',
    'blue4': '#8FBCBB',
    'red': '#BF616A',
    'orange': '#D08770',
    'yellow': '#EBCB8B',
    'green': '#A3BE8C',
    'purple': '#B48EAD',
    'spikeHighlighting' : '#FFEF00',
    'tracePlotting' : 'k'
}

dark_theme_colors = {
    'spikeHighlighting' : '#EBCB8B',
    'tracePlotting': '#08F7FE'
}

themes = {
    'light': light_theme_colors,
    'dark': dark_theme_colors
}

class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):
    """ Inherited from PyQt main window class. Contains all the functions necessary
    to start and run GUI elements.
    """
    ### PROGRAM VARS ###
    first_time_plotting = True  # toggles to false when all the charts are setup for the first time
    settings = {}  # session parameters created through user input from the startup pane
    loading_dict = {}  # contains details of the datarun currently being analyzed
    LoadedData = None  # contains all neural data loaded from specified datarun
    profile_data = None  # contains information about how long different gui functions took to run
    charts = {}  # keys=name of every possible chart, value=reference to chart in GUI, None if not in it
    chart_update_function_mapping = {}  # keys=names of charts, value=related functions to update respective charts
    external_windows = []  # reference to windows that have been generated outside of this MainWindow
    basedir = None  # base directory of where the program is loaded up, acquired from run.py script

    # list of length DC1DataContainer.data_processing_settings["simultaneousChannelsRecordedPerPacket"] with data and
    # information to plot every channel in the latest data packet processed
    # list contains a dictionary for every channel, with keys
    # 'x': all times in packet
    # 'y': all electrode amp values in packets, correlated with x
    # 'curr_x': times in current window shown directly in GUI
    # 'curr_y': respective amplitude values of curr_x
    # 'chan_idx': the channel idx being plotted
    trace_channels_info = []

    ### MISCELLANEOUS ###
    pageNum = 0 # used for knowing which traces to display in spike search mode. Zero-indexed
    tracesToPlot = []
    p = None
    arrayMap_colorbar = None  # reference to the colorbar embedded with the array map chart
    noiseHeatMap_colorbar = None
    arrayMapHoverCoords = None

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle('Stanford Artificial Retina Project | Retina Chip v1.0 Experimental Visualization')

        # GUI STATE: contains variables which change over the course of the GUI visualization
        self.gui_state = {
            # different GUI modes
            'is_mode_profiling': False,  # if on, measures how long different aspects of the GUI takes to compute
            'is_mode_multithreading': False,  # if on, enables multiprocessing capability. may be easier to debug if off
            'is_dark_mode': False,  # appearance of GUI background (light vs dark)

            # GUI play/pause
            'first_time_plotting': True,  # indicates if the first packet of data has not been processed yet,
            # (useful to know for setting up PyQtGraph charts)
            'is_live_plotting': True,  # indicates if the program is still continuously reading available data packets
            'is_true_realtime': True, # indicates if the program is continuously reading the LAST available data packet
            'curr_processing_buf_idx' : 0, # the latest buffer that has been processed and put into DC1DataContainer
            'curr_viewing_buf_idx': 0, # the latest buffer that has been added to the GUI chart

            # center of the minimap, this can be set by user on mouse click on the array map
            'cursor_row': 16,
            'cursor_col': 16
        }

        ### WINDOW REFERENCES ###
        self.charts = {
            "arrayMap": None, "noiseHeatMap": None, "miniMap": None, "spikeRatePlot": None, "noiseHistogram": None,
            "channelTraceVerticalLayout": None, "channelTraces": []
        }

        self.chart_update_function_mapping = {
            "miniMap": self.updateMiniMapPlot,
            "spikeRatePlot": self.updateSpikeRatePlot, "noiseHistogram": self.updateNoiseHistogramPlot,
            "channelTrace1": self.updateChannelTracePlot, "arrayMap": self.updateArrayMapPlot,
            "noiseHeatMap": self.updateNoiseHeatMap
        }
        '''old
        self.chart_update_function_mapping = {
            "arrayMap": self.updateArrayMapPlot, "miniMap": self.updateMiniMapPlot,
            "spikeRatePlot": self.updateSpikeRatePlot, "noiseHistogram": self.updateNoiseHistogramPlot,
            "channelTrace1": self.updateChannelTracePlot, "channelTrace2": self.updateChannelTracePlot,
            "channelTrace3": self.updateChannelTracePlot, "channelTrace4": self.updateChannelTracePlot
        }'''

        ### MODES ###
        if self.gui_state['is_mode_profiling']:
            self.profile_data = {
                'appendRawData': [], 'filterData': [], 'calculateArrayStats': [], 'arrayMap': [],
                'noiseHeatMap': [], 'channelTrace': [], 'noiseHistogram': [], 'spikeRatePlot': [],
                'miniMap': [], 'channelTrace1': [], 'channelTrace2': [], 'channelTrace3': [], 'channelTrace4': []
            }
        if self.gui_state['is_mode_multithreading']: print('GUI is multithreading')

    def setSettings(self, settings): self.settings = settings
    def setBaseDir(self, basedir): self.basedir = basedir

    def setupLayout(self):
        """ Runs initial setup to load all the charts and their basic information for a given layout

        Returns:
            Nothing
        """
        print("SESSION SETTINGS | " + str(self.settings))

        # Load layout based on QtDesigner .ui file
        if self.settings["visStyle"] == "Default":
            uic.loadUi("./src/gui/default_vis.ui", self)

            self.RewindButton = QPushButton("⏪")
            self.RewindButton.setToolTip('REWIND plotting to the very first recording')
            self.RewindButton.setStyleSheet("background-color: white")

            self.TogglePlayButton = QPushButton("⏸︎")
            self.TogglePlayButton.setToolTip('PAUSE plotting on the current packet')
            self.TogglePlayButton.setStyleSheet("background-color: white")

            self.FastForwardButton = QPushButton("⏩")
            self.FastForwardButton.setToolTip('FAST FORWARD plotting to the latest processed packet')
            self.FastForwardButton.setStyleSheet("background-color: white")

            self.statusBar().addPermanentWidget(self.RewindButton)
            self.statusBar().addPermanentWidget(self.TogglePlayButton)
            self.statusBar().addPermanentWidget(self.FastForwardButton)

            self.charts["arrayMap"] = self.arrayMap
            setupArrayMap(self.charts["arrayMap"])
            self.charts["arrayMapHover"] = HoverRegion(self.charts["arrayMap"], self.showArrayLocOnStatusBar,
                                                       self.setMiniMapLoc)
            self.charts["miniMap"] = self.miniMap
            setupMiniMapPlot(self.charts["miniMap"])

            self.charts["spikeRatePlot"] = self.spikeRatePlot
            setupSpikeRatePlot(self.charts["spikeRatePlot"])

            self.charts["noiseHistogram"] = self.noiseHistogram
            setupNoiseHistogramPlot(self.charts["noiseHistogram"])

            self.charts["channelTraceVerticalLayout"] = self.channelTraceVerticalLayout
            self.charts["channelTraces"] = [self.channelTrace1, self.channelTrace2, self.channelTrace3, self.channelTrace4]
            self.toggleDarkMode()
            self.toggleDarkMode()
            for plot in self.charts["channelTraces"]:
                plot.scene().sigMouseClicked.connect(self.pausePlotting)

            setupSpikeTrace(self.charts["channelTraces"])

        elif self.settings["visStyle"] == "Spike Search":

            uic.loadUi("./src/gui/spikefinding_vis.ui", self)
            # self.charts["ResetButton"] = self.resetButton
            # self.charts["nextFigButton"] = self.nextFigButton
            # self.charts["yScaleButton"] = self.yScaleButton
            # self.charts["backButton"] = self.backButton
            # self.charts["nextButton"] = self.nextButton
            # self.charts["atTimeWindowButton"] = self.atTimeWindowButton
            self.charts.clear()
            self.FigureLabel.setText("Figure: " + str(self.pageNum))

            CURRENT_THEME = 'light'

            for i in range(0,6):
                for j in range(0,6):
                    chart_name = "r" + str(i) + "c" + str(j)
                    self.charts[chart_name] = eval("self." + chart_name)
            self.toggleDarkMode()
            self.toggleDarkMode()
            self.setupInteractivity()
            self.updateSpikeSearchPlots()

        elif self.settings["visStyle"] == "Noise":
            uic.loadUi("./src/gui/NoiseWindow.ui", self)

            self.charts["noiseHeatMap"] = self.noiseHeatMap
            self.charts["noiseHistogram"] = self.noiseHistogramPlot
            setupNoiseHistogramPlot(self.charts["noiseHistogram"])

            self.charts["channelTraceVerticalLayout"] = self.channelTraceLayout
            self.charts["channelTraces"] = [self.channelTrace1, self.channelTrace2, self.channelTrace3, self.channelTrace4]
            setupSpikeTrace(self.charts["channelTraces"])
            self.charts["noiseHeatMap"].setTitle("Noise Heat Map", size = "12pt")

        else:
            sys.exit()


        # Because we needed to call self.setupInteractivity separately in
        # the case that Spike Search is called, we don't want to call it twice (causes a bug)
        if self.settings["visStyle"] != "Spike Search":
            self.setupInteractivity()

        # for continuously scanning through trace plot data
        self.timer = QtCore.QTimer()
        self.timer.setInterval(25)
        self.timer.timeout.connect(self.continouslyUpdateTracePlotData)
        self.timer.start()



        # just sets background to white TODO make this cleaner
        #self.toggleDarkMode()
        #self.toggleDarkMode()


    def showArrayLocOnStatusBar(self, x, y):
        """ Given x, y mouse location on a chart -> display on the status bar on the bottom of the GUI

        Args:
            x: x value on window as detected by mouse on hover
            y: y value on window as detected by mouse on hover
        """
        int_x = int(x)
        int_y = int(y)

        self.arrayMapHoverCoords = (int_x, int_y)


    def setMiniMapLoc(self, x, y):
        """ Given an x, y coord as clicked on from the array map,
        reset the center of the electrode minimap to that location.

        Args:
            x: x value on window as detected by mouse on click
            y: x value on window as detected by mouse on click
        """
        self.gui_state['cursor_row'] = int(x)
        if self.gui_state['cursor_row'] < 4:
            self.gui_state['cursor_row'] = 4
        elif self.gui_state['cursor_row'] > 26:
            self.gui_state['cursor_row'] = 26

        self.gui_state['cursor_col'] = int(y)
        if self.gui_state['cursor_col'] < 2:
            self.gui_state['cursor_col'] = 2
        elif self.gui_state['cursor_col'] > 29:
            self.gui_state['cursor_col'] = 29


        self.updateMiniMapPlot()
        self.updateArrayMapPlot()


    def setupInteractivity(self):
        """ Connects all the different buttons with their respective actions. Also set up multithreading."""
        self.LoadedData = DC1DataContainer()  # class for holding and manipulating data
        self.LoadedData.setSpikeThreshold(self.settings["spikeThreshold"])
        self.LoadedData.setNumChannels(self.settings["numChannels"])
        # Set up PyQt multithreading
        self.threadpool = QThreadPool()
        if self.gui_state['is_mode_multithreading']:
            print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.actionIndividualChannelInfo.triggered.connect(self.viewNewIndividualChannelInformation)
        self.actionListElectrodesInfo.triggered.connect(self.viewChannelListInformation)
        self.actionAnalysisParameters.triggered.connect(self.viewGUIPreferences)
        if self.settings["visStyle"] == "Spike Search":
            self.resetButton.clicked.connect(self.updateSpikeSearchPlots)
            self.nextButton.clicked.connect(self.nextPage)
            self.backButton.clicked.connect(self.backPage)

    def viewNewIndividualChannelInformation(self):
        """ Connected to [View > Individual channel info...]. Opens up a new window containing useful plots
        for analyzing individual channels on DC1. """

        from ..gui.gui_individualchannel import IndividualChannelInformation
        new_window = IndividualChannelInformation()
        new_window.label = QLabel("Individual Channel Analysis")
        new_window.setSessionParent(self)
        new_window.show()
        self.external_windows.append(new_window)

    def viewChannelListInformation(self):
        """ Connected to [View > List of electrodes info...]. Opens up a new window containing useful quant data
        for sorting all the electrodes on the array. """
        from ..gui.gui_electrodelist import ElectrodeListInformation
        new_window = ElectrodeListInformation()
        new_window.label = QLabel("Electrode List Analysis")
        new_window.setSessionParent(self)
        new_window.show()
        self.external_windows.append(new_window)

    def viewGUIPreferences(self):
        from ..gui.gui_sessionparameters import GUIPreferences
        new_window = GUIPreferences()
        new_window.label = QLabel("GUI Preferences")
        new_window.show()
        new_window.exec()
        self.external_windows.append(new_window)

    def toggleDarkMode(self):
        self.gui_state['is_dark_mode'] = not self.gui_state['is_dark_mode'] # toggle

        if self.gui_state['is_dark_mode'] is True:
            color = 'k'
        else:
            color = 'w'
            self.setStyleSheet("background-color: " + themes[CURRENT_THEME]['light3'])

        for chart in self.charts.keys():
            chart_type = type(self.charts[chart])
            if str(chart_type) == "<class 'pyqtgraph.widgets.PlotWidget.PlotWidget'>":
                self.charts[chart].setBackground(color)
            elif chart_type is list:
                for chart in self.charts[chart]:
                    chart.setBackground(color)

    """
    =======================
    MULTITHREADING PROGRESS FUNCS
    =======================
    """
    def progress_fn(self, n):
        print("%d%% done" % n)

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    """
    =======================
    MENU BAR // FILE...
    =======================
    """
    def getDataPath(self, file_type : str):
        """

        Args:
            file_type:

        Returns:

        """
        options = QFileDialog.Options()
        if file_type is None:
            file_path, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()",
                                                      "", "All Files (*)", options=options)
        else:
            file_path, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()",
                                                      "", file_type, options=options)
        if file_path: print(file_path)
        return file_path


    def loadSession(self):
        print('loadSession()')
        if self.settings["path"] == "":
            raise ValueError("Path is not specified!")
        if self.settings['realTime'] == "Yes, load first .mat chunk":
            self.onLoadRealtimeStream(load_from_beginning=True)
            # update GUI
        elif self.settings['realTime'] == "Yes, load latest .mat chunk":
            self.onLoadRealtimeStream(load_from_beginning=False)
        elif self.settings['realTime'] == "No, load raw .mat file":
            #TODO parallelize
            self.onLoadRealtimeStream(load_from_beginning=True)
        elif self.settings['realTime'] == "No, load pre-processed .npz file":
            #TODO
            self.onActionLoadNPZ()
        elif self.settings['realTime'] == "No, load filtered .npz file":
            #TODO
            self.onActionLoadNPZ()
        else:
            raise ValueError("this should not be possible")

    # (1) Yes, load first .mat chunk & (2) Yes, load latest .mat chunk
    def onLoadRealtimeStream(self, load_from_beginning = True):
        print('onLoadRealtimeStream()')
        self.loading_dict = initDataLoading(self.settings["path"])

        # TODO parallelize loading already saved .mat files
        load_realtime_worker = Worker(self.realtimeLoading, self.settings["path"], self.loading_dict, load_from_beginning)
        load_realtime_worker.signals.progress.connect(self.updateStatusBar)
        load_realtime_worker.signals.gui_callback.connect(self.updateGUIWithNewData)
        self.threadpool.start(load_realtime_worker)

    # TODO (3) No, load raw .mat file
    # parallelize this faster

    # TODO (4) No, load pre-processed .npz file
    def onActionLoadNPZ(self):
        """

        Returns:

        """
        path = self.getDataPath("Numpy files (*.npz)")
        self.loading_dict["path"] = path
        data = loadDataFromFileNpz(path)
        self.updateGUIWithNewData()

    # TODO (5) No, load filtered .npz file

    # callback from progress signal
    def updateStatusBar(self, message):
        self.statusBar().showMessage(message)

    # Continuously Check for New Data
    def realtimeLoading(self, path, loadingDict, load_from_beginning,
                        progress_callback, gui_callback, dataIdentifierString='gmem1'):
        """

        Args:
            path:
            loadingDict:
            progress_callback:
            gui_callback:
            dataIdentifierString:

        Returns:

        """
        print('realtimeLoading()')

        progress_callback.emit("in realtimeloading(): " + path)

        # string parse datarun+datapiece
        split_path = os.path.split(path)
        data_run = split_path[1]
        data_piece = os.path.split(split_path[0])[1]

        if load_from_beginning:
            last_file_idx = 0
        else:
            last_file_idx = loadingDict["num_of_buf"] - 2

        while True:
            # In case multiple files coming in at once, hold 100ms (not likely)
            #     time.sleep(0.1)
            next_file = path + "/" + data_run + "_" + str(last_file_idx+1) + ".mat"

            # If the next numbered file doesn't exist, just wait
            if os.path.exists(next_file) is False:
                status_bar_message = "Waiting... {Piece: " + loadingDict['datapiece'] + ",  Run: " + loadingDict[
                    'datarun'] + '}' \
                                 " | Received Packets: " + str(loadingDict['num_of_buf']) + \
                                     " | Processing Packet #" + str(last_file_idx) + \
                                     " | Viewing Packet #" + str(last_file_idx)
                progress_callback.emit(status_bar_message)
                continue
            else:  # next file does exist, so process it
                last_file_idx += 1 # update idx

                status_bar_message = "Real-Time {Piece: " + loadingDict['datapiece'] + ",  Run: " + loadingDict['datarun'] + '}'\
                                     " | Received Packets: " + str(loadingDict['num_of_buf']) + \
                                     " | Processing Packet #" + str(last_file_idx) + \
                                     " | Viewing Packet #" + str(last_file_idx)

                #progress_callback.emit("Loading latest buffer file idx " + str(last_file_idx))
                progress_callback.emit(status_bar_message)

                # In the off chance the file has been written, but not saved by the TCP socket yet, pause
                time.sleep(0.5)

                # Load Data from this Loop's Buffer file
                mat_contents = sio.loadmat(next_file)
                dataRaw = mat_contents[dataIdentifierString][0][:]

                data_real, cnt_real, N = removeMultipleCounts(dataRaw)

                start = time.time()
                self.LoadedData.update_array_stats(data_real, N)
                end = time.time()
                if self.gui_state['is_mode_profiling']:
                    self.profile_data['calculateArrayStats'] = end - start

                start = time.time()
                self.LoadedData.append_raw_data(data_real, cnt_real, N)
                end = time.time()
                if self.gui_state['is_mode_profiling']:
                    self.profile_data['appendRawData'] = end - start

                start = time.time()
                #self.dataAll, self.cntAll, self.times = processData(loadingDict, dataIdentifierString='gmem1',buffer_num=0)
                #self.numChan, self.chMap, self.chId, self.startIdx, self.findCoors, self.recordedChannels = identify_relevant_channels(self.dataAll)

                self.LoadedData.update_filtered_data(filtType=self.settings["filter"])
                end = time.time()
                if self.gui_state['is_mode_profiling']:
                    self.profile_data['filterData'] = end - start

                # we need to call the main GUI thread to update graphs (can't do with non GUI-thread)
                gui_callback.emit()

    def onActionLoadMAT(self):
        """

        Returns:

        """
        # path = self.getDataPath("MATLAB files (*.mat)")
        path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')

        # init loading dict with path variables
        loadingDict = initDataLoading(path)
        self.loading_dict = loadingDict

        # loading data freezes GUI -> multithread
        if self.gui_state['is_mode_multithreading']:
            worker = Worker(self.loadDataFromFileMat, path, loadingDict)
            #worker.signals.result.connect(self.updateGUIWithNewData)
            self.threadpool.start(worker)

        else:
            self.loadDataFromFileMat(path, loadingDict)

# TODO : when is this next function used?
    def loadDataFromFileMat(self, path, loadingDict):
        """

        Args:
            path:
            loadingDict:

        Returns:

        """
        self.dataAll, self.cntAll, self.times = processData(loadingDict, dataIdentifierString='gmem1',
                                                            buffer_num=0)  # Any other args, kwargs
        print('identify relevant channels...')
        self.numChan, self.chMap, self.chId, self.startIdx, self.findCoors = identify_relevant_channels(
            self.dataAll)
        print('applying filter...')
        self.filtered_data = applyFilterToAllData(self.dataAll, self.numChan, self.chMap, filtType=self.settings["filter"])

        if self.gui_state['is_mode_multithreading'] is False:  # if multi-threaded, then this function is already connected on completion of fn
            self.updateGUIWithNewData()

    '''
    def MainGUILoop(self, REFRESH_RATE=100):
        # REFRESH_RATE in ms

        last_updated_time = time.time()

        while (last_updated_time
    '''

    # def getRC(self, string):
    #     """
    #     Function to extract row and col from string in form "r#c#"
    #     Returns: row and column strings
    #
    #     """
    #     newStr = string.split("c")
    #     row = newStr[0].split("r")[1]
    #     col = newStr[1]
    #     return row, col

    def electrodeToPlotGrid(self, electrodeNum):
        """

        Args:
            electrodeNum: electrode number on RC array (0-1023)

        Returns: row, col (each between 0 and 5) for the 6x6 plot grid

        """
        electrodeNum = electrodeNum - 36 * self.pageNum
        row = int(electrodeNum/6)
        col = int(electrodeNum - row * 6)
        return row, col


    def getTracesToPlot(self):
        """
        Function to determine which electrodes to plot given what page of spike
        search GUI user is on

        Returns: 36 electrodes #s in a list

        """
        self.tracesToPlot.clear()
        for i in range(36):
            self.tracesToPlot.append(self.pageNum * 36 + i)
            self.FigureLabel.setText("Figure " + str(self.pageNum)
                                     + ": Ch " + str(self.tracesToPlot[0]) + " to Ch " + str(self.tracesToPlot[-1]))
        return self.tracesToPlot

    def clearSpikeSearchPlots(self):
        for chart in self.charts:
            self.charts[chart].clear()


    def nextPage(self):
        if self.pageNum < 28:
            self.pageNum += 1
            self.FigureLabel.setText("Page: " + str(self.pageNum))
            self.updateSpikeSearchPlots()

    def backPage(self):
        if self.pageNum > 0:
            self.pageNum -= 1
            self.FigureLabel.setText("Page: " + str(self.pageNum))
            self.updateSpikeSearchPlots()

    def updateSpikeSearchPlots(self):
        """

        Returns:

        """

        # First, clear the plots
        self.clearSpikeSearchPlots()

        # Second, set up the plot figures for every electrode on the page
        for elec in self.getTracesToPlot():
            row, col = self.electrodeToPlotGrid(elec)
            setupOneSpikeTrace(self.charts["r" + str(row) + "c" + str(col)],elec)

        individualChannel = IndividualChannelInformation()
        individualChannel.setSessionParent(self)

        pen = pg.mkPen(color = themes[CURRENT_THEME]['tracePlotting'])
        yMin = -50
        yMax = 20
        # Third, fill in plots with what data you have
        for elec in self.getTracesToPlot():
            individualChannel.current_elec = elec
            individualChannel.updateElectrodeData()
            row, col = self.electrodeToPlotGrid(elec)
            gridToPlot = "r" + str(row) + "c" + str(col)
            self.charts[gridToPlot].plot(individualChannel.electrode_times,
                                        individualChannel.electrode_data, pen = pen)
            self.charts[gridToPlot].setYRange(yMin, yMax, padding = 0)
            if len(individualChannel.electrode_times)>25:
                for spike in individualChannel.electrode_spike_times:
                    lr = pg.LinearRegionItem([spike-2, spike+2])
                    lr.setBrush(pg.mkBrush(themes[CURRENT_THEME]["spikeHighlighting"]))
                    lr.setZValue(-5)
                    self.charts[gridToPlot].addItem(lr)

    def updateGUIWithNewData(self):
        """

        Returns:

        """
        for window in self.external_windows:
            window.update()

        # prioritize processing channel trace plot info first #TODO optimization - this is slightly inefficient

        # if doing spike search, don't use the normal update methods
        if self.settings["visStyle"] == "Spike Search":
            self.updateSpikeSearchPlots()
        else:
            for chart in self.charts.keys():
                chart_type = type(self.charts[chart])
                # then it's the list of channel traces
                if chart_type is list:
                    print(chart)
                    self.updateChannelTracePlot(self.charts[chart])

            for chart in self.charts.keys():
                chart_type = type(self.charts[chart])
                if str(chart_type) == "<class 'pyqtgraph.widgets.PlotWidget.PlotWidget'>":
                    if self.gui_state['is_mode_profiling']:
                        start = time.time()
                    self.chart_update_function_mapping[chart]()
                    if self.gui_state['is_mode_profiling']:
                        end = time.time()
                        self.profile_data[chart].append(end-start)


        if self.gui_state['is_mode_profiling']:
            self.printProfilingData()

    def printProfilingData(self):
        if self.gui_state['is_mode_profiling']:
            print("------------------------------")
            print("Current profiling statistics:")
            for key in self.profile_data.keys():
                if self.profile_data[key] != []:
                    avg_time = np.round(np.mean(self.profile_data[key]), 3)
                    print(key, avg_time)
            print("------------------------------\n")

    def updateArrayMapPlot(self):
        self.charts["arrayMap"].clear()

        if self.arrayMapHoverCoords is not None:
            x, y = self.arrayMapHoverCoords
            if -1 <= x < 31 and 0 <= y < 32:
                import math
                spike_cnt = self.LoadedData.array_stats['spike_cnt'][y][x + 1]
                spike_amp = self.LoadedData.array_stats['spike_avg'][y][x + 1]
                channel_idx = map2idx(y, x)

                tooltip_text = "<html>" + "Electrode Channel #" + str(channel_idx) + "<br>" + \
                               "Row " + str(y) + ", Column " + str(x) + "<br>" + \
                               "Spike Count: " + str(round(spike_cnt)) + "<br>" + \
                               "Spike Amplitude: " + str(round(spike_amp, 3)) + "<\html>"

                self.charts["arrayMap"].setToolTip(str(tooltip_text))

        if self.first_time_plotting is False:
            colors = self.LoadedData.array_stats['spike_avg']
            data = colors.T  # for old pixel-based data

            max_dot = 50
            # AX1) Size by Number of Samples
            spike_cnt = self.LoadedData.array_stats['spike_cnt']
            scale1 = (max_dot - 15) / (np.max(spike_cnt) - np.min(spike_cnt[spike_cnt != 0]))
            b_add = max_dot - (np.max(spike_cnt) * scale1)
            size = np.round(spike_cnt * scale1 + b_add)
            size[size < 15] = 10  # TODO fix saturation point

        else:
            data = None

        cm = pg.colormap.get('plasma', source='matplotlib')
        image = pg.ImageItem(data)
        self.charts["arrayMap"].addItem(image)

        # bound the LinearRegionItem to the plotted data
        self.charts["arrayMapHover"].region.setClipItem(image)

        if self.arrayMap_colorbar is None:
            self.arrayMap_colorbar = self.charts["arrayMap"].addColorBar(image, colorMap=cm, label="Spike Amplitude", values=(0, 150)) #values=(0, np.max(data)))
            self.arrayMap_colorbar.sigLevelsChanged.connect(self.colorBarLevelsChanged)
        else:

            self.arrayMap_colorbar.setImageItem(image)
            #self.charts["arrayMap"]_colorbar.setLevels((0, np.max(data)))

            # Set pxMode=False to allow spots to transform with the view
            scatter = pg.ScatterPlotItem(pxMode=False)

            # creating empty list for spots
            spots = []

            for i in range(32):
                for j in range(32):
                    # creating  spot position which get updated after each iteration
                    # of color which also get updated

                    if self.first_time_plotting is True:
                        spot_dic = {'pos': (i, j), 'size': 0,
                                    'pen': {'color': 'w', 'width': 1},
                                    'brush': pg.intColor(1, 100)}
                    else:
                        color_map = self.arrayMap_colorbar.colorMap()
                        levels = self.arrayMap_colorbar.levels()

                        value = colors[i,j]
                        if value < levels[0]: value = levels[0]
                        elif value > levels[1]: value = levels[1]

                        adjusted_value = (value - levels[0]) / (levels[1] - levels[0])
                        color_indicator = color_map.map(adjusted_value)

                        spot_dic = {'pos': (j, i), 'size': size[i, j] / 60,
                                    'pen': {'color': 'w', 'width': size[i, j] / 60},
                                    'brush': pg.mkColor(color_indicator)}  # TODO fix coloring

                        # used to be 'brush': pg.intColor(color_indicator, 100)
                    # adding spot_dic in the list of spots
                    spots.append(spot_dic)

            self.first_time_plotting = False

            self.charts["arrayMap"].clear()
            scatter.addPoints(spots)  # adding spots to the scatter plot
            self.charts["arrayMap"].addItem(scatter)  # adding scatter plot to the plot window

            # add squares around electrodes currently being recorded from + visualized in spike trace
            scatter2 = pg.ScatterPlotItem(pxMode=False)
            current_recording_electrodes = []
            for i in range(len(self.trace_channels_info)):
                chan_idx = self.trace_channels_info[i]['chan_idx']
                row, col = idx2map(chan_idx)
                spot_dict = {'pos': (col, row), 'size': 1,
                             'pen': {'color': pg.mkColor(themes[CURRENT_THEME]['blue1']), 'width': 3},
                             'brush': QColor(255,0,255,0),
                             'symbol': 's'}
                current_recording_electrodes.append(spot_dict)
            scatter2.addPoints(current_recording_electrodes)
            self.charts["arrayMap"].addItem(scatter2)

            # add a square around electrodes displayed in the minimap
            minimap_square_indicator = pg.QtGui.QGraphicsRectItem(self.gui_state['cursor_row'] - 4.5,
                                                                  self.gui_state['cursor_col'] - 2.5, 8, 4)
            minimap_square_indicator.setPen(pg.mkPen(themes[CURRENT_THEME]['blue3']))
            minimap_square_indicator.setBrush(QColor(255,0,255,0))
            self.charts["arrayMap"].addItem(minimap_square_indicator)


    def colorBarLevelsChanged(self):
        self.charts["arrayMap"].clear()

        colors = self.LoadedData.array_stats['spike_avg']
        data = colors.T # for old pixel-based data

        max_dot = 75
        # AX1) Size by Number of Samples
        spike_cnt = self.LoadedData.array_stats['spike_cnt']
        scale1 = (max_dot - 15) / (np.max(spike_cnt) - np.min(spike_cnt[spike_cnt != 0]))
        b_add = max_dot - (np.max(spike_cnt) * scale1)
        size = np.round(spike_cnt * scale1 + b_add)
        size[size < 15] = 10  # TODO fix saturation point

        # Set pxMode=False to allow spots to transform with the view
        scatter = pg.ScatterPlotItem(pxMode=False)

        # creating empty list for spots
        spots = []

        # color modulated by amplitude
        cmap = plt.cm.get_cmap("jet")

        for i in range(32):
            for j in range(32):
                # creating  spot position which get updated after each iteration
                # of color which also get updated

                if self.first_time_plotting is True:
                    spot_dic = {'pos': (i, j), 'size': random.random() * 0.5 + 0.5,
                                'pen': {'color': 'w', 'width': 2},
                                'brush': pg.intColor(i * 10 + j, 100)}
                else:
                    color_map = self.arrayMap_colorbar.colorMap()
                    levels = self.arrayMap_colorbar.levels()

                    value = colors[i, j]
                    if value < levels[0]:
                        value = levels[0]
                    elif value > levels[1]:
                        value = levels[1]

                    adjusted_value = (value - levels[0]) / (levels[1] - levels[0])
                    color_indicator = color_map.map(adjusted_value)

                    spot_dic = {'pos': (j, i), 'size': size[i, j] / 60,
                                'pen': {'color': 'w', 'width': size[i, j] / 60},
                                'brush': pg.mkColor(color_indicator)}  # TODO fix coloring

                    # used to be 'brush': pg.intColor(color_indicator, 100)

                # adding spot_dic in the list of spots
                spots.append(spot_dic)

        self.charts["arrayMap"].clear()
        scatter.addPoints(spots)  # adding spots to the scatter plot
        self.charts["arrayMap"].addItem(scatter)  # adding scatter plot to the plot window

    def updateNoiseHeatMap(self, debug = True):

        plot = self.charts["noiseHeatMap"]
        plot.clear()

        font = pg.QtGui.QFont()
        font.setPixelSize(20)
        plot.getAxis("bottom").tickFont = font
        plot.getAxis("bottom").setStyle(tickTextOffset=1)

        if self.first_time_plotting is False:
            data = self.LoadedData.array_stats["noise_std"]
            data = data.T
        else:
            data = None


        img = pg.ImageItem(data)
        cm = pg.colormap.get('plasma', source='matplotlib')
        plot.addItem(img)

        if self.noiseHeatMap_colorbar is None:
            self.noiseHeatMap_colorbar = self.charts["noiseHeatMap"].addColorBar(img, colorMap = cm, label = "Noise SD",
                                                                                 values = (0,10))
        else:
            self.noiseHeatMap_colorbar.setImageItem(img)

        self.first_time_plotting = False

        if debug:
            print("Data" + str(data))

    def updateChannelTracePlot(self, trace_plots):
        """
        This function updates the data for the trace plots when a new packet arrives. The plots are updated even faster
        through 'continuouslyUpdateTracePlotData()', which scans through the packet slowly to visualize data as realtime.
        Args:
            trace_plots:

        Returns:
        """
        len_data = len(self.LoadedData.filtered_data)


        self.trace_channels_info = []
        # Generate subplots
        for m, plt in enumerate(trace_plots):

            if m < int(self.settings['numChannels']): #TODO stopgap actually implement num of trace plots for simult recordings
                plt.clear()
                idx_of_channel_order = len_data + (m - int(self.LoadedData.data_processing_settings["simultaneousChannelsRecordedPerPacket"]))

                chan_idx = self.LoadedData.filtered_data[idx_of_channel_order]['channel_idx']
                row, col = idx2map(chan_idx)

                x = self.LoadedData.filtered_data[idx_of_channel_order]['times']
                y = self.LoadedData.filtered_data[idx_of_channel_order]['data']
                noise_mean = self.LoadedData.array_stats['noise_mean'][row, col]
                noise_std = self.LoadedData.array_stats['noise_std'][row, col]

                if noise_std == 0:
                    plt.setAutoVisible(y=True)
                else:
                    plt.setAutoVisible(y=True)

                    #plt.setYRange(- 3 * noise_std, 3 * noise_std, padding=0)

                begin_time = x[0]
                end_time = x[-1]
                tooltip_text = '<html>Trace signal of electrode #' + str(chan_idx) + \
                               '<br>Row ' + str(row) + ', Column ' + str(col) + \
                               '<br>From time ' + str(round(begin_time, 2)) + 's to ' + str(round(end_time, 2)) + \
                               's after this recording started.' + \
                               '<\html>'

                plt.setToolTip(tooltip_text)

                LEN_BUFFER = len(self.LoadedData.filtered_data[idx_of_channel_order]['data'])
                NUM_TIME_IN_WINDOW = 2000
                if NUM_TIME_IN_WINDOW > LEN_BUFFER:
                    NUM_TIME_IN_WINDOW = LEN_BUFFER

                plot_dict = {'linked_plot': plt, 'chan_idx': chan_idx,
                             'x': self.LoadedData.filtered_data[idx_of_channel_order]['times'],
                             'y': self.LoadedData.filtered_data[idx_of_channel_order]['data'], 'len_buffer': LEN_BUFFER,
                             'NUM_TIME_IN_WINDOW': NUM_TIME_IN_WINDOW, 'len_time_in': NUM_TIME_IN_WINDOW,
                             'curr_x': list(x[0:NUM_TIME_IN_WINDOW]), 'curr_y': list(y[0:NUM_TIME_IN_WINDOW]),
                             'noise_mean': self.LoadedData.array_stats['noise_mean'][row, col],
                             'noise_std': self.LoadedData.array_stats['noise_std'][row, col], 'tooltip_text': tooltip_text,
                             'pause': False}

                plot_dict['test'] = plt.plot(plot_dict['curr_x'] , plot_dict['curr_y'],
                                             pen=pg.mkPen(themes[CURRENT_THEME]['blue1']))
                self.trace_channels_info.append(plot_dict)

                plt.setLabel('left', '#' + str(self.LoadedData.filtered_data[idx_of_channel_order]['channel_idx']))
                plt.getAxis("left").setTextPen(themes[CURRENT_THEME]['dark1'])


    def pausePlotting(self):
        # for now, just pause all plots
        for i in range(len(self.trace_channels_info)):
            self.trace_channels_info[i]["pause"] = not self.trace_channels_info[i]["pause"]


    def continouslyUpdateTracePlotData(self):

        # TODO update for traces that are recorded one at a time, but 4 channels per packet
        SPEED = 1

        if len(self.trace_channels_info) > 0:
            NUM_SAMPS_REFRESHED = int(self.trace_channels_info[0]['len_buffer'] * (SPEED / 1000))

            time_in = self.trace_channels_info[0]['len_time_in']
            length_of_buffer = self.trace_channels_info[0]['len_buffer']

            if time_in + NUM_SAMPS_REFRESHED + 1 < length_of_buffer:
                for plot_dict in self.trace_channels_info:
                    plot_dict['len_time_in'] += NUM_SAMPS_REFRESHED
                    refresh_time_begin = plot_dict['len_time_in'] - NUM_SAMPS_REFRESHED
                    refresh_time_end = plot_dict['len_time_in']
                    new_x = plot_dict['x'][refresh_time_begin:refresh_time_end]
                    new_y = plot_dict['y'][refresh_time_begin:refresh_time_end]
                    plot_dict['curr_x'] = np.concatenate([plot_dict['curr_x'][NUM_SAMPS_REFRESHED:], new_x])
                    plot_dict['curr_y'] = np.concatenate([plot_dict['curr_y'][NUM_SAMPS_REFRESHED:], new_y])
                    plot_dict['test'].setData(plot_dict['curr_x'], plot_dict['curr_y'])

    def updateNoiseHistogramPlot(self, debug=True):
        self.charts["noiseHistogram"].clear()
        vals = self.LoadedData.array_stats['noise_std']
        vals = vals[np.nonzero(vals)]

        cm = pg.colormap.get('plasma', source='matplotlib')

        y, x = np.histogram(vals, bins=np.linspace(0, 15, 30))

        colors = cm.getColors()

        scale = (int(len(colors) / 10))

        if debug:
            print(scale)

        for i in range(len(x) - 1):
            bins = [x[i], x[i + 1]]
            values = [y[i]]

            color = int(scale*x[i])

            if color > 255:
                color = 255

            '''
            if debug:
                print(x[i])
                print(color)
            '''

            curve = pg.PlotCurveItem(bins, values, stepMode=True, fillLevel=0,
                                     brush=colors[color])

            self.charts["noiseHistogram"].addItem(curve)

    def updateSpikeRatePlot(self):
        self.charts["spikeRatePlot"].clear()
        if self.LoadedData is not None:
            avg_spike_rate_times = self.LoadedData.array_stats["array spike rate times"]
            x = np.cumsum(avg_spike_rate_times)
            y = self.LoadedData.array_stats["array spike rate"]
            print("x: " + str(x))
            print("y: " + str(y))
            self.charts["spikeRatePlot"].setLimits(xMin=0, yMin=-5, minXRange=5)
            self.charts["spikeRatePlot"].enableAutoRange(axis='x')
            self.charts["spikeRatePlot"].setYRange(0, max(y) + 50, padding=0.1)
            self.charts["spikeRatePlot"].plot(x, y, pen=pg.mkPen(themes[CURRENT_THEME]['blue1'], width=5))

    def updateMiniMapPlot(self):
        self.charts["miniMap"].clear()
        BAR_LENGTH = 4
        MAX_SPIKES = 16 # can't draw every spike or gui will crash -> group spikes together

        for row in range(self.gui_state['cursor_row']-4, self.gui_state['cursor_row']+4):
            for col in range(self.gui_state['cursor_col']-2, self.gui_state['cursor_col']+2):
                if (row > -2) and (col > -2):
                    spike_indicator_base = pg.QtGui.QGraphicsRectItem(row*5, col*5, BAR_LENGTH, 0.2)
                    spike_indicator_base.setPen(pg.mkPen(themes[CURRENT_THEME]['blue1']))
                    spike_indicator_base.setBrush(pg.mkBrush(themes[CURRENT_THEME]['blue1']))

                    elec_idx = str(map2idx(col, row))
                    spike_indicator_text = pg.TextItem(elec_idx,
                                                       'k',
                                                       anchor=(0,0))
                    spike_indicator_text.setPos(row*5, col*5)
                    spike_indicator_text.setParentItem(spike_indicator_base)

                    self.charts["miniMap"].addItem(spike_indicator_base)
                    self.charts["miniMap"].addItem(spike_indicator_text)
                    '''
                    #times = [0, 1, 3, 5, 10, 11, 14]
                    if np.random.random() > 0.5:
                        times = np.random.randint(0, 20, (3,), dtype='int64')
                        for i in times:
                            spike_indicator = pg.QtGui.QGraphicsRectItem(row*5 + i/5, col*5, 0.1, 1.5)
                            spike_indicator.setPen(pg.mkPen((0, 0, 0, 100)))
                            spike_indicator.setBrush(pg.mkBrush((50, 50, 200)))
                            spike_indicator.setParentItem(spike_indicator_base)
                            self.charts["miniMap"].addItem(spike_indicator)
    
                    self.charts["miniMap"].addItem(spike_indicator_base)
                    self.charts["miniMap"].addItem(spike_indicator_text)
                    '''
        LAST_N_BUFFER_DATA = 100
        to_search = self.LoadedData.preprocessed_data[-LAST_N_BUFFER_DATA:]
        spikes_within_view = []
        for data_packet in to_search:
            chan_idx = data_packet['channel_idx']
            c, r = idx2map(chan_idx)
            if (self.gui_state['cursor_row'] - 4 <= r) & (r < self.gui_state['cursor_row'] + 4) & \
                    (self.gui_state['cursor_col'] - 2 <= c) & (c < self.gui_state['cursor_col'] + 2):
                spikes_within_view.append(data_packet)

        for data_packet in spikes_within_view:
            chan_idx = data_packet['channel_idx']
            row, col = idx2map(chan_idx)
            spikeBins = data_packet['spikeBins']
            spikeBinsMaxAmp = data_packet['spikeBinsMaxAmp']
            spikeLocs = np.argwhere(spikeBins == True)

            num_bins = data_packet['num_bins_in_buffer']
            for i in spikeLocs:
                spike_loc_on_vis_bar = (i / num_bins) * BAR_LENGTH
                spike_height_on_vis_bar = spikeBinsMaxAmp[i] / 50
                spike_indicator = pg.QtGui.QGraphicsRectItem(col * 5 + spike_loc_on_vis_bar, row * 5, 0.1, spike_height_on_vis_bar)
                spike_indicator.setPen(pg.mkPen(themes[CURRENT_THEME]['blue1']))
                spike_indicator.setBrush(pg.mkBrush(themes[CURRENT_THEME]['blue1']))
                spike_indicator.setParentItem(spike_indicator_base)
                self.charts["miniMap"].addItem(spike_indicator)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.setMiniMapLoc(self.gui_state['cursor_row'], self.gui_state['cursor_col']+1)
        if event.key() == Qt.Key_Down:
            self.setMiniMapLoc(self.gui_state['cursor_row'], self.gui_state['cursor_col']-1)
        if event.key() == Qt.Key_Right:
            self.setMiniMapLoc(self.gui_state['cursor_row']+1, self.gui_state['cursor_col'])
        if event.key() == Qt.Key_Left:
            self.setMiniMapLoc(self.gui_state['cursor_row']-1, self.gui_state['cursor_col'])

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QtWidgets.QMessageBox.question(self, 'Message', quit_msg,
                                               QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok)
        if reply == QtWidgets.QMessageBox.Ok:
            event.accept()
        else:
            event.ignore()