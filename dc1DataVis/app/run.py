# this script runs the startup app for all the DC1 data visualization tools
# author: Huy Nguyen (2022)
import os, sys

basedir = os.path.dirname(__file__)


from src.gui.gui_layout import *

from src.data.data_loading import *
import multiprocessing as mp

# GUI STATE: contains variables which change over the course of the GUI visualization
WINDOW_TITLE = 'Stanford Artificial Retina Project | Retina Chip v1.0 Experimental Visualization'
GLOBAL_SETTINGS = {
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

if __name__ == "__main__":
    mp.set_start_method('spawn') # multiprocessing setting
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  # fix Windows scaling issue
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, )  # use highdpi icons
    app.setStyleSheet("QWidget { font: 14px; }")


    from src.gui.gui_guipreferences import GUIPreferences
    gui_preferences = GUIPreferences(basedir)  # startup pane to set runtime preferences

    if gui_preferences.exec():  # run startup dialog before anything
        os.chdir(basedir)

        SESSION_SETTINGS = gui_preferences.settings
        settings = {**SESSION_SETTINGS, **GLOBAL_SETTINGS}




        # init main GUI window
        from dc1DataVis.app.src.MainWindow import MainWindow
        window = MainWindow(settings=settings, window_title=WINDOW_TITLE)

        # setup visualization layout chosen during startup
        window.setupLayout()
        window.loadSession()

        window.resize(1000, 750)

        # execute main app
        window.show()
        app.exec_()

    else:  # if dialog canceled then close app
        print('startup-no')
        sys.exit()




