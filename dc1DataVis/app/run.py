# this script runs the startup app for all the DC1 data visualization tools
# author: Huy Nguyen (2022)
import os

basedir = os.path.dirname(__file__)
print(basedir)

from src.gui.gui_base import * # MainWindow class
from src.gui.gui_layout import *
from src.gui.gui_funcs import *

from src.analysis.analysis_helpers import *
from src.data.data_loading import *
from src.data.preprocessing import *
import multiprocessing as mp

from src.gui.default_vis import Ui_mainWindow # layout



if __name__ == "__main__":
    mp.set_start_method('spawn') # multiprocessing setting
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1" # fix Windows scaling issue
    app = QtWidgets.QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling) # fix Windows scaling issue
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, )  # use highdpi icons
    app.setStyleSheet("QWidget { font: 14px;}")
    gui_preferences = GUIPreferences(basedir) # startup pane to set runtime preferences

    if gui_preferences.exec():  # run startup dialog before anything
        os.chdir(basedir)
        settings = gui_preferences.settings

        # create visualization window with the given settings
        window = MainWindow()
        window.setSettings(settings)
        window.setBaseDir(basedir)

        # setup visualization layout chosen during startup
        window.setupLayout()
        window.loadSession()

        # execute main app
        window.show()
        app.exec_()

        #QtCore.QTimer.singleShot(0, window.close) # <---
        #sys.exit(app.exec_())


    else: # if dialog canceled then close app
        print('startup-no')
        sys.exit()




