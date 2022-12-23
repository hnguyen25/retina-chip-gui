"""
Huy Nguyen, John Bailey (2022)
Contains the base app framework for loading up the GUI.
"""

from dc1DataVis.app.src.model.DC1DataContainer import *
from dc1DataVis.app.src.model.python_thread_worker import *  # multithreading
from PyQt5 import QtWidgets
from dc1DataVis.app.src.view.gui_themes import *
import multiprocessing

class MainWindow(QtWidgets.QMainWindow):
    """ Inherited from PyQt main window class. Contains all the functions necessary
    to start and run GUI elements.
    """
    ### PROGRAM VARS ###
    running = True
    is_paused = False
    first_time_plotting = True  # toggles to false when all the charts are setup for the first time
    settings = {}  # session parameters created through user input from the startup pane
    loading_dict = {}  # contains details of the model run currently being analyzed
    LoadedData = None  # contains all neural model loaded from specified model run
    profile_data = {
        'appendRawData': [], 'filterData': [], 'calculateArrayStats': [], 'arrayMap': [],
        'noiseHeatMap': [], 'channelTrace': [], 'noiseHistogram': [], 'spikeRatePlot': [],
        'miniMap': [], 'channelTrace1': [], 'channelTrace2': [], 'channelTrace3': [], 'channelTrace4': []
    }  # contains information about how long different view functions took to run
    charts = {}  # keys=name of every possible chart, value=reference to chart in GUI, None if not in it
    chart_update_function_mapping = {}  # keys=names of charts, value=related functions to update respective charts
    chart_update_extra_params = {}
    external_windows = []  # reference to windows that have been generated outside of this MainWindow
    basedir = None  # base directory of where the program is loaded up, acquired from run.py script

    # list of length DC1DataContainer.settings["simultaneousChannelsRecordedPerPacket"] with model and
    # information to plot every channel in the latest model packet processed
    # list contains a dictionary for every channel, with keys
    # 'x': all times in packet
    # 'y': all electrode amp values in packets, correlated with x
    # 'curr_x': times in current window shown directly in GUI
    # 'curr_y': respective amplitude values of curr_x
    # 'chan_idx': the channel idx being plotted
    trace_channels_info = []

    ### MISCELLANEOUS ###
    pageNum = 0  # used for knowing which traces to display in spike search modes. Zero-indexed
    timeStep = 0  # used for stepping through trace plots in spike search modes. Zero-indexed
    numberOfTimeSteps = 4  # how many segments to divide trace plots into per view in spike search modes
    timeZoom = True  # bool for spike search modes. True if plots display in time steps divided into numberOfTimeSteps,
                     # if false the entire trace displays on spike search
    tracesToPlot = []
    p = None
    array_map_color_bar = None  # reference to the color bar embedded with the array map chart
    noise_heat_map_color_bar = None
    arrayMapHoverCoords = None
    array_map_channels_to_update = []

    #### NEW STRUCTS
    subplot_elements = {}
    def update_subplot_element(self, chart, key, value):
        if key in self.subplot_elements:
            self.charts[chart].removeItem(self.subplot_elements[key])
        self.charts[chart].addItem(value)
        self.subplot_elements[key] = value

    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__()
        if "settings" in kwargs:
            self.settings = kwargs["settings"]
        if "window_title" in kwargs:
            self.setWindowTitle(kwargs["window_title"])
        if "layout" in kwargs:
            self.charts = kwargs["layout"]["charts"]
            self.chart_update_function_mapping = kwargs["layout"]["chart_update_function_mapping"]
            self.buttons = kwargs["layout"]["buttons"]

        # load first buffer so that layout can load properly from start
        self.data = DC1DataContainer(self)
        self.settings["num_channels"] = load_first_buffer_info(self)
        self.data_loading_serialized_loop()

        if not setup_layout(self, self.settings['visStyle'],
                            self.settings["current_theme"], themes,
                            self.settings["num_channels"]):
            print("This layout has not been developed yet! Exiting application...")
            sys.exit()

        charts_list = self.chart_update_function_mapping.keys()
        self.gui_charts_time_counter = {chart: 100 for chart in charts_list}

        profiling_columns = [
            "buffer_idx",
            "gui_refresh",
            "parallelized_loop",
            "serial_loop",
            "array_map",
            "minimap",
            "spike_rate",
            "noise",
            "trace"
        ]

        initial_data = []
        for i in range(300):
            initial_data.append([
                i, -1, -1, -1, -1, -1, -1, -1, -1
            ])

        self.profiling_df = pd.DataFrame(initial_data, columns=profiling_columns)
        self.exec_multithreading()

    last_gui_refresh_time = time.time()
    array_data, latest_buffers, buffer_metadata = None, None, None

    NUM_UNPROCESSED, NUM_PROCESSED, NUM_GUI_QUEUE, NUM_DISPLAYED = 0, 0, 0, 0
    NUM_TOTAL = 0  # should be = NUM_UNPROCESSED + NUM_PROCESSED + NUM_GUI_QUEUE + NUM_DISPLAYED
    threadpool = None
    def exec_multithreading(self):
        print('setup multithreading')

        self.running = True
        # Set up PyQt multithreading
        self.threadpool = QThreadPool()
        if self.settings['is_mode_multithreading']:
            print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        # TODO LOAD FROM BEGINNING vs LOAD FROM END
        """
        if load_from_beginning:
            last_file_idx = 0
        else:
            last_file_idx = loadingDict["num_of_buf"] - 2
        """
        # (1) set up thread for handling the parallelized part of model loading
        data_loading_parallelized_worker = Worker(self.data_loading_parallelized_thread)
        data_loading_parallelized_worker.signals.progress.connect(self.updateStatusBar)
        # TODO GUI refresh loop cannot be a separate worker
        data_loading_parallelized_worker.signals.gui_callback.connect(self.gui_refresh_loop)

        # (2) set up thread for handling the serialized part of model loading
        data_loading_serialized_worker = Worker(self.data_loading_serialized_thread)
        data_loading_serialized_worker.signals.progress.connect(self.updateStatusBar)
        data_loading_serialized_worker.signals.gui_callback.connect(self.gui_refresh_loop)

        # main thread = self.gui_refresh_thread + self.gui_refresh_loop
        # Start all concurrent threads
        self.threadpool.start(data_loading_parallelized_worker)
        self.threadpool.start(data_loading_serialized_worker)

        # start a view refresh loop
        self.timer = QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.setInterval(1000) # in milliseconds
        self.timer.timeout.connect(self.gui_refresh_thread)
        self.timer.start()

    # this is one separate thread running a multiprocessing
    def data_loading_parallelized_thread(self, progress_callback, gui_callback,  NUM_SIMULTANEOUS_PROCESSES=6):
        if self.settings['debug_threads']: print("START: parallel thread")
        pool = multiprocessing.Pool(processes=NUM_SIMULTANEOUS_PROCESSES)

        while self.running is True:
            if self.settings['debug_threads']: print('Thread-Parallel >> Time elapsed', round(time.time() - self.last_gui_refresh_time, 2))

            # update counters
            buf_dir = os.listdir(self.settings["path"])
            self.NUM_TOTAL = len(buf_dir)
            self.NUM_UNPROCESSED = self.NUM_TOTAL - self.NUM_PROCESSED - self.NUM_GUI_QUEUE - self.NUM_DISPLAYED
            self.NUM_PROCESSED = self.data.to_serialize.qsize()
            self.NUM_GUI_QUEUE = self.data.to_show.qsize()

            # run when there isn't enough processed model to display + there is model left to process
            if self.NUM_GUI_QUEUE < 3 and self.NUM_UNPROCESSED > 1:
                num_packets_processed = self.file_loading_parallelized_loop(pool, NUM_SIMULTANEOUS_PROCESSES)
                if num_packets_processed == 0:
                    time.sleep(5)
            else:  # sleep this thread because there's nothing to do
                time.sleep(5)

    def data_loading_serialized_thread(self, progress_callback, gui_callback):
        if self.settings['debug_threads']: print("START: serial thread")
        while self.running is True:
            buf_dir = os.listdir(self.settings["path"])
            self.NUM_TOTAL = len(buf_dir)
            self.NUM_UNPROCESSED = self.NUM_TOTAL - self.NUM_PROCESSED - self.NUM_GUI_QUEUE - self.NUM_DISPLAYED
            self.NUM_PROCESSED = self.data.to_serialize.qsize()
            self.NUM_GUI_QUEUE = self.data.to_show.qsize()

            if self.settings['debug_threads']: print('Thread-Serial >> Time elapsed', round(time.time() - self.last_gui_refresh_time, 2))
            if self.NUM_PROCESSED > 0:
                packet_successfully_added = self.data_loading_serialized_loop()

            else:  # sleep this thread if there's nothing to process
                time.sleep(1)

        #TODO status bar messages
        #status_bar_message = "Waiting... {Piece: " + loadingDict['datapiece'] + ",  Run: " + loadingDict[
        #            'datarun'] + '}' \
        #                         " | Received Packets: " + str(loadingDict['num_of_buf']) + \
        #                             " | Processing Packet #" + str(last_file_idx) + \
        #                             " | Viewing Packet #" + str(last_file_idx)
        #status_bar_message = "Real-Time {Piece: " + loadingDict['datapiece'] + ",  Run: " + loadingDict[
        #    'datarun'] + '}' \
        #                 " | Received Packets: " + str(loadingDict['num_of_buf']) + \
        #                     " | Processing Packet #" + str(last_file_idx) + \
        #                     " | Viewing Packet #" + str(last_file_idx)

    MIN_GUI_REFRESH_INTERVAL = 2
    # this loop is run by a QTimer in MainWindow.exec_multithread
    def gui_refresh_thread(self):

        buf_dir = os.listdir(self.settings["path"])
        self.NUM_TOTAL = len(buf_dir)
        self.NUM_UNPROCESSED = self.NUM_TOTAL - self.NUM_PROCESSED - self.NUM_GUI_QUEUE - self.NUM_DISPLAYED
        self.NUM_PROCESSED = self.data.to_serialize.qsize()
        self.NUM_GUI_QUEUE = self.data.to_show.qsize()
        time_elapsed = round(time.time() - self.last_gui_refresh_time, 2)
        if self.settings['debug_threads']: print('Thread-GUI >> Time elapsed:', time_elapsed)
        if (self.NUM_GUI_QUEUE > 0 and time_elapsed > self.MIN_GUI_REFRESH_INTERVAL) or \
            (self.NUM_GUI_QUEUE > 0 and self.NUM_DISPLAYED == 0):
            #print('refresh view loop')
            self.last_gui_refresh_time = time.time()
            new_packet_displayed = self.gui_refresh_loop()
            if new_packet_displayed:
                self.NUM_DISPLAYED += 1

        split1 = os.path.split(self.settings['path'])
        split2 = os.path.split(split1[0])
        datarun = split2[1] + '/' + split1[1]

        msg = "Viewing packet " + str(self.NUM_DISPLAYED) + "/" + str(self.NUM_TOTAL) + "  (" + str(self.NUM_PROCESSED) \
              + " loaded into memory,  " + str(self.NUM_GUI_QUEUE) + " waiting to be displayed). " +  \
             "From model directory " + datarun + "."
        self.statusBar().showMessage(msg)
        #self.statusBar().showMessage('||TOT' + str(self.NUM_TOTAL) + '|| UNPROC' + str(self.NUM_UNPROCESSED) + ' >> PROC' +
        #      str(self.NUM_PROCESSED) + ' >> GUIQ' + str(self.NUM_GUI_QUEUE) + ' >> DISP' + str(self.NUM_DISPLAYED))

    curr_buf_idx = 0
    def file_loading_parallelized_loop(self, pool, NUM_SIMULTANEOUS_PROCESSES):
        if self.is_paused: return
        # decide how many packets to multiprocess this time
        if self.NUM_UNPROCESSED >= NUM_SIMULTANEOUS_PROCESSES:
            num_packets_to_process = NUM_SIMULTANEOUS_PROCESSES
        else:
            num_packets_to_process = self.NUM_UNPROCESSED

        # generate parameters
        params_to_process = []
        for i in range(num_packets_to_process):
            if self.curr_buf_idx < self.NUM_TOTAL:
                data_run = os.path.basename(self.settings["path"])
                next_file = self.settings["path"] + "/" + data_run + "_" + str(self.curr_buf_idx) + ".mat"

                packet_params = {
                    "file_dir": next_file,
                    "filter_type": self.settings["filter"],
                    "packet_idx": self.curr_buf_idx,
                    "SPIKING_THRESHOLD": self.settings["spikeThreshold"],
                    "BIN_SIZE": self.settings["binSize"]
                }
                params_to_process.append(packet_params)
                self.curr_buf_idx += 1
            else:
                num_packets_to_process = i
                break
        if num_packets_to_process == 0:
            return 0

        # multiprocessing core
        # TODO BUG right now not multiprocessing is faster than multiprocessing
        self.settings["is_mode_multithreading"] = False
        if self.settings["is_mode_multithreading"] is True:
            # create params to put through multiprocessing
            a = time.time()
            for packet in pool.map(load_one_mat_file, params_to_process):
                print("Time elapsed: {}s)".format(int(time.time() - a)))
                self.data.to_serialize.put(packet)

        else:  # if multiprocessing disabled, just serialized (this is useful for debugging)
            for idx, buffer_params in enumerate(params_to_process):
                packet = load_one_mat_file(buffer_params)
                self.data.to_serialize.put(packet)
        return num_packets_to_process

    def data_loading_serialized_loop(self):
        if self.is_paused: return
        next_packet = self.data.to_serialize.get()
        channel_idxs = self.data.append_buf(next_packet)
        return True

    CHART_MIN_TIME_TO_REFRESH = {
        "miniMap": 2,
        "spikeRatePlot": 0.5,
        "noiseHistogram": 2,
        "channelTraces": 1,
        "arrayMap": 4, #4
        "noiseHeatMap": 0.5,
        "spikeSearch": 0.5
    }

    def gui_refresh_loop(self):
        if self.is_paused: return
        next_packet = self.data.to_show.get()

        # TODO implement a force override of chart updating
        for chart in self.chart_update_function_mapping.keys():
            if (time.time() - self.gui_charts_time_counter[chart]) > self.CHART_MIN_TIME_TO_REFRESH[chart]:
                # TODO once you finish adapting array stats, expand to ohter plots
                # run update function for this chart

                if True:
                #if chart == "channelTraces" or chart == "noiseHistogram" or chart == "arrayMap":
                    a = time.time()
                    extra_params = self.chart_update_extra_params[chart]
                    self.chart_update_function_mapping[chart](self, next_packet, self.settings["current_theme"], themes, extra_params)
                    #print('updating chart time', chart, time.time()-a)
                self.gui_charts_time_counter[chart] = time.time()
        return True

    def showArrayLocOnStatusBar(self, x, y):
        """ Given x, y mouse location on a chart -> display on the status bar on the bottom of the GUI

        Args:
            x: x value on window as detected by mouse on hover
            y: y value on window as detected by mouse on hover
        """
        int_x = int(x)
        int_y = int(y)

        self.arrayMapHoverCoords = (int_x, int_y)

    def onArrayMapClick(self, x, y):

        """ Given an x, y coord as clicked on from the array map,
        reset the center of the electrode minimap to that location.

        Args:
            x: x value on window as detected by mouse on click
            y: x value on window as detected by mouse on click
        """

        self.settings['cursor_row'] = np.clip(int(x), 4, 28)
        self.settings['cursor_col'] = np.clip(int(y), 2, 30)

        update_minimap_indicator(self, self.settings["current_theme"], themes)
        # TODO update minimap plot with new model
        #self.update_mini_map_plot()

    def viewNewIndividualChannelInformation(self):
        """ Connected to [View > Individual channel info...]. Opens up a new window containing useful plots
        for analyzing individual channels on DC1. """

        from dc1DataVis.app.src.view.windows.window_individualchannel import IndividualChannelInformation
        new_window = IndividualChannelInformation()
        new_window.label = QLabel("Individual Channel Analysis")
        new_window.setSessionParent(self)
        new_window.show()
        self.external_windows.append(new_window)

    def viewChannelListInformation(self):
        """ Connected to [View > List of electrodes info...]. Opens up a new window containing useful quant model
        for sorting all the electrodes on the array. """
        from dc1DataVis.app.src.view.windows.window_electrodelist import ElectrodeListInformation
        new_window = ElectrodeListInformation()
        new_window.label = QLabel("Electrode List Analysis")
        new_window.setSessionParent(self)
        new_window.show()
        self.external_windows.append(new_window)

    def viewGUIPreferences(self):
        from dc1DataVis.app.src.view.windows.window_sessionparameters import GUIPreferences
        new_window = GUIPreferences()
        new_window.label = QLabel("GUI Preferences")
        new_window.show()
        new_window.exec()
        self.external_windows.append(new_window)

    def viewGUIProfiler(self):
        from dc1DataVis.app.src.view.windows.window_profiler import GUIProfiler
        new_window = GUIProfiler()
        new_window.label = QLabel("GUI Profiler")
        new_window.show()
        new_window.exec()
        self.external_windows.append(new_window)

    def update_theme(self, new_theme):
        print('update_theme()')
        self.settings["current_theme"] = new_theme
        background_color = themes[new_theme]["background_color"]
        background_border = themes[new_theme]["background_borders"]
        self.setStyleSheet("background-color: " + background_border)

        for chart in self.charts.keys():
            chart_type = type(self.charts[chart])
            if str(chart_type) == "<class 'pyqtgraph.widgets.PlotWidget.PlotWidget'>":
                self.charts[chart].setBackground(background_color)
            elif chart_type is list:
                for chart in self.charts[chart]:
                    chart.setBackground(background_color)

        for window in self.external_windows:
            window.setBackground(background_color)

    def toggle_dark_mode(self):
        if self.settings["current_theme"] == "light":
            self.update_theme("dark")
        elif self.settings["current_theme"] == "dark":
            self.update_theme("light")

    def progress_fn(self, n): print("%d%% done" % n)
    def print_output(self, s): print(s)
    def thread_complete(self): print("THREAD COMPLETE!")

    """
    =======================
    MENU BAR // FILE...
    =======================
    """
    def getDataPath(self, file_type : str):
        options = QFileDialog.Options()
        if file_type is None:
            file_path, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()",
                                                      "", "All Files (*)", options=options)
        else:
            file_path, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()",
                                                      "", file_type, options=options)
        if file_path: print(file_path)
        return file_path
    # (1) Yes, load first .mat chunk & (2) Yes, load latest .mat chunk
    def onLoadRealtimeStream(self, load_from_beginning = True):
        self.loading_dict = init_data_loading(self.settings["path"])

        # TODO parallelize loading already saved .mat files
        load_realtime_worker = Worker(self.realtimeLoading, self.settings["path"], self.loading_dict, load_from_beginning)
        load_realtime_worker.signals.progress.connect(self.updateStatusBar)
        load_realtime_worker.signals.gui_callback.connect(self.gui_refresh_loop)
        self.threadpool.start(load_realtime_worker)
    # TODO (3) No, load raw .mat file
    # parallelize this faster

    # TODO (4) No, load pre-processed .npz file

    # TODO (5) No, load filtered .npz file

    # callback from progress signal
    def updateStatusBar(self, message):
        self.statusBar().showMessage(message)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.onArrayMapClick(self.settings['cursor_row'], self.settings['cursor_col']+1)
        if event.key() == Qt.Key_Down:
            self.onArrayMapClick(self.settings['cursor_row'], self.settings['cursor_col']-1)
        if event.key() == Qt.Key_Right:
            self.onArrayMapClick(self.settings['cursor_row']+1, self.settings['cursor_col'])
        if event.key() == Qt.Key_Left:
            self.onArrayMapClick(self.settings['cursor_row']-1, self.settings['cursor_col'])
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QtWidgets.QMessageBox.question(self, 'Message', quit_msg,
                                               QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Ok)
        if reply == QtWidgets.QMessageBox.Ok:
            self.running = False
            event.accept()
        else:
            event.ignore()
    def printProfilingData(self):
        if self.settings['is_mode_profiling']:
            print("------------------------------")
            print("Current profiling statistics:")
            for key in self.profile_data.keys():
                if self.profile_data[key] != []:
                    avg_time = np.round(np.mean(self.profile_data[key]), 3)
                    print(key, avg_time)
            print("------------------------------\n")

    def OnRewind(self):
        print('<<')
        pass

    def OnPlay(self):
        print('play')
        self.is_paused = not self.is_paused
        if self.is_paused is True:
            self.statusBar().showMessage("Paused!")
        else:
            self.statusBar().showMessage("Un-paused!")
        pass

    def OnFastForward(self):
        print('>>')
        pass

