# this script runs the startup app for all the DC1 data visualization tools
# author: Huy Nguyen (2022)

from src.gui.gui_base import * # MainWindow class
from src.gui.gui_layout import *
from src.gui.gui_funcs import *

from src.analysis.analysis_helpers import *
from src.data.data_loading import *
from src.data.preprocessing import *
import multiprocessing as mp

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
    mp.set_start_method('spawn')

