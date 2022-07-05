from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os, sys
from ..gui.startup import Ui_Startup # layout

class GUIPreferences(QtWidgets.QDialog, Ui_Startup):
    THRESHOLD_MIN = 0.5
    THRESHOLD_DEFAULT = 2
    THRESHOLD_MAX = 5
    settings = {}

    def __init__(self, basedir, *args, **kwargs):
        super(QtWidgets.QDialog, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setWindowTitle("Set Session Parameters...")

        self.chooseVisStyle.activated.connect(self.setVisStyle)
        self.settings["visStyle"] = self.chooseVisStyle.currentText()

        self.chooseFilePath.clicked.connect(self.getFolderDir)

        # ensure correct directory for packaged app
        os.chdir(basedir)
        #os.chdir('../')
        self.settings["path"] = os.path.join(os.getcwd(), "debugData/2022-02-17-0/data002")
        #'/Users/huy/artifical-retina-pipeline-guis/dc1DataVis/debugData/2022-02-17-0/data002'

        self.chooseRealTime.activated.connect(self.setRealTime)
        self.settings["realTime"] = self.chooseRealTime.currentText()

        self.chooseAutoSave.activated.connect(self.setAutoSave)
        self.settings["autoSave"] = self.chooseAutoSave.currentText()

        self.chooseNumChannels.activated.connect(self.setNumChannels)
        self.settings["numChannels"] = int(self.chooseNumChannels.currentText())

        self.chooseFilter.activated.connect(self.setFilter)
        self.settings["filter"] = self.chooseFilter.currentText()

        self.chooseSpikeThreshold.sliderMoved.connect(self.setSpikeThreshold)
        self.chooseSpikeThreshold.setRange(float(self.THRESHOLD_MIN) * 100, float(self.THRESHOLD_MAX) * 100)
        self.chooseSpikeThreshold.setValue(self.THRESHOLD_DEFAULT * 100)
        self.LabelSpikeThreshold.setText(str(self.THRESHOLD_DEFAULT))
        self.settings["spikeThreshold"] = float(self.THRESHOLD_DEFAULT)

    def getFolderDir(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.LabelFilePath.setText(os.path.basename(path))
        self.settings["path"] = path

    def setVisStyle(self):
        self.settings["visStyle"] = self.chooseVisStyle.currentText()

    def setRealTime(self):
        self.settings["realTime"] = self.chooseRealTime.currentText()

    def setAutoSave(self):
        self.settings["autoSave"] = self.chooseAutoSave.currentText()

    def setNumChannels(self):
        self.settings["numChannels"] = self.chooseNumChannels.currentText()

    def setFilter(self):
        self.settings["filter"] = self.chooseFilter.currentText()

    def setSpikeThreshold(self):
        self.settings["spikeThreshold"] = round(self.chooseSpikeThreshold.value() / 100, 2)
        self.LabelSpikeThreshold.setText(str(self.settings["spikeThreshold"]))