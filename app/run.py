"""
script to run entire application
"""
import os, sys
sys.path.append("app")

import multiprocessing as mp
from PyQt5 import QtWidgets, QtCore
from src.controller.windows.window_sessionstartup import SessionStartupGUI
from src.MainWindow import MainWindow


APP_TITLE = 'Stanford Artificial Retina Project | Retina Chip v1.0 Experimental Visualization'
WINDOWED_APP_SIZE = [1000, 750]  # size of main application (W x H)
DEBUG_SETTINGS = {
    'current_theme': 'dark',
    # different GUI modes
    'is_mode_profiling': True,  # if on, measures how long different aspects of the GUI takes to compute
    'is_mode_multithreading': False,  # if on, enables multiprocessing capability. may be easier to debug if off
    # GUI play/pause
    'first_time_plotting': True,  # indicates if the first packet of model has not been processed yet,
    # (useful to know for setting up PyQtGraph charts)
    'is_live_plotting': True,  # indicates if the program is still continuously reading available model packets
    'is_true_realtime': True,  # indicates if the program is continuously reading the LAST available model packet
    # initial location of cursor on the array map
    'cursor_row': 4, 'cursor_col': 2,
    #'filter': "Modified Hierlemann", # this will override the session startup settings
    'binSize': 4,
    'simultaneousChannelsRecordedPerPacket': 4,
    'debug_threads': False,

    # array map
    'min_dot_size': 0.1,
    'max_dot_size': 1.5,
    'spike_cnt_for_dot_size_saturation': 50
}

# Session Startup Panel
DEBUG_STARTUP = {
    'threshold_min': 1, 'threshold_max': 8, 'threshold_default': 4,
    'default_dataset_path': 'debugData/2022-02-18-0/data001'
}

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    os.chdir(base_dir)

    print("Application starting from base directory", base_dir)

    if DEBUG_SETTINGS['is_mode_multithreading']: mp.set_start_method('spawn')

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  # fix Windows scaling issue
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)  # use high DPI icons
    app.setStyleSheet("QWidget { font: 14px; }")
    app.setStyleSheet("""QToolTip { 
                                   background-color: black; 
                                   color: white; 
                                   border: black solid 1px
                                   }""")
    app.setStyleSheet("QStatusBar{padding-left:8px;color:white;font-weight:bold;font-family:'Arial'}")

    continue_running = True
    while continue_running:
        continue_running = False

        session_startup = SessionStartupGUI(base_dir, DEBUG_STARTUP)  # load initial startup window where user can specify session
        if session_startup.exec():  # continue running app only if user has successfully completed startup window

            SESSION_SETTINGS = session_startup.settings
            print("SESSION_SETTINGS", SESSION_SETTINGS)
            settings = {**SESSION_SETTINGS, **DEBUG_SETTINGS} # get all settings, both from user and developer

            # start analysis window of choice
            window = MainWindow(settings=settings, window_title=APP_TITLE)
            window.resize(WINDOWED_APP_SIZE[0], WINDOWED_APP_SIZE[1])
            window.show()
            app.exec()

            if window.new_session:
                continue_running = True

    print('Application completed. Killing process...')
    app.quit()