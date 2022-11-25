from PyQt5 import QtWidgets, QtCore
import PyQt5.uic as uic
import os

class SessionStartupGUI(QtWidgets.QDialog):
    settings = {}

    def __init__(self, basedir, DEBUG_SETTINGS):
        super(QtWidgets.QDialog, self).__init__()
        uic.loadUi("./src/view/layouts/SessionStartupGUI.ui", self)
        self.THRESHOLD_MIN = DEBUG_SETTINGS['threshold_min']
        self.THRESHOLD_MAX = DEBUG_SETTINGS['threshold_max']
        self.THRESHOLD_DEFAULT = DEBUG_SETTINGS['threshold_default']
        self.DEFAULT_DATASET_PATH = DEBUG_SETTINGS['default_dataset_path']

        self.setWindowTitle("Set Session Parameters...")

        self.chooseVisStyle.activated.connect(self.setVisStyle)
        self.settings["visStyle"] = self.chooseVisStyle.currentText()

        self.chooseFilePath.clicked.connect(self.getFolderDir)

        os.chdir(basedir)
        self.settings["path"] = os.path.join(os.getcwd(), self.DEFAULT_DATASET_PATH)

        self.chooseRealTime.activated.connect(self.setRealTime)
        self.settings["realTime"] = self.chooseRealTime.currentText()

        self.chooseFilter.activated.connect(self.setFilter)
        self.settings["filter"] = self.chooseFilter.currentText()

        self.chooseSpikeDetectionMethod.activated.connect(self.setSpikeDetectionMethod)
        self.settings["spikeDetectionMethod"] = self.chooseSpikeDetectionMethod.currentText()

        self.chooseSpikeThreshold.sliderMoved.connect(self.setSpikeThreshold)
        self.chooseSpikeThreshold.setRange(float(self.THRESHOLD_MIN) * 100, float(self.THRESHOLD_MAX) * 100)
        self.chooseSpikeThreshold.setValue(self.THRESHOLD_DEFAULT * 100)
        self.LabelSpikeThreshold.setText(str(self.THRESHOLD_DEFAULT))
        self.settings["spikeThreshold"] = float(self.THRESHOLD_DEFAULT)

    def getFolderDir(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.LabelFilePath.setText(os.path.basename(path))
        self.settings["path"] = path

    def setVisStyle(self): self.settings["visStyle"] = self.chooseVisStyle.currentText()
    def setRealTime(self): self.settings["realTime"] = self.chooseRealTime.currentText()
    def setFilter(self): self.settings["filter"] = self.chooseFilter.currentText()
    def setSpikeDetectionMethod(self):
        self.settings["spikeDetectionMethod"] = self.chooseSpikeDetectionMethod.currentText()
    def setSpikeThreshold(self):
        self.settings["spikeThreshold"] = round(self.chooseSpikeThreshold.value() / 100, 2)
        self.LabelSpikeThreshold.setText(str(self.settings["spikeThreshold"]))