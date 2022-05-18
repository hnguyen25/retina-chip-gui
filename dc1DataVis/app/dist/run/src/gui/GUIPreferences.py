# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUIPreferences.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GuiPreferences(object):
    def setupUi(self, GuiPreferences):
        GuiPreferences.setObjectName("GuiPreferences")
        GuiPreferences.resize(370, 291)
        self.DialogButtons = QtWidgets.QDialogButtonBox(GuiPreferences)
        self.DialogButtons.setGeometry(QtCore.QRect(10, 250, 341, 32))
        self.DialogButtons.setOrientation(QtCore.Qt.Horizontal)
        self.DialogButtons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.DialogButtons.setObjectName("DialogButtons")
        self.label = QtWidgets.QLabel(GuiPreferences)
        self.label.setGeometry(QtCore.QRect(10, 10, 161, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(GuiPreferences)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 151, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(GuiPreferences)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 141, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(GuiPreferences)
        self.label_4.setGeometry(QtCore.QRect(10, 170, 141, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(GuiPreferences)
        self.label_5.setGeometry(QtCore.QRect(10, 210, 141, 31))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(GuiPreferences)
        self.label_6.setGeometry(QtCore.QRect(10, 130, 141, 31))
        self.label_6.setObjectName("label_6")
        self.chooseTheme = QtWidgets.QComboBox(GuiPreferences)
        self.chooseTheme.setGeometry(QtCore.QRect(160, 10, 191, 26))
        self.chooseTheme.setObjectName("chooseTheme")
        self.chooseTheme.addItem("")
        self.chooseTheme.addItem("")
        self.chooseTheme.addItem("")
        self.chooseTheme.addItem("")
        self.chooseTheme.addItem("")
        self.choosePerformanceProfiling = QtWidgets.QComboBox(GuiPreferences)
        self.choosePerformanceProfiling.setGeometry(QtCore.QRect(160, 50, 191, 26))
        self.choosePerformanceProfiling.setObjectName("choosePerformanceProfiling")
        self.choosePerformanceProfiling.addItem("")
        self.choosePerformanceProfiling.addItem("")
        self.chooseParallelization = QtWidgets.QComboBox(GuiPreferences)
        self.chooseParallelization.setGeometry(QtCore.QRect(160, 90, 191, 26))
        self.chooseParallelization.setObjectName("chooseParallelization")
        self.chooseParallelization.addItem("")
        self.chooseParallelization.addItem("")
        self.chooseParallelization.addItem("")
        self.chooseParallelization.addItem("")
        self.chooseColorMap = QtWidgets.QComboBox(GuiPreferences)
        self.chooseColorMap.setGeometry(QtCore.QRect(160, 130, 191, 26))
        self.chooseColorMap.setObjectName("chooseColorMap")
        self.chooseColorMap.addItem("")
        self.choosePlotLineThickness = QtWidgets.QSlider(GuiPreferences)
        self.choosePlotLineThickness.setGeometry(QtCore.QRect(170, 170, 141, 22))
        self.choosePlotLineThickness.setOrientation(QtCore.Qt.Horizontal)
        self.choosePlotLineThickness.setObjectName("choosePlotLineThickness")
        self.chooseTraceTimeWindow = QtWidgets.QSlider(GuiPreferences)
        self.chooseTraceTimeWindow.setGeometry(QtCore.QRect(170, 210, 141, 22))
        self.chooseTraceTimeWindow.setOrientation(QtCore.Qt.Horizontal)
        self.chooseTraceTimeWindow.setObjectName("chooseTraceTimeWindow")
        self.LabelPlotLineThickness = QtWidgets.QLabel(GuiPreferences)
        self.LabelPlotLineThickness.setGeometry(QtCore.QRect(320, 160, 31, 41))
        self.LabelPlotLineThickness.setAlignment(QtCore.Qt.AlignCenter)
        self.LabelPlotLineThickness.setObjectName("LabelPlotLineThickness")
        self.LabelTraceTimeWindow = QtWidgets.QLabel(GuiPreferences)
        self.LabelTraceTimeWindow.setGeometry(QtCore.QRect(320, 200, 31, 41))
        self.LabelTraceTimeWindow.setAlignment(QtCore.Qt.AlignCenter)
        self.LabelTraceTimeWindow.setObjectName("LabelTraceTimeWindow")
        self.label.setBuddy(self.chooseTheme)
        self.label_2.setBuddy(self.choosePerformanceProfiling)
        self.label_3.setBuddy(self.chooseParallelization)
        self.label_4.setBuddy(self.choosePlotLineThickness)
        self.label_5.setBuddy(self.chooseTraceTimeWindow)
        self.label_6.setBuddy(self.chooseColorMap)

        self.retranslateUi(GuiPreferences)
        self.DialogButtons.accepted.connect(GuiPreferences.accept) # type: ignore
        self.DialogButtons.rejected.connect(GuiPreferences.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(GuiPreferences)
        GuiPreferences.setTabOrder(self.chooseTheme, self.choosePerformanceProfiling)
        GuiPreferences.setTabOrder(self.choosePerformanceProfiling, self.chooseParallelization)
        GuiPreferences.setTabOrder(self.chooseParallelization, self.chooseColorMap)
        GuiPreferences.setTabOrder(self.chooseColorMap, self.choosePlotLineThickness)
        GuiPreferences.setTabOrder(self.choosePlotLineThickness, self.chooseTraceTimeWindow)

    def retranslateUi(self, GuiPreferences):
        _translate = QtCore.QCoreApplication.translate
        GuiPreferences.setWindowTitle(_translate("GuiPreferences", "GUI Preferences"))
        self.label.setText(_translate("GuiPreferences", "Theme"))
        self.label_2.setText(_translate("GuiPreferences", "Performance profiling"))
        self.label_3.setText(_translate("GuiPreferences", "Parallelization"))
        self.label_4.setText(_translate("GuiPreferences", "Plot line thickness"))
        self.label_5.setText(_translate("GuiPreferences", "Trace time window"))
        self.label_6.setText(_translate("GuiPreferences", "Color map"))
        self.chooseTheme.setItemText(0, _translate("GuiPreferences", "Light"))
        self.chooseTheme.setItemText(1, _translate("GuiPreferences", "Solarized"))
        self.chooseTheme.setItemText(2, _translate("GuiPreferences", "Nord"))
        self.chooseTheme.setItemText(3, _translate("GuiPreferences", "Dark"))
        self.chooseTheme.setItemText(4, _translate("GuiPreferences", "True Black"))
        self.choosePerformanceProfiling.setItemText(0, _translate("GuiPreferences", "No"))
        self.choosePerformanceProfiling.setItemText(1, _translate("GuiPreferences", "Yes"))
        self.chooseParallelization.setItemText(0, _translate("GuiPreferences", "Yes, everything"))
        self.chooseParallelization.setItemText(1, _translate("GuiPreferences", "Yes, only filtering"))
        self.chooseParallelization.setItemText(2, _translate("GuiPreferences", "Yes, only preprocessing"))
        self.chooseParallelization.setItemText(3, _translate("GuiPreferences", "No"))
        self.chooseColorMap.setItemText(0, _translate("GuiPreferences", "Jet"))
        self.LabelPlotLineThickness.setText(_translate("GuiPreferences", "0"))
        self.LabelTraceTimeWindow.setText(_translate("GuiPreferences", "0"))
