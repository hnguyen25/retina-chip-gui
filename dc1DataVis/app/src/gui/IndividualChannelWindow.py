# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'individualchannelwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IndividualChannelInfo(object):
    def setupUi(self, IndividualChannelInfo):
        IndividualChannelInfo.setObjectName("IndividualChannelInfo")
        IndividualChannelInfo.resize(825, 587)
        self.gridLayout_2 = QtWidgets.QGridLayout(IndividualChannelInfo)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.UpdateInput = QtWidgets.QPushButton(IndividualChannelInfo)
        self.UpdateInput.setObjectName("UpdateInput")
        self.horizontalLayout.addWidget(self.UpdateInput)
        self.label = QtWidgets.QLabel(IndividualChannelInfo)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.InputElectrodeNumber = QtWidgets.QTextEdit(IndividualChannelInfo)
        self.InputElectrodeNumber.setMaximumSize(QtCore.QSize(167, 167))
        self.InputElectrodeNumber.setObjectName("InputElectrodeNumber")
        self.horizontalLayout.addWidget(self.InputElectrodeNumber)
        self.label_2 = QtWidgets.QLabel(IndividualChannelInfo)
        self.label_2.setMaximumSize(QtCore.QSize(50, 167))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.InputElectrodeRow = QtWidgets.QTextEdit(IndividualChannelInfo)
        self.InputElectrodeRow.setMaximumSize(QtCore.QSize(100, 167))
        self.InputElectrodeRow.setObjectName("InputElectrodeRow")
        self.horizontalLayout.addWidget(self.InputElectrodeRow)
        self.label_3 = QtWidgets.QLabel(IndividualChannelInfo)
        self.label_3.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.InputElectrodeCol = QtWidgets.QTextEdit(IndividualChannelInfo)
        self.InputElectrodeCol.setMaximumSize(QtCore.QSize(100, 167))
        self.InputElectrodeCol.setObjectName("InputElectrodeCol")
        self.horizontalLayout.addWidget(self.InputElectrodeCol)
        self.LabelElectrodeInfo = QtWidgets.QLabel(IndividualChannelInfo)
        self.LabelElectrodeInfo.setMaximumSize(QtCore.QSize(167, 167))
        self.LabelElectrodeInfo.setObjectName("LabelElectrodeInfo")
        self.horizontalLayout.addWidget(self.LabelElectrodeInfo)
        self.totalSamples = QtWidgets.QLabel(IndividualChannelInfo)
        self.totalSamples.setMaximumSize(QtCore.QSize(167, 167))
        self.totalSamples.setObjectName("totalSamples")
        self.horizontalLayout.addWidget(self.totalSamples)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.ChannelTracePlot = PlotWidget(IndividualChannelInfo)
        self.ChannelTracePlot.setMinimumSize(QtCore.QSize(402, 247))
        self.ChannelTracePlot.setObjectName("ChannelTracePlot")
        self.gridLayout.addWidget(self.ChannelTracePlot, 0, 1, 1, 1)
        self.AmplitudeHistPlot = PlotWidget(IndividualChannelInfo)
        self.AmplitudeHistPlot.setMinimumSize(QtCore.QSize(402, 247))
        self.AmplitudeHistPlot.setObjectName("AmplitudeHistPlot")
        self.gridLayout.addWidget(self.AmplitudeHistPlot, 0, 0, 1, 1)
        self.SpikeRatePlot = PlotWidget(IndividualChannelInfo)
        self.SpikeRatePlot.setEnabled(True)
        self.SpikeRatePlot.setMinimumSize(QtCore.QSize(402, 247))
        self.SpikeRatePlot.setObjectName("SpikeRatePlot")
        self.gridLayout.addWidget(self.SpikeRatePlot, 1, 1, 1, 1)
        self.SpikeRateHistPlot = PlotWidget(IndividualChannelInfo)
        self.SpikeRateHistPlot.setMinimumSize(QtCore.QSize(402, 247))
        self.SpikeRateHistPlot.setObjectName("SpikeRateHistPlot")
        self.gridLayout.addWidget(self.SpikeRateHistPlot, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.label.setBuddy(self.InputElectrodeNumber)
        self.label_2.setBuddy(self.InputElectrodeRow)
        self.label_3.setBuddy(self.InputElectrodeCol)

        self.retranslateUi(IndividualChannelInfo)
        QtCore.QMetaObject.connectSlotsByName(IndividualChannelInfo)

    def retranslateUi(self, IndividualChannelInfo):
        _translate = QtCore.QCoreApplication.translate
        IndividualChannelInfo.setWindowTitle(_translate("IndividualChannelInfo", "Individual Channel Information"))
        self.UpdateInput.setText(_translate("IndividualChannelInfo", "Update Input"))
        self.label.setText(_translate("IndividualChannelInfo", "Electrode No. "))
        self.InputElectrodeNumber.setHtml(_translate("IndividualChannelInfo", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
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
        self.LabelElectrodeInfo.setText(_translate("IndividualChannelInfo", "Extra information:"))
        self.totalSamples.setText(_translate("IndividualChannelInfo", "TextLabel"))
from pyqtgraph import PlotWidget