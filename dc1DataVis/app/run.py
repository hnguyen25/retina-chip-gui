# this script runs the startup app for all the DC1 data visualization tools
# author: Huy Nguyen (2022)

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
    app = QtWidgets.QApplication(sys.argv)
    gui_preferences = GUIPreferences() # startup pane to set runtime preferences

    if gui_preferences.exec():  # run startup dialog before anything
        settings = gui_preferences.settings

        # create visualization window with the given settings
        window = MainWindow()
        window.setSettings(settings)

        # setup visualization layout chosen during startup
        window.setupLayout()
        window.loadSession()

        # execute main app
        window.show()
        app.exec_()

    else: # if dialog canceled then close app
        print('startup-no')
        sys.exit()




