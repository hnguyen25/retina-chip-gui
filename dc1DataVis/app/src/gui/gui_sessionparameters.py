def openSessionParams():
    session_dialog = QDialog()
    uic.loadUi("./src/gui/SessionStartupGUI.ui", session_dialog)
    session_dialog.setWindowTitle("Set Session Parameters...")
    session_dialog.exec()

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

class GUIPreferences(QDialog):
    def __init__(self, *args, **kwargs):
        super(QtWidgets.QDialog, self).__init__(*args, **kwargs)
        uic.loadUi("./src/gui/GUIPreferences.ui", self)

