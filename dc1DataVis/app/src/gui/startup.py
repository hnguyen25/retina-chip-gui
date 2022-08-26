# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'startup.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Startup(object):
    def setupUi(self, Startup):
        Startup.setObjectName("Startup")
        Startup.resize(486, 382)
        self.gridLayout = QtWidgets.QGridLayout(Startup)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Startup)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.chooseVisStyle = QtWidgets.QComboBox(Startup)
        self.chooseVisStyle.setObjectName("chooseVisStyle")
        self.chooseVisStyle.addItem("")
        self.chooseVisStyle.addItem("")
        self.chooseVisStyle.addItem("")
        self.chooseVisStyle.addItem("")
        self.chooseVisStyle.addItem("")
        self.chooseVisStyle.addItem("")
        self.gridLayout.addWidget(self.chooseVisStyle, 0, 1, 1, 2)
        self.label_8 = QtWidgets.QLabel(Startup)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)
        self.chooseRealTime = QtWidgets.QComboBox(Startup)
        self.chooseRealTime.setObjectName("chooseRealTime")
        self.chooseRealTime.addItem("")
        self.chooseRealTime.addItem("")
        self.chooseRealTime.addItem("")
        self.chooseRealTime.addItem("")
        self.chooseRealTime.addItem("")
        self.gridLayout.addWidget(self.chooseRealTime, 1, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(Startup)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.chooseFilePath = QtWidgets.QPushButton(Startup)
        self.chooseFilePath.setObjectName("chooseFilePath")
        self.gridLayout.addWidget(self.chooseFilePath, 2, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(Startup)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)
        self.chooseAutoSave = QtWidgets.QComboBox(Startup)
        self.chooseAutoSave.setObjectName("chooseAutoSave")
        self.chooseAutoSave.addItem("")
        self.chooseAutoSave.addItem("")
        self.chooseAutoSave.addItem("")
        self.gridLayout.addWidget(self.chooseAutoSave, 4, 1, 1, 2)
        self.label_4 = QtWidgets.QLabel(Startup)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        self.chooseNumChannels = QtWidgets.QComboBox(Startup)
        self.chooseNumChannels.setObjectName("chooseNumChannels")
        self.chooseNumChannels.addItem("")
        self.chooseNumChannels.addItem("")
        self.chooseNumChannels.addItem("")
        self.chooseNumChannels.addItem("")
        self.chooseNumChannels.addItem("")
        self.chooseNumChannels.addItem("")
        self.gridLayout.addWidget(self.chooseNumChannels, 5, 1, 1, 2)
        self.label_5 = QtWidgets.QLabel(Startup)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        self.chooseFilter = QtWidgets.QComboBox(Startup)
        self.chooseFilter.setObjectName("chooseFilter")
        self.chooseFilter.addItem("")
        self.chooseFilter.addItem("")
        self.chooseFilter.addItem("")
        self.chooseFilter.addItem("")
        self.chooseFilter.addItem("")
        self.chooseFilter.addItem("")
        self.chooseFilter.addItem("")
        self.chooseFilter.addItem("")
        self.chooseFilter.addItem("")
        self.gridLayout.addWidget(self.chooseFilter, 6, 1, 1, 2)
        self.label_6 = QtWidgets.QLabel(Startup)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 7, 0, 1, 1)
        self.chooseSpikeThreshold = QtWidgets.QSlider(Startup)
        self.chooseSpikeThreshold.setOrientation(QtCore.Qt.Horizontal)
        self.chooseSpikeThreshold.setObjectName("chooseSpikeThreshold")
        self.gridLayout.addWidget(self.chooseSpikeThreshold, 7, 1, 1, 1)
        self.LabelSpikeThreshold = QtWidgets.QLabel(Startup)
        self.LabelSpikeThreshold.setAlignment(QtCore.Qt.AlignCenter)
        self.LabelSpikeThreshold.setObjectName("LabelSpikeThreshold")
        self.gridLayout.addWidget(self.LabelSpikeThreshold, 7, 2, 1, 1)
        self.DialogButtonBox = QtWidgets.QDialogButtonBox(Startup)
        self.DialogButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.DialogButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.DialogButtonBox.setObjectName("DialogButtonBox")
        self.gridLayout.addWidget(self.DialogButtonBox, 8, 0, 1, 3)
        self.LabelFilePath = QtWidgets.QLabel(Startup)
        self.LabelFilePath.setMaximumSize(QtCore.QSize(16777215, 30))
        self.LabelFilePath.setObjectName("LabelFilePath")
        self.gridLayout.addWidget(self.LabelFilePath, 3, 1, 1, 1)
        self.label.setBuddy(self.chooseVisStyle)
        self.label_8.setBuddy(self.chooseRealTime)
        self.label_2.setBuddy(self.chooseFilePath)
        self.label_9.setBuddy(self.chooseAutoSave)
        self.label_4.setBuddy(self.chooseNumChannels)
        self.label_5.setBuddy(self.chooseFilter)
        self.label_6.setBuddy(self.chooseSpikeThreshold)

        self.retranslateUi(Startup)
        self.DialogButtonBox.accepted.connect(Startup.accept) # type: ignore
        self.DialogButtonBox.rejected.connect(Startup.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Startup)
        Startup.setTabOrder(self.chooseVisStyle, self.chooseRealTime)
        Startup.setTabOrder(self.chooseRealTime, self.chooseFilePath)
        Startup.setTabOrder(self.chooseFilePath, self.chooseAutoSave)
        Startup.setTabOrder(self.chooseAutoSave, self.chooseNumChannels)
        Startup.setTabOrder(self.chooseNumChannels, self.chooseFilter)
        Startup.setTabOrder(self.chooseFilter, self.chooseSpikeThreshold)

    def retranslateUi(self, Startup):
        _translate = QtCore.QCoreApplication.translate
        Startup.setWindowTitle(_translate("Startup", "Choose Session Parameters..."))
        self.label.setText(_translate("Startup", "Visualization style"))
        self.chooseVisStyle.setItemText(0, _translate("Startup", "Default"))
        self.chooseVisStyle.setItemText(1, _translate("Startup", "Spike Search"))
        self.chooseVisStyle.setItemText(2, _translate("Startup", "Noise"))
        self.chooseVisStyle.setItemText(3, _translate("Startup", "Diagnostic"))
        self.chooseVisStyle.setItemText(4, _translate("Startup", "Full-bandwidth recording"))
        self.chooseVisStyle.setItemText(5, _translate("Startup", "Compressed recording"))
        self.label_8.setText(_translate("Startup", "Real-time?"))
        self.chooseRealTime.setItemText(0, _translate("Startup", "Yes, load first .mat chunk"))
        self.chooseRealTime.setItemText(1, _translate("Startup", "Yes, load latest .mat chunk"))
        self.chooseRealTime.setItemText(2, _translate("Startup", "No, load raw .mat file"))
        self.chooseRealTime.setItemText(3, _translate("Startup", "No, load pre-processed .npz file"))
        self.chooseRealTime.setItemText(4, _translate("Startup", "No, load filtered .npz file"))
        self.label_2.setText(_translate("Startup", "Data file directory"))
        self.chooseFilePath.setText(_translate("Startup", "File path..."))
        self.label_9.setText(_translate("Startup", "Autosave processed data?"))
        self.chooseAutoSave.setItemText(0, _translate("Startup", "Yes, save preprocessed data to .npz"))
        self.chooseAutoSave.setItemText(1, _translate("Startup", "Yes, save filtered data to .npz"))
        self.chooseAutoSave.setItemText(2, _translate("Startup", "No"))
        self.label_4.setText(_translate("Startup", "No. of channels at once"))
        self.chooseNumChannels.setItemText(0, _translate("Startup", "1"))
        self.chooseNumChannels.setItemText(1, _translate("Startup", "2"))
        self.chooseNumChannels.setItemText(2, _translate("Startup", "4"))
        self.chooseNumChannels.setItemText(3, _translate("Startup", "8"))
        self.chooseNumChannels.setItemText(4, _translate("Startup", "16"))
        self.chooseNumChannels.setItemText(5, _translate("Startup", "32"))
        self.label_5.setText(_translate("Startup", "Filter type"))
        self.chooseFilter.setItemText(0, _translate("Startup", "Hierlemann"))
        self.chooseFilter.setItemText(1, _translate("Startup", "Modified Hierlemann"))
        self.chooseFilter.setItemText(2, _translate("Startup", "Highpass"))
        self.chooseFilter.setItemText(3, _translate("Startup", "H0 Bandpass"))
        self.chooseFilter.setItemText(4, _translate("Startup", "Auto"))
        self.chooseFilter.setItemText(5, _translate("Startup", "Fast Bandpass"))
        self.chooseFilter.setItemText(6, _translate("Startup", "Faster Bandpass"))
        self.chooseFilter.setItemText(7, _translate("Startup", "Litke"))
        self.chooseFilter.setItemText(8, _translate("Startup", "None"))
        self.label_6.setText(_translate("Startup", "Spike detection threshold"))
        self.LabelSpikeThreshold.setText(_translate("Startup", "1"))
        self.LabelFilePath.setText(_translate("Startup", "(File path not chosen...)"))
