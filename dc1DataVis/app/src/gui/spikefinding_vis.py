# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spikefinding_vis.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(936, 585)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.r5c3 = PlotWidget(self.centralwidget)
        self.r5c3.setObjectName("r5c3")
        self.gridLayout.addWidget(self.r5c3, 5, 2, 1, 1)
        self.r2c4 = PlotWidget(self.centralwidget)
        self.r2c4.setObjectName("r2c4")
        self.gridLayout.addWidget(self.r2c4, 2, 3, 1, 1)
        self.r2c2 = PlotWidget(self.centralwidget)
        self.r2c2.setObjectName("r2c2")
        self.gridLayout.addWidget(self.r2c2, 2, 1, 1, 1)
        self.r3c1 = PlotWidget(self.centralwidget)
        self.r3c1.setObjectName("r3c1")
        self.gridLayout.addWidget(self.r3c1, 3, 0, 1, 1)
        self.r4c4 = PlotWidget(self.centralwidget)
        self.r4c4.setObjectName("r4c4")
        self.gridLayout.addWidget(self.r4c4, 4, 3, 1, 1)
        self.r5c2 = PlotWidget(self.centralwidget)
        self.r5c2.setObjectName("r5c2")
        self.gridLayout.addWidget(self.r5c2, 5, 1, 1, 1)
        self.r3c6 = PlotWidget(self.centralwidget)
        self.r3c6.setObjectName("r3c6")
        self.gridLayout.addWidget(self.r3c6, 3, 5, 1, 1)
        self.r1c5 = PlotWidget(self.centralwidget)
        self.r1c5.setObjectName("r1c5")
        self.gridLayout.addWidget(self.r1c5, 1, 4, 1, 1)
        self.r2c6 = PlotWidget(self.centralwidget)
        self.r2c6.setObjectName("r2c6")
        self.gridLayout.addWidget(self.r2c6, 2, 5, 1, 1)
        self.r1c1 = PlotWidget(self.centralwidget)
        self.r1c1.setObjectName("r1c1")
        self.gridLayout.addWidget(self.r1c1, 1, 0, 1, 1)
        self.r5c5 = PlotWidget(self.centralwidget)
        self.r5c5.setObjectName("r5c5")
        self.gridLayout.addWidget(self.r5c5, 5, 4, 1, 1)
        self.r1c4 = PlotWidget(self.centralwidget)
        self.r1c4.setObjectName("r1c4")
        self.gridLayout.addWidget(self.r1c4, 1, 3, 1, 1)
        self.r1c3 = PlotWidget(self.centralwidget)
        self.r1c3.setObjectName("r1c3")
        self.gridLayout.addWidget(self.r1c3, 1, 2, 1, 1)
        self.r1c2 = PlotWidget(self.centralwidget)
        self.r1c2.setObjectName("r1c2")
        self.gridLayout.addWidget(self.r1c2, 1, 1, 1, 1)
        self.r3c2 = PlotWidget(self.centralwidget)
        self.r3c2.setObjectName("r3c2")
        self.gridLayout.addWidget(self.r3c2, 3, 1, 1, 1)
        self.r1c6 = PlotWidget(self.centralwidget)
        self.r1c6.setObjectName("r1c6")
        self.gridLayout.addWidget(self.r1c6, 1, 5, 1, 1)
        self.r4c2 = PlotWidget(self.centralwidget)
        self.r4c2.setObjectName("r4c2")
        self.gridLayout.addWidget(self.r4c2, 4, 1, 1, 1)
        self.r5c4 = PlotWidget(self.centralwidget)
        self.r5c4.setObjectName("r5c4")
        self.gridLayout.addWidget(self.r5c4, 5, 3, 1, 1)
        self.horizontalLayoutC4 = QtWidgets.QHBoxLayout()
        self.horizontalLayoutC4.setObjectName("horizontalLayoutC4")
        self.atTimeWindowButton = QtWidgets.QPushButton(self.centralwidget)
        self.atTimeWindowButton.setObjectName("atTimeWindowButton")
        self.horizontalLayoutC4.addWidget(self.atTimeWindowButton)
        self.gridLayout.addLayout(self.horizontalLayoutC4, 0, 3, 1, 1)
        self.r2c3 = PlotWidget(self.centralwidget)
        self.r2c3.setObjectName("r2c3")
        self.gridLayout.addWidget(self.r2c3, 2, 2, 1, 1)
        self.horizontalLayoutC5 = QtWidgets.QHBoxLayout()
        self.horizontalLayoutC5.setObjectName("horizontalLayoutC5")
        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.resetButton.setObjectName("resetButton")
        self.horizontalLayoutC5.addWidget(self.resetButton)
        self.gridLayout.addLayout(self.horizontalLayoutC5, 0, 4, 1, 1)
        self.r5c1 = PlotWidget(self.centralwidget)
        self.r5c1.setObjectName("r5c1")
        self.gridLayout.addWidget(self.r5c1, 5, 0, 1, 1)
        self.r2c1 = PlotWidget(self.centralwidget)
        self.r2c1.setObjectName("r2c1")
        self.gridLayout.addWidget(self.r2c1, 2, 0, 1, 1)
        self.horizontalLayoutC6 = QtWidgets.QHBoxLayout()
        self.horizontalLayoutC6.setObjectName("horizontalLayoutC6")
        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.backButton.setObjectName("backButton")
        self.horizontalLayoutC6.addWidget(self.backButton)
        self.nextButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextButton.setMaximumSize(QtCore.QSize(60, 16777215))
        self.nextButton.setObjectName("nextButton")
        self.horizontalLayoutC6.addWidget(self.nextButton)
        self.gridLayout.addLayout(self.horizontalLayoutC6, 0, 5, 1, 1)
        self.r3c5 = PlotWidget(self.centralwidget)
        self.r3c5.setObjectName("r3c5")
        self.gridLayout.addWidget(self.r3c5, 3, 4, 1, 1)
        self.r4c1 = PlotWidget(self.centralwidget)
        self.r4c1.setObjectName("r4c1")
        self.gridLayout.addWidget(self.r4c1, 4, 0, 1, 1)
        self.horizontalLayoutC3 = QtWidgets.QHBoxLayout()
        self.horizontalLayoutC3.setObjectName("horizontalLayoutC3")
        self.yScaleButton = QtWidgets.QPushButton(self.centralwidget)
        self.yScaleButton.setObjectName("yScaleButton")
        self.horizontalLayoutC3.addWidget(self.yScaleButton)
        self.gridLayout.addLayout(self.horizontalLayoutC3, 0, 2, 1, 1)
        self.r2c5 = PlotWidget(self.centralwidget)
        self.r2c5.setObjectName("r2c5")
        self.gridLayout.addWidget(self.r2c5, 2, 4, 1, 1)
        self.r4c5 = PlotWidget(self.centralwidget)
        self.r4c5.setObjectName("r4c5")
        self.gridLayout.addWidget(self.r4c5, 4, 4, 1, 1)
        self.r4c3 = PlotWidget(self.centralwidget)
        self.r4c3.setObjectName("r4c3")
        self.gridLayout.addWidget(self.r4c3, 4, 2, 1, 1)
        self.r3c3 = PlotWidget(self.centralwidget)
        self.r3c3.setObjectName("r3c3")
        self.gridLayout.addWidget(self.r3c3, 3, 2, 1, 1)
        self.r4c6 = PlotWidget(self.centralwidget)
        self.r4c6.setObjectName("r4c6")
        self.gridLayout.addWidget(self.r4c6, 4, 5, 1, 1)
        self.horizontalLayoutC2 = QtWidgets.QHBoxLayout()
        self.horizontalLayoutC2.setObjectName("horizontalLayoutC2")
        self.nextFigButton = QtWidgets.QPushButton(self.centralwidget)
        self.nextFigButton.setObjectName("nextFigButton")
        self.horizontalLayoutC2.addWidget(self.nextFigButton)
        self.gridLayout.addLayout(self.horizontalLayoutC2, 0, 1, 1, 1)
        self.r5c6 = PlotWidget(self.centralwidget)
        self.r5c6.setObjectName("r5c6")
        self.gridLayout.addWidget(self.r5c6, 5, 5, 1, 1)
        self.r3c4 = PlotWidget(self.centralwidget)
        self.r3c4.setObjectName("r3c4")
        self.gridLayout.addWidget(self.r3c4, 3, 3, 1, 1)
        self.FigureLabel = QtWidgets.QLabel(self.centralwidget)
        self.FigureLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        self.FigureLabel.setText("")
        self.FigureLabel.setObjectName("FigureLabel")
        self.gridLayout.addWidget(self.FigureLabel, 0, 0, 1, 1)
        self.r6c1 = PlotWidget(self.centralwidget)
        self.r6c1.setObjectName("r6c1")
        self.gridLayout.addWidget(self.r6c1, 6, 0, 1, 1)
        self.r6c2 = PlotWidget(self.centralwidget)
        self.r6c2.setObjectName("r6c2")
        self.gridLayout.addWidget(self.r6c2, 6, 1, 1, 1)
        self.r6c3 = PlotWidget(self.centralwidget)
        self.r6c3.setObjectName("r6c3")
        self.gridLayout.addWidget(self.r6c3, 6, 2, 1, 1)
        self.r6c4 = PlotWidget(self.centralwidget)
        self.r6c4.setObjectName("r6c4")
        self.gridLayout.addWidget(self.r6c4, 6, 3, 1, 1)
        self.r6c5 = PlotWidget(self.centralwidget)
        self.r6c5.setObjectName("r6c5")
        self.gridLayout.addWidget(self.r6c5, 6, 4, 1, 1)
        self.r6c6 = PlotWidget(self.centralwidget)
        self.r6c6.setObjectName("r6c6")
        self.gridLayout.addWidget(self.r6c6, 6, 5, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 936, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        mainWindow.setMenuBar(self.menubar)
        self.actionUpdateSession = QtWidgets.QAction(mainWindow)
        self.actionUpdateSession.setObjectName("actionUpdateSession")
        self.actionLoad_real_time_stream = QtWidgets.QAction(mainWindow)
        self.actionLoad_real_time_stream.setObjectName("actionLoad_real_time_stream")
        self.action_changeLayout = QtWidgets.QAction(mainWindow)
        self.action_changeLayout.setObjectName("action_changeLayout")
        self.actionDocumentation = QtWidgets.QAction(mainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.actionParameter_1 = QtWidgets.QAction(mainWindow)
        self.actionParameter_1.setObjectName("actionParameter_1")
        self.actionParameter_2 = QtWidgets.QAction(mainWindow)
        self.actionParameter_2.setObjectName("actionParameter_2")
        self.actionParameter_3 = QtWidgets.QAction(mainWindow)
        self.actionParameter_3.setObjectName("actionParameter_3")
        self.actionPreferences = QtWidgets.QAction(mainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionAnalysisParameters = QtWidgets.QAction(mainWindow)
        self.actionAnalysisParameters.setObjectName("actionAnalysisParameters")
        self.actionSave = QtWidgets.QAction(mainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionExport_to = QtWidgets.QAction(mainWindow)
        self.actionExport_to.setObjectName("actionExport_to")
        self.actionParameter_4 = QtWidgets.QAction(mainWindow)
        self.actionParameter_4.setObjectName("actionParameter_4")
        self.actionParameter_5 = QtWidgets.QAction(mainWindow)
        self.actionParameter_5.setObjectName("actionParameter_5")
        self.actionParameter_6 = QtWidgets.QAction(mainWindow)
        self.actionParameter_6.setObjectName("actionParameter_6")
        self.actionParameter_7 = QtWidgets.QAction(mainWindow)
        self.actionParameter_7.setObjectName("actionParameter_7")
        self.actionParameter = QtWidgets.QAction(mainWindow)
        self.actionParameter.setObjectName("actionParameter")
        self.actionParameter_8 = QtWidgets.QAction(mainWindow)
        self.actionParameter_8.setObjectName("actionParameter_8")
        self.actionParameter_9 = QtWidgets.QAction(mainWindow)
        self.actionParameter_9.setObjectName("actionParameter_9")
        self.actionParameter_10 = QtWidgets.QAction(mainWindow)
        self.actionParameter_10.setObjectName("actionParameter_10")
        self.action_tl_arraymap = QtWidgets.QAction(mainWindow)
        self.action_tl_arraymap.setObjectName("action_tl_arraymap")
        self.action_tr_arraymap = QtWidgets.QAction(mainWindow)
        self.action_tr_arraymap.setObjectName("action_tr_arraymap")
        self.action_bl_arraymap = QtWidgets.QAction(mainWindow)
        self.action_bl_arraymap.setObjectName("action_bl_arraymap")
        self.action_br_arraymap_2 = QtWidgets.QAction(mainWindow)
        self.action_br_arraymap_2.setObjectName("action_br_arraymap_2")
        self.action_tl_channels = QtWidgets.QAction(mainWindow)
        self.action_tl_channels.setObjectName("action_tl_channels")
        self.action_bl_channels = QtWidgets.QAction(mainWindow)
        self.action_bl_channels.setObjectName("action_bl_channels")
        self.action_br_channels_2 = QtWidgets.QAction(mainWindow)
        self.action_br_channels_2.setObjectName("action_br_channels_2")
        self.action_tl_spikerate = QtWidgets.QAction(mainWindow)
        self.action_tl_spikerate.setObjectName("action_tl_spikerate")
        self.action_tl_electrodeminimap = QtWidgets.QAction(mainWindow)
        self.action_tl_electrodeminimap.setObjectName("action_tl_electrodeminimap")
        self.action_hierlemann = QtWidgets.QAction(mainWindow)
        self.action_hierlemann.setObjectName("action_hierlemann")
        self.action_modifiedhierlemann = QtWidgets.QAction(mainWindow)
        self.action_modifiedhierlemann.setObjectName("action_modifiedhierlemann")
        self.action_Highpass = QtWidgets.QAction(mainWindow)
        self.action_Highpass.setObjectName("action_Highpass")
        self.actionSpike_detection = QtWidgets.QAction(mainWindow)
        self.actionSpike_detection.setObjectName("actionSpike_detection")
        self.action_npz = QtWidgets.QAction(mainWindow)
        self.action_npz.setObjectName("action_npz")
        self.action_mat = QtWidgets.QAction(mainWindow)
        self.action_mat.setObjectName("action_mat")
        self.action_save_npz = QtWidgets.QAction(mainWindow)
        self.action_save_npz.setObjectName("action_save_npz")
        self.action_save_mat = QtWidgets.QAction(mainWindow)
        self.action_save_mat.setObjectName("action_save_mat")
        self.action_tr_channels = QtWidgets.QAction(mainWindow)
        self.action_tr_channels.setObjectName("action_tr_channels")
        self.action_tr_spikerate = QtWidgets.QAction(mainWindow)
        self.action_tr_spikerate.setObjectName("action_tr_spikerate")
        self.action_tr_electrodeminimap = QtWidgets.QAction(mainWindow)
        self.action_tr_electrodeminimap.setObjectName("action_tr_electrodeminimap")
        self.action_bl_spikerate = QtWidgets.QAction(mainWindow)
        self.action_bl_spikerate.setObjectName("action_bl_spikerate")
        self.action_bl_electrodeminimap = QtWidgets.QAction(mainWindow)
        self.action_bl_electrodeminimap.setObjectName("action_bl_electrodeminimap")
        self.action_br_spikerate_2 = QtWidgets.QAction(mainWindow)
        self.action_br_spikerate_2.setObjectName("action_br_spikerate_2")
        self.action_br_electrodeminimap_2 = QtWidgets.QAction(mainWindow)
        self.action_br_electrodeminimap_2.setObjectName("action_br_electrodeminimap_2")
        self.action_save_csv = QtWidgets.QAction(mainWindow)
        self.action_save_csv.setObjectName("action_save_csv")
        self.action_csv = QtWidgets.QAction(mainWindow)
        self.action_csv.setObjectName("action_csv")
        self.actionEntire_window = QtWidgets.QAction(mainWindow)
        self.actionEntire_window.setObjectName("actionEntire_window")
        self.actionWindow_1 = QtWidgets.QAction(mainWindow)
        self.actionWindow_1.setObjectName("actionWindow_1")
        self.actionWindow_2 = QtWidgets.QAction(mainWindow)
        self.actionWindow_2.setObjectName("actionWindow_2")
        self.actionWindow_3 = QtWidgets.QAction(mainWindow)
        self.actionWindow_3.setObjectName("actionWindow_3")
        self.actionWindow_4 = QtWidgets.QAction(mainWindow)
        self.actionWindow_4.setObjectName("actionWindow_4")
        self.action_tl_tracesearch = QtWidgets.QAction(mainWindow)
        self.action_tl_tracesearch.setObjectName("action_tl_tracesearch")
        self.action_tr_tracesearch = QtWidgets.QAction(mainWindow)
        self.action_tr_tracesearch.setObjectName("action_tr_tracesearch")
        self.action_bl_tracesearch = QtWidgets.QAction(mainWindow)
        self.action_bl_tracesearch.setObjectName("action_bl_tracesearch")
        self.action_br_tracesearch_2 = QtWidgets.QAction(mainWindow)
        self.action_br_tracesearch_2.setObjectName("action_br_tracesearch_2")
        self.actionToggle_light_dark_mode = QtWidgets.QAction(mainWindow)
        self.actionToggle_light_dark_mode.setObjectName("actionToggle_light_dark_mode")
        self.actionToggle_profiling = QtWidgets.QAction(mainWindow)
        self.actionToggle_profiling.setObjectName("actionToggle_profiling")
        self.action_H0Bandpass = QtWidgets.QAction(mainWindow)
        self.action_H0Bandpass.setObjectName("action_H0Bandpass")
        self.action_Auto = QtWidgets.QAction(mainWindow)
        self.action_Auto.setObjectName("action_Auto")
        self.action_FastBandpass = QtWidgets.QAction(mainWindow)
        self.action_FastBandpass.setObjectName("action_FastBandpass")
        self.action_FasterBandpass = QtWidgets.QAction(mainWindow)
        self.action_FasterBandpass.setObjectName("action_FasterBandpass")
        self.action_Litke = QtWidgets.QAction(mainWindow)
        self.action_Litke.setObjectName("action_Litke")
        self.action_None = QtWidgets.QAction(mainWindow)
        self.action_None.setObjectName("action_None")
        self.actionSpike_threshold = QtWidgets.QAction(mainWindow)
        self.actionSpike_threshold.setObjectName("actionSpike_threshold")
        self.actionTime_window = QtWidgets.QAction(mainWindow)
        self.actionTime_window.setObjectName("actionTime_window")
        self.actionIndividualChannelInfo = QtWidgets.QAction(mainWindow)
        self.actionIndividualChannelInfo.setObjectName("actionIndividualChannelInfo")
        self.actionChannelAmplitudeHistogram = QtWidgets.QAction(mainWindow)
        self.actionChannelAmplitudeHistogram.setObjectName("actionChannelAmplitudeHistogram")
        self.actionToggleDarkMode = QtWidgets.QAction(mainWindow)
        self.actionToggleDarkMode.setObjectName("actionToggleDarkMode")
        self.actionToggleProfiling = QtWidgets.QAction(mainWindow)
        self.actionToggleProfiling.setObjectName("actionToggleProfiling")
        self.actionListElectrodesInfo = QtWidgets.QAction(mainWindow)
        self.actionListElectrodesInfo.setObjectName("actionListElectrodesInfo")
        self.menuFile.addAction(self.actionUpdateSession)
        self.menuEdit.addAction(self.actionPreferences)
        self.menuEdit.addAction(self.actionAnalysisParameters)
        self.menuView.addAction(self.actionIndividualChannelInfo)
        self.menuView.addAction(self.actionListElectrodesInfo)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "DC1 Visualization"))
        self.atTimeWindowButton.setText(_translate("mainWindow", "At Time Window"))
        self.resetButton.setText(_translate("mainWindow", "Reset"))
        self.backButton.setText(_translate("mainWindow", "Back"))
        self.nextButton.setText(_translate("mainWindow", "Next"))
        self.yScaleButton.setText(_translate("mainWindow", "Y Scale"))
        self.nextFigButton.setText(_translate("mainWindow", "Next Fig"))
        self.menuFile.setTitle(_translate("mainWindow", "File"))
        self.menuEdit.setTitle(_translate("mainWindow", "Edit"))
        self.menuView.setTitle(_translate("mainWindow", "View"))
        self.menuHelp.setTitle(_translate("mainWindow", "Help"))
        self.actionUpdateSession.setText(_translate("mainWindow", "New session..."))
        self.actionLoad_real_time_stream.setText(_translate("mainWindow", "Load real-time stream..."))
        self.action_changeLayout.setText(_translate("mainWindow", "Change visualization style..."))
        self.actionDocumentation.setText(_translate("mainWindow", "Documentation"))
        self.actionParameter_1.setText(_translate("mainWindow", "Parameter 1"))
        self.actionParameter_2.setText(_translate("mainWindow", "Parameter 2"))
        self.actionParameter_3.setText(_translate("mainWindow", "Parameter 3"))
        self.actionPreferences.setText(_translate("mainWindow", "Session parameters..."))
        self.actionAnalysisParameters.setText(_translate("mainWindow", "GUI preferences..."))
        self.actionSave.setText(_translate("mainWindow", "Save"))
        self.actionExport_to.setText(_translate("mainWindow", "Export to..."))
        self.actionParameter_4.setText(_translate("mainWindow", "Toggle highlight spikes"))
        self.actionParameter_5.setText(_translate("mainWindow", "Toggle auto axis"))
        self.actionParameter_6.setText(_translate("mainWindow", "Parameter 1"))
        self.actionParameter_7.setText(_translate("mainWindow", "Parameter 2"))
        self.actionParameter.setText(_translate("mainWindow", "Parameter 3"))
        self.actionParameter_8.setText(_translate("mainWindow", "Parameter 1"))
        self.actionParameter_9.setText(_translate("mainWindow", "Parameter 2"))
        self.actionParameter_10.setText(_translate("mainWindow", "Parameter 3"))
        self.action_tl_arraymap.setText(_translate("mainWindow", "Array Map"))
        self.action_tr_arraymap.setText(_translate("mainWindow", "Array Map"))
        self.action_bl_arraymap.setText(_translate("mainWindow", "Array Map"))
        self.action_br_arraymap_2.setText(_translate("mainWindow", "Array Map"))
        self.action_tl_channels.setText(_translate("mainWindow", "Channel Traces"))
        self.action_bl_channels.setText(_translate("mainWindow", "Channel Traces"))
        self.action_br_channels_2.setText(_translate("mainWindow", "Channel Traces"))
        self.action_tl_spikerate.setText(_translate("mainWindow", "Spike Rate Plot"))
        self.action_tl_electrodeminimap.setText(_translate("mainWindow", "Electrode Minimap"))
        self.action_hierlemann.setText(_translate("mainWindow", "Hierlemann"))
        self.action_modifiedhierlemann.setText(_translate("mainWindow", "Modified Hierlemann"))
        self.action_Highpass.setText(_translate("mainWindow", "Highpass"))
        self.actionSpike_detection.setText(_translate("mainWindow", "Spike detection..."))
        self.action_npz.setText(_translate("mainWindow", "Numpy file (.npz)"))
        self.action_mat.setText(_translate("mainWindow", "MATLAB file (.mat)"))
        self.action_save_npz.setText(_translate("mainWindow", "Numpy file (.npz)"))
        self.action_save_mat.setText(_translate("mainWindow", "MATLAB file (.mat)"))
        self.action_tr_channels.setText(_translate("mainWindow", "Channel Traces"))
        self.action_tr_spikerate.setText(_translate("mainWindow", "Spike Rate Plot"))
        self.action_tr_electrodeminimap.setText(_translate("mainWindow", "Electrode Minimap"))
        self.action_bl_spikerate.setText(_translate("mainWindow", "Spike Rate Plot"))
        self.action_bl_electrodeminimap.setText(_translate("mainWindow", "Electrode Minimap"))
        self.action_br_spikerate_2.setText(_translate("mainWindow", "Spike Rate Plot"))
        self.action_br_electrodeminimap_2.setText(_translate("mainWindow", "Electrode Minimap"))
        self.action_save_csv.setText(_translate("mainWindow", "CSV file (.csv)"))
        self.action_csv.setText(_translate("mainWindow", "CSV file (.csv)"))
        self.actionEntire_window.setText(_translate("mainWindow", "Entire window"))
        self.actionWindow_1.setText(_translate("mainWindow", "Window 1"))
        self.actionWindow_2.setText(_translate("mainWindow", "Window 2"))
        self.actionWindow_3.setText(_translate("mainWindow", "Window 3"))
        self.actionWindow_4.setText(_translate("mainWindow", "Window 4"))
        self.action_tl_tracesearch.setText(_translate("mainWindow", "Trace Search"))
        self.action_tr_tracesearch.setText(_translate("mainWindow", "Trace Search"))
        self.action_bl_tracesearch.setText(_translate("mainWindow", "Trace Search"))
        self.action_br_tracesearch_2.setText(_translate("mainWindow", "Trace Search"))
        self.actionToggle_light_dark_mode.setText(_translate("mainWindow", "Toggle light/dark mode"))
        self.actionToggle_profiling.setText(_translate("mainWindow", "Toggle profiling"))
        self.action_H0Bandpass.setText(_translate("mainWindow", "h0 Bandpass"))
        self.action_Auto.setText(_translate("mainWindow", "Auto"))
        self.action_FastBandpass.setText(_translate("mainWindow", "Fast Bandpass"))
        self.action_FasterBandpass.setText(_translate("mainWindow", "Faster Bandpass"))
        self.action_Litke.setText(_translate("mainWindow", "Litke"))
        self.action_None.setText(_translate("mainWindow", "None"))
        self.actionSpike_threshold.setText(_translate("mainWindow", "Spike threshold..."))
        self.actionTime_window.setText(_translate("mainWindow", "Time window..."))
        self.actionIndividualChannelInfo.setText(_translate("mainWindow", "Individual channel info..."))
        self.actionChannelAmplitudeHistogram.setText(_translate("mainWindow", "Channel amplitude histogram..."))
        self.actionToggleDarkMode.setText(_translate("mainWindow", "Toggle dark mode"))
        self.actionToggleProfiling.setText(_translate("mainWindow", "Toggle profiling"))
        self.actionListElectrodesInfo.setText(_translate("mainWindow", "List of electrodes info..."))
from pyqtgraph import PlotWidget
