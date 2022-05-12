"""
Huy Nguyen (2022)
Contains the base app framework for loading up the GUI.

Note: To regenerate gui_layout.py, in terminal do
pyuic5 layout.ui -o gui_layout.py
"""
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import uic
import pyqtgraph as pg
import random
import matplotlib as plt

from ..data.data_loading import *
from ..data.preprocessing import *
from ..data.filters import *
from ..data.DC1DataContainer import *
from ..analysis.PyqtGraphParams import *
from ..gui.worker import *  # multithreading

from ..gui.default_vis import Ui_mainWindow # layout
from ..gui.gui_guipreferences import *

class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):
    """ Inherited from PyQt main window class. Contains all the functions necessary
    to start and run GUI elements.
    """
    # Settings
    settings = {

    }

    # MODES
    mode_profiling = True
    mode_multithreading = True
    first_time_plotting = True
    is_dark_mode = False
    # GUI GRAPHS
    win1, win2, win3, win4 = None, None, None, None

    # ==== DATA PARAMETERS ====
    graph_params = None

    # ==== DATA CONTAINERS ====
    # Raw data stream from chip, only double/triple/etc. counts removed
    LoadedData = None

    # TODO reconsolidate into new data containers
    data = None
    dataAll, cntAll, times = None, None, None
    numChan, chMap, chId, startIdx, findCoors = None, None, None, None, None
    filtered_data = None
    loading_dict = None
    p = None
    window_update_counter = 0
    profile_data = None

    bar1=None
    bar2=None

    #crosshair
    region = None
    vLine, hLine = None, None
    vb = None
    proxy = None

    win1_colorbar = None

    def __init__(self, *args, **kwargs):
        # old way
        #super().__init__(*args, **kwargs)
        # Load layout based on QtDesigner .ui file
        #uic.loadUi("./src/gui/default-vis.ui", self)

        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        gui_preferences = GUIPreferences()
        gui_preferences.exec()


        # ======================
        # DEBUGGING (tests + profiling)
        # =====================
        self.graph_params = PyqtGraphParams({})

        if self.mode_profiling:
            print('GUI is in profiling mode')
            self.profile_data = {
                'append raw data': [],
                'filter data': [],
                'calculate array stats': [],
                'array map': [],
                'spike trace': [],
                'noise histogram': [],
                'spike rate': []
            }

        if self.mode_multithreading:
            print('GUI is multithreading')

        # =====================
        # FRONT END (GUI layout + design)
        # =====================

        #self.openSessionParams()

        # TODO make window system more flexible+modular
        # top left window = Array Map
        self.win1 = self.arrayMap
        self.win1.setBackground('w')
        self.win1.showGrid(x=True, y=True, alpha=0)
        self.win1.setXRange(-10, 40, padding=0)
        self.win1.setAspectLocked()
        self.win1.setLimits(xMin=-10, xMax=45, yMin=-5, yMax=37)
        self.win1.setLabel('top', "Spike Amplitude")
        self.win1.setLabel('left', "Electrode No. (vertical)")
        self.win1.setLabel('bottom', "Electrode No. (horizontal)")

        # top right = Trace Search
        self.win2 = self.traceplot_verticalLayout
        self.traceplot_1.setBackground('w')
        self.traceplot_2.setBackground('w')
        self.traceplot_3.setBackground('w')
        self.traceplot_4.setBackground('w')
        self.traceplot_1.setLabel('left', "# XXX")
        self.traceplot_2.setLabel('left', "# XXX")
        self.traceplot_3.setLabel('left', "# XXX")
        self.traceplot_4.setLabel('left', "# XXX")

        # bottom left = Spike Rate Plot
        self.win3 = self.spikeRatePlot
        self.win3.setLabel('top', "Noise")
        self.win3.setLabel('left', "Count")
        self.win3.setLabel('bottom', "Standard Dev")
        self.win3.setLimits(xMin=0, yMin=0)
        self.win3.setBackground('w')

        # bottom right window = Array Map
        self.win4 = self.miniMapWidget
        self.win4.setBackground('w')
        self.win4.showGrid(x=True, y=True, alpha=0)
        self.win4.setXRange(-10, 40, padding=0)
        self.win4.setAspectLocked()
        self.win4.setLimits(xMin=-10, xMax=45, yMin=-5, yMax=37)
        self.win4.setLabel('top', "Spike Cnt")
        self.win4.setLabel('left', "Electrode No. (vertical)")
        self.win4.setLabel('bottom', "Electrode No. (horizontal)")

        # init debug plot
        ## make interesting distribution of values
        vals = np.hstack([np.random.normal(size=500), np.random.normal(size=260, loc=4)])

        ## compute standard histogram
        y, x = np.histogram(vals, bins=np.linspace(-3, 8, 40))

        ## notice that len(x) == len(y)+1
        ## We are required to use stepMode=True so that PlotCurveItem will interpret this data correctly.
        curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
        self.win3.addItem(curve)

        # bottom right - Spike Rate Plot // MiniMap Widget -> in development
        # ======================
        # BACKEND (multithreading + interactivity)
        # =====================

        self.LoadedData = DC1DataContainer()  # class for holding and manipulating data

        # Set up PyQt multithreading
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        # >>>> MENU BAR <<<<<
        # TODO hook up interactivity for all menu bar buttons
        # >> FILE BUTTON
        self.action_npz.triggered.connect(self.onActionLoadNPZ)
        self.action_mat.triggered.connect(self.onActionLoadMAT)
        self.actionUpdateSession.triggered.connect(self.onLoadRealtimeStream)

        #hack no longer needed - self.windowTitleChanged.connect(self.newOfflineDataSession)

        # >> EDIT BUTTON
        # >> VIEW BUTTON
        # >> WINDOW BUTTON
        # >> SETTINGS BUTTON
        # >> HELP BUTTON

        # plot 1 - hover

        self.region = pg.LinearRegionItem()
        self.region.setZValue(10)
        # Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this
        # item when doing auto-range calculations.
        self.win1.addItem(self.region, ignoreBounds=True)

        self.win1.sigRangeChanged.connect(self.updateRegion)
        self.region.setRegion([-10, 50])
        self.region.sigRegionChanged.connect(self.update)
        # cross hair
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.win1.addItem(self.vLine, ignoreBounds=True)
        self.win1.addItem(self.hLine, ignoreBounds=True)
        self.vb = self.win1.plotItem.vb

        self.proxy = pg.SignalProxy(self.win1.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

        self.update_win1()
        self.update_win4()

        #containing_layout = self.win4.parent().layout()
        #containing_layout.replaceWidget(self.win4, self.win2)

        # END __INIT__ FUNCTION
        # =====================

    def newWidgetInPane(self):
        pass

    def toggleDarkMode(self):
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode: # dark mode
            self.win1.setBackground('d')
            self.win2.setBackground('d')
            self.win3.setBackground('d')
            self.win4.setBackground('d')
        else: # light mode
            self.win1.setBackground('w')
            self.win2.setBackground('w')
            self.win3.setBackground('w')
            self.win4.setBackground('w')

    # for crosshairs
    def update(self):
        self.region.setZValue(10)
        minX, maxX = self.region.getRegion()
        self.win1.setXRange(-10, 40, padding=0)

    def updateRegion(self, window, viewRange):
        rgn = viewRange[0]
        self.region.setRegion(rgn)

    def mouseMoved(self, evt):

        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.win1.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)

            print("array_stats")
            print(self.LoadedData.array_stats['spike_avg'])

            int_x = int(mousePoint.x())
            int_y = int(mousePoint.y())
            if 0 <= int_x < 32 and 0 <= int_y < 32:
                self.statusBar().showMessage(
                    "Array Map Spike Average @ " + str(int_x) + ", " + str(int_y) +
                    ": " + str(self.LoadedData.array_stats['spike_avg'][int_x][int_y])
                )

            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())

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

    def onLoadRealtimeStream(self):
        """
        Returns:

        """
        path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.loading_dict = initDataLoading(path)

        # TODO parallelize loading already saved .mat files
        load_realtime_worker = Worker(self.realtimeLoading, path, self.loading_dict)
        load_realtime_worker.signals.progress.connect(self.updateStatusBar)
        load_realtime_worker.signals.gui_callback.connect(self.updateGUIWithNewData)
        self.threadpool.start(load_realtime_worker)

    # callback from progress signal
    def updateStatusBar(self, message):
        self.statusBar().showMessage(message)

    # Continuously Check for New Data
    def realtimeLoading(self, path, loadingDict, progress_callback, gui_callback, dataIdentifierString='gmem1'):
        """

        Args:
            path:
            loadingDict:
            progress_callback:
            gui_callback:
            dataIdentifierString:

        Returns:

        """

        progress_callback.emit("in realtimeloading(): " + path)

        # string parse datarun+datapiece
        split_path = os.path.split(path)
        data_run = split_path[1]
        data_piece = os.path.split(split_path[0])[1]
        last_file_idx = 0

        while True:
            # In case multiple files coming in at once, hold 100ms (not likely)
            #     time.sleep(0.1)

            next_file = path + "/" + data_run + "_" + str(last_file_idx+1) + ".mat"

            # If the next numbered file doesn't exist, just wait
            if os.path.exists(next_file) is False:
                progress_callback.emit("Waiting for next buffer file to load in: " + next_file)

                continue
            else:  # next file does exist, so process it
                last_file_idx += 1 # update idx
                print("NEW FILE: ", last_file_idx)
                progress_callback.emit("Loading latest buffer file idx " + str(last_file_idx))

                # In the off chance the file has been written, but not saved by the TCP socket yet, pause
                time.sleep(0.5)

                # Load Data from this Loop's Buffer file
                mat_contents = sio.loadmat(next_file)
                dataRaw = mat_contents[dataIdentifierString][0][:]

                data_real, cnt_real, N = removeMultipleCounts(dataRaw)

                start = time.time()
                self.LoadedData.append_raw_data(data_real, cnt_real, N)
                end = time.time()
                if self.mode_profiling:
                    self.profile_data['append raw data'] = end - start

                start = time.time()
                self.LoadedData.update_filtered_data()
                end = time.time()
                if self.mode_profiling:
                    self.profile_data['filter data'] = end - start

                start = time.time()
                self.LoadedData.update_array_stats(data_real, N)
                end = time.time()
                if self.mode_profiling:
                    self.profile_data['calculate array stats'] = end - start

                # we need to call the main GUI thread to update graphs (can't do with non GUI-thread)
                gui_callback.emit()

    def onActionLoadNPZ(self):
        """

        Returns:

        """
        path = self.getDataPath("Numpy files (*.npz)")

        data = loadDataFromFileNpz(path)
        self.updateGUIWithNewData()

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
        if self.mode_multithreading:
            worker = Worker(self.loadDataFromFileMat, path, loadingDict)
            worker.signals.result.connect(self.updateGUIWithNewData)
            #worker.signals.finished.connect(self.thread_complete)
            #worker.signals.progress.connect(self.progress_fn)
            self.threadpool.start(worker)

        else:
            self.loadDataFromFileMat(path, loadingDict)

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
        self.filtered_data = applyFilterToAllData(self.dataAll, self.numChan, self.chMap, filtType='modHierlemann')

        if self.mode_multithreading is False:  # if multi-threaded, then this function is already connected on completion of fn
            self.updateGUIWithNewData()

    def updateGUIWithNewData(self):
        """

        Returns:

        """
        self.setWindowTitle('DC1 Vis - ' + self.loading_dict['path']) # -> connects to newOfflineDataSession

        print("GUI Counter: ", self.window_update_counter)

        start = time.time()
        self.update_win1()
        end = time.time()
        if self.mode_profiling:
            self.profile_data['array map'].append(end - start)

        start = time.time()
        self.update_win2()
        end = time.time()
        if self.mode_profiling:
            self.profile_data['spike trace'].append(end - start)

        start = time.time()
        self.update_win3()
        end = time.time()
        if self.mode_profiling:
            self.profile_data['noise histogram'].append(end - start)

        self.update_win4()

        if self.mode_profiling:
            print("Current profiling statistics:")
            for key in self.profile_data.keys():
                avg_time = np.round(np.mean(self.profile_data[key]), 3)
                print(key, avg_time)
        print("")

    def update_win1(self):

        self.win1.clear()
        # prepare demonstration data:
        if self.first_time_plotting is False:
            colors = self.LoadedData.array_stats['spike_avg']

            data = colors.T
        else:
            data = np.fromfunction(lambda i, j: (1 + 0.3 * np.sin(i)) * (i) ** 2 + (j) ** 2, (32, 32))
            data = data * (1 + 0.2 * np.random.random(data.shape))



        # Example: False color image with interactive level adjustment
        #self.first_time_plotting = False

        cm = pg.colormap.get('CET-D1')


        image = pg.ImageItem(data)
        self.win1.clear()
        self.win1.addItem(image)

        # bound the LinearRegionItem to the plotted data
        self.region.setClipItem(image)

        # TODO fix color limits
        if self.win1_colorbar is None:
            self.win1_colorbar = self.win1.addColorBar(image, colorMap=cm, values=(0, np.max(data)))
        else:
            self.win1_colorbar.setImageItem(image)
            self.win1_colorbar.setLevels((0, np.max(data)))

    def update_win2(self):
        trace_plots = [self.traceplot_1, self.traceplot_2, self.traceplot_3, self.traceplot_4]
        len_data = len(self.LoadedData.filtered_data)

        # Generate subplots
        for m, plt in enumerate(trace_plots):
            chan_idx = len_data + (m-4)
            x = self.LoadedData.filtered_data[chan_idx]['times']
            y = self.LoadedData.filtered_data[chan_idx]['data']
            plt.clear()
            plt.plot(x, y, pen='b')
            plt.setLabel('left', '#' + str(self.LoadedData.filtered_data[chan_idx]['channel_idx']))
            plt.enableAutoRange(axis='y')
            plt.setAutoVisible(y=True)

    def update_win3(self):
        self.win3.clear()
        vals = self.LoadedData.array_stats['noise_std']
        vals = vals[np.nonzero(vals)]
        # get nonzero vals because zeros have not had noise calculation done yet

        y, x = np.histogram(vals, bins=np.linspace(0,20,40))
        curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0,0,255,80))
        self.win3.addItem(curve)

    def update_win4(self):
        self.win4.clear()
        # prepare demonstration data:

        if self.first_time_plotting is False:
            spike_cnt = self.LoadedData.array_stats['spike_cnt']

            # AX1) Size by Number of Samples
            scale1 = (max_dot - 15) / (np.max(spike_cnt) - np.min(spike_cnt[spike_cnt != 0]))
            b_add = max_dot - (np.max(spike_cnt) * scale1)
            size = np.round(spike_cnt * scale1 + b_add)
            size[size < 15] = 10

            data = spike_cnt.T
        else:
            data = np.fromfunction(lambda i, j: (1 + 0.3 * np.sin(i)) * (i) ** 2 + (j) ** 2, (32, 32))
            data = data * (1 + 0.2 * np.random.random(data.shape))

        self.first_time_plotting = False

        # Example: False color image with interactive level adjustment
        #self.first_time_plotting = False

        cm = pg.colormap.get('CET-D1')

        image = pg.ImageItem(data)

        self.win4.addItem(image)
        # TODO fix color limits

        self.win4.addColorBar(image, colorMap=cm, values=(0, np.max(data)))


    def change_win1(self):
        self.horizontalLayout_top.removeItem(self.win1)
        self.horizontalLayout_top.addItem(self.win1)

    def plot_data(self, widget, x, y):
        widget.plot(x, y)

    """
    =======================
    MENU BAR // EDIT...
    =======================
    """


    """
    =======================
    MENU BAR // VIEW...
    =======================
    """


    """
    =======================
    MENU BAR // WINDOW...
    =======================
    """
    # TODO func - update window with new data
    def updateWindowWithNewData(self, window):
        pass

    """
    =======================
    MENU BAR // SETTINGS...
    =======================
    """


    """
    =======================
    TEST FUNCTIONS
    =======================
    """
    def plot(self, hour, temperature):
        self.traceplot_1.plot(hour, temperature)

class PlotWindow():
    data = None

    def __init__(self):
        pass

    def update(self):
        pass

