# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'IndividualChannelWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IndividualChannelInfo(object):
    def setupUi(self, IndividualChannelInfo):
        IndividualChannelInfo.setObjectName("IndividualChannelInfo")
        IndividualChannelInfo.resize(835, 606)
        self.gridLayout_2 = QtWidgets.QGridLayout(IndividualChannelInfo)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.updateElectrodeNum = QtWidgets.QPushButton(IndividualChannelInfo)
        self.updateElectrodeNum.setMaximumSize(QtCore.QSize(150, 16777215))
        self.updateElectrodeNum.setObjectName("updateElectrodeNum")
        self.horizontalLayout.addWidget(self.updateElectrodeNum)
        self.label_2 = QtWidgets.QLabel(IndividualChannelInfo)
        self.label_2.setMaximumSize(QtCore.QSize(40, 20))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.InputElectrodeRow = QtWidgets.QTextEdit(IndividualChannelInfo)
        self.InputElectrodeRow.setMaximumSize(QtCore.QSize(50, 20))
        self.InputElectrodeRow.setObjectName("InputElectrodeRow")
        self.horizontalLayout.addWidget(self.InputElectrodeRow)
        self.label_3 = QtWidgets.QLabel(IndividualChannelInfo)
        self.label_3.setMaximumSize(QtCore.QSize(40, 20))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.InputElectrodeCol = QtWidgets.QTextEdit(IndividualChannelInfo)
        self.InputElectrodeCol.setMaximumSize(QtCore.QSize(60, 20))
        self.InputElectrodeCol.setObjectName("InputElectrodeCol")
        self.horizontalLayout.addWidget(self.InputElectrodeCol)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.updateRC = QtWidgets.QPushButton(IndividualChannelInfo)
        self.updateRC.setMaximumSize(QtCore.QSize(200, 16777215))
        self.updateRC.setObjectName("updateRC")
        self.horizontalLayout_2.addWidget(self.updateRC)
        self.label = QtWidgets.QLabel(IndividualChannelInfo)
        self.label.setMaximumSize(QtCore.QSize(100, 30))
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.InputElectrodeNumber = QtWidgets.QTextEdit(IndividualChannelInfo)
        self.InputElectrodeNumber.setMaximumSize(QtCore.QSize(80, 30))
        self.InputElectrodeNumber.setObjectName("InputElectrodeNumber")
        self.horizontalLayout_2.addWidget(self.InputElectrodeNumber)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.totalSamples = QtWidgets.QLabel(IndividualChannelInfo)
        self.totalSamples.setMaximumSize(QtCore.QSize(200, 167))
        self.totalSamples.setObjectName("totalSamples")
        self.verticalLayout_2.addWidget(self.totalSamples)
        self.timeRecorded = QtWidgets.QLabel(IndividualChannelInfo)
        self.timeRecorded.setObjectName("timeRecorded")
        self.verticalLayout_2.addWidget(self.timeRecorded)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.AmplitudeHistPlot = PlotWidget(IndividualChannelInfo)
        self.AmplitudeHistPlot.setMinimumSize(QtCore.QSize(402, 247))
        self.AmplitudeHistPlot.setObjectName("AmplitudeHistPlot")
        self.gridLayout.addWidget(self.AmplitudeHistPlot, 0, 0, 1, 1)
        self.SpikeRatePlot = PlotWidget(IndividualChannelInfo)
        self.SpikeRatePlot.setEnabled(True)
        self.SpikeRatePlot.setMinimumSize(QtCore.QSize(402, 247))
        self.SpikeRatePlot.setObjectName("SpikeRatePlot")
        self.gridLayout.addWidget(self.SpikeRatePlot, 0, 1, 1, 1)
        self.ChannelTracePlot = PlotWidget(IndividualChannelInfo)
        self.ChannelTracePlot.setMinimumSize(QtCore.QSize(402, 247))
        self.ChannelTracePlot.setObjectName("ChannelTracePlot")
        self.gridLayout.addWidget(self.ChannelTracePlot, 1, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.label_2.setBuddy(self.InputElectrodeRow)
        self.label_3.setBuddy(self.InputElectrodeCol)
        self.label.setBuddy(self.InputElectrodeNumber)

        self.retranslateUi(IndividualChannelInfo)
        QtCore.QMetaObject.connectSlotsByName(IndividualChannelInfo)

    def retranslateUi(self, IndividualChannelInfo):
        _translate = QtCore.QCoreApplication.translate
        IndividualChannelInfo.setWindowTitle(_translate("IndividualChannelInfo", "Individual Channel Information"))
        self.updateElectrodeNum.setText(_translate("IndividualChannelInfo", "Update Electrode No. "))
        self.label_2.setText(_translate("IndividualChannelInfo", "Row"))
        self.InputElectrodeRow.setHtml(_translate("IndividualChannelInfo", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_3.setText(_translate("IndividualChannelInfo", "Col"))
        self.InputElectrodeCol.setHtml(_translate("IndividualChannelInfo", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.updateRC.setText(_translate("IndividualChannelInfo", "Update Row and Column"))
        self.label.setText(_translate("IndividualChannelInfo", "Electrode No. "))
        self.InputElectrodeNumber.setHtml(_translate("IndividualChannelInfo", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.totalSamples.setText(_translate("IndividualChannelInfo", "totalSamples"))
        self.timeRecorded.setText(_translate("IndividualChannelInfo", "timeRecorded"))
from pyqtgraph import PlotWidget