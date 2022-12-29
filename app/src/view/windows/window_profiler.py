from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
import numpy as np
import pyqtgraph as pg
import time
from app.src.model.spike_detection import *
from app.src.model.DC1DataContainer import *

class GUIProfiler(QWidget):
    session_parent = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./src/view/layouts/GUIProfiler.ui", self)

    def setSessionParent(self, session_parent):
        self.session_parent = session_parent
        self.setupCharts()

    def setupCharts(self):
        pass