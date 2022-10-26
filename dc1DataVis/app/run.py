"""
run.py
Huy Nguyen (2022)
----
script to run entire application
"""

import os, sys
import multiprocessing as mp

from PyQt5 import QtWidgets, QtCore
from dc1DataVis.app.src.gui.SessionStartupGUI import SessionStartupGUI

from dc1DataVis.app.src.MainWindow import MainWindow

# =============================
# EDITABLE PARAMETERS
# =============================
APP_TITLE = 'Stanford Artificial Retina Project | Retina Chip v1.0 Experimental Visualization'
WINDOWED_APP_SIZE = [1000, 750]  # size of main application (W x H)
DEBUG_SETTINGS = {
    'current_theme': 'dark',
    # different GUI modes
    'is_mode_profiling': False,  # if on, measures how long different aspects of the GUI takes to compute
    'is_mode_multithreading': False,  # if on, enables multiprocessing capability. may be easier to debug if off
    # GUI play/pause
    'first_time_plotting': True,  # indicates if the first packet of data has not been processed yet,
    # (useful to know for setting up PyQtGraph charts)
    'is_live_plotting': True,  # indicates if the program is still continuously reading available data packets
    'is_true_realtime': True,  # indicates if the program is continuously reading the LAST available data packet
    # initial location of cursor on the array map
    'cursor_row': 16, 'cursor_col': 16,
    'filter': "Modified Hierlemann",
    'spikeThreshold': 4,
    'binSize': 1,
    'simultaneousChannelsRecordedPerPacket': 4
}

# Session Startup Panel
DEBUG_STARTUP = {
    'threshold_min': 0.5, 'threshold_max': 6, 'threshold_default': 4,
    'default_dataset_path': 'debugData/2022-02-18-0/data001'
}

# =============================
# MAIN BODY
# =============================
if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    os.chdir(base_dir)
    print("Application starting from base directory", base_dir)

    if DEBUG_SETTINGS['is_mode_multithreading']: mp.set_start_method('spawn')

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  # fix Windows scaling issue
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)  # use high DPI icons
    app.setStyleSheet("QWidget { font: 14px; }")

    session_startup = SessionStartupGUI(base_dir, DEBUG_STARTUP)  # load initial startup window where user can specify session
    if session_startup.exec():  # continue running app only if user has successfully completed startup window

        SESSION_SETTINGS = session_startup.settings
        settings = {**SESSION_SETTINGS, **DEBUG_SETTINGS} # get all settings, both from user and developer

        # start analysis window of choice
        window = MainWindow(settings=settings, window_title=APP_TITLE)
        window.resize(WINDOWED_APP_SIZE[0], WINDOWED_APP_SIZE[1])
        window.show()
        app.exec()


    print('Application completed. Killing process...')
    sys.exit()
