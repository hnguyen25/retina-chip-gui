# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(936, 618)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_top = QtWidgets.QHBoxLayout()
        self.horizontalLayout_top.setObjectName("horizontalLayout_top")
        self.arrayMap = PlotWidget(self.centralwidget)
        self.arrayMap.setObjectName("arrayMap")
        self.horizontalLayout_top.addWidget(self.arrayMap)
        self.traceplot_verticalLayout = QtWidgets.QVBoxLayout()
        self.traceplot_verticalLayout.setObjectName("traceplot_verticalLayout")
        self.traceplot_1 = PlotWidget(self.centralwidget)
        self.traceplot_1.setObjectName("traceplot_1")
        self.traceplot_verticalLayout.addWidget(self.traceplot_1)
        self.traceplot_2 = PlotWidget(self.centralwidget)
        self.traceplot_2.setObjectName("traceplot_2")
        self.traceplot_verticalLayout.addWidget(self.traceplot_2)
        self.traceplot_3 = PlotWidget(self.centralwidget)
        self.traceplot_3.setObjectName("traceplot_3")
        self.traceplot_verticalLayout.addWidget(self.traceplot_3)
        self.traceplot_4 = PlotWidget(self.centralwidget)
        self.traceplot_4.setObjectName("traceplot_4")
        self.traceplot_verticalLayout.addWidget(self.traceplot_4)
        self.horizontalLayout_top.addLayout(self.traceplot_verticalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_top)
        self.horizontalLayout_bottom = QtWidgets.QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName("horizontalLayout_bottom")
        self.spikeRatePlot = PlotWidget(self.centralwidget)
        self.spikeRatePlot.setObjectName("spikeRatePlot")
        self.horizontalLayout_bottom.addWidget(self.spikeRatePlot)
        self.miniMapWidget = PlotWidget(self.centralwidget)
        self.miniMapWidget.setObjectName("miniMapWidget")
        self.horizontalLayout_bottom.addWidget(self.miniMapWidget)
        self.verticalLayout.addLayout(self.horizontalLayout_bottom)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 936, 24))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuLoad_offline_data = QtWidgets.QMenu(self.menuFile)
        self.menuLoad_offline_data.setObjectName("menuLoad_offline_data")
        self.menuSave_as = QtWidgets.QMenu(self.menuFile)
        self.menuSave_as.setObjectName("menuSave_as")
        self.menuExport_image = QtWidgets.QMenu(self.menuFile)
        self.menuExport_image.setObjectName("menuExport_image")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menu_view_arraymap = QtWidgets.QMenu(self.menuView)
        self.menu_view_arraymap.setObjectName("menu_view_arraymap")
        self.menu_view_channels = QtWidgets.QMenu(self.menuView)
        self.menu_view_channels.setObjectName("menu_view_channels")
        self.menu_view_spikerate = QtWidgets.QMenu(self.menuView)
        self.menu_view_spikerate.setObjectName("menu_view_spikerate")
        self.menu_view_electrodeminimap = QtWidgets.QMenu(self.menuView)
        self.menu_view_electrodeminimap.setObjectName("menu_view_electrodeminimap")
        self.menuWindow = QtWidgets.QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")
        self.menu_topleft = QtWidgets.QMenu(self.menuWindow)
        self.menu_topleft.setObjectName("menu_topleft")
        self.menu_topright = QtWidgets.QMenu(self.menuWindow)
        self.menu_topright.setObjectName("menu_topright")
        self.menu_bottomleft = QtWidgets.QMenu(self.menuWindow)
        self.menu_bottomleft.setObjectName("menu_bottomleft")
        self.menu_bottomright = QtWidgets.QMenu(self.menuWindow)
        self.menu_bottomright.setObjectName("menu_bottomright")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuFilter_design = QtWidgets.QMenu(self.menuSettings)
        self.menuFilter_design.setObjectName("menuFilter_design")
        mainWindow.setMenuBar(self.menubar)
        self.actionNew_session = QtWidgets.QAction(mainWindow)
        self.actionNew_session.setObjectName("actionNew_session")
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
        self.actionAnalysis_parameters = QtWidgets.QAction(mainWindow)
        self.actionAnalysis_parameters.setObjectName("actionAnalysis_parameters")
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
        self.menuLoad_offline_data.addAction(self.action_npz)
        self.menuLoad_offline_data.addAction(self.action_mat)
        self.menuLoad_offline_data.addAction(self.action_csv)
        self.menuSave_as.addAction(self.action_save_npz)
        self.menuSave_as.addAction(self.action_save_mat)
        self.menuSave_as.addAction(self.action_save_csv)
        self.menuExport_image.addAction(self.actionEntire_window)
        self.menuExport_image.addAction(self.actionWindow_1)
        self.menuExport_image.addAction(self.actionWindow_2)
        self.menuExport_image.addAction(self.actionWindow_3)
        self.menuExport_image.addAction(self.actionWindow_4)
        self.menuFile.addAction(self.actionNew_session)
        self.menuFile.addAction(self.menuLoad_offline_data.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.menuSave_as.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuExport_image.menuAction())
        self.menuEdit.addAction(self.actionPreferences)
        self.menuEdit.addAction(self.actionAnalysis_parameters)
        self.menu_view_arraymap.addAction(self.actionParameter_1)
        self.menu_view_arraymap.addAction(self.actionParameter_2)
        self.menu_view_channels.addAction(self.actionParameter_4)
        self.menu_view_channels.addAction(self.actionParameter_5)
        self.menu_view_channels.addSeparator()
        self.menu_view_channels.addAction(self.actionSpike_threshold)
        self.menu_view_channels.addAction(self.actionTime_window)
        self.menu_view_spikerate.addAction(self.actionParameter_6)
        self.menu_view_spikerate.addAction(self.actionParameter_7)
        self.menu_view_electrodeminimap.addAction(self.actionParameter_8)
        self.menu_view_electrodeminimap.addAction(self.actionParameter_9)
        self.menuView.addAction(self.menu_view_arraymap.menuAction())
        self.menuView.addAction(self.menu_view_channels.menuAction())
        self.menuView.addAction(self.menu_view_spikerate.menuAction())
        self.menuView.addAction(self.menu_view_electrodeminimap.menuAction())
        self.menuView.addSeparator()
        self.menu_topleft.addAction(self.action_tl_arraymap)
        self.menu_topleft.addAction(self.action_tl_channels)
        self.menu_topleft.addAction(self.action_tl_spikerate)
        self.menu_topleft.addAction(self.action_tl_electrodeminimap)
        self.menu_topleft.addAction(self.action_tl_tracesearch)
        self.menu_topright.addAction(self.action_tr_arraymap)
        self.menu_topright.addAction(self.action_tr_channels)
        self.menu_topright.addAction(self.action_tr_spikerate)
        self.menu_topright.addAction(self.action_tr_electrodeminimap)
        self.menu_topright.addAction(self.action_tr_tracesearch)
        self.menu_bottomleft.addAction(self.action_bl_arraymap)
        self.menu_bottomleft.addAction(self.action_bl_channels)
        self.menu_bottomleft.addAction(self.action_bl_spikerate)
        self.menu_bottomleft.addAction(self.action_bl_electrodeminimap)
        self.menu_bottomleft.addAction(self.action_bl_tracesearch)
        self.menu_bottomright.addAction(self.action_br_arraymap_2)
        self.menu_bottomright.addAction(self.action_br_channels_2)
        self.menu_bottomright.addAction(self.action_br_spikerate_2)
        self.menu_bottomright.addAction(self.action_br_electrodeminimap_2)
        self.menu_bottomright.addAction(self.action_br_tracesearch_2)
        self.menuWindow.addAction(self.action_changeLayout)
        self.menuWindow.addAction(self.menu_topleft.menuAction())
        self.menuWindow.addAction(self.menu_topright.menuAction())
        self.menuWindow.addAction(self.menu_bottomleft.menuAction())
        self.menuWindow.addAction(self.menu_bottomright.menuAction())
        self.menuWindow.addSeparator()
        self.menuWindow.addAction(self.actionToggle_light_dark_mode)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuFilter_design.addAction(self.action_hierlemann)
        self.menuFilter_design.addAction(self.action_modifiedhierlemann)
        self.menuFilter_design.addAction(self.action_Highpass)
        self.menuFilter_design.addAction(self.action_H0Bandpass)
        self.menuFilter_design.addAction(self.action_Auto)
        self.menuFilter_design.addAction(self.action_FastBandpass)
        self.menuFilter_design.addAction(self.action_FasterBandpass)
        self.menuFilter_design.addAction(self.action_Litke)
        self.menuFilter_design.addAction(self.action_None)
        self.menuSettings.addAction(self.menuFilter_design.menuAction())
        self.menuSettings.addAction(self.actionSpike_detection)
        self.menuSettings.addAction(self.actionToggle_profiling)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "DC1 Visualization"))
        self.menuFile.setTitle(_translate("mainWindow", "File"))
        self.menuLoad_offline_data.setTitle(_translate("mainWindow", "Load offline data..."))
        self.menuSave_as.setTitle(_translate("mainWindow", "Save as..."))
        self.menuExport_image.setTitle(_translate("mainWindow", "Export image..."))
        self.menuEdit.setTitle(_translate("mainWindow", "Edit"))
        self.menuView.setTitle(_translate("mainWindow", "View"))
        self.menu_view_arraymap.setTitle(_translate("mainWindow", "Array Map"))
        self.menu_view_channels.setTitle(_translate("mainWindow", "Channel Traces"))
        self.menu_view_spikerate.setTitle(_translate("mainWindow", "Spike Rate Plot"))
        self.menu_view_electrodeminimap.setTitle(_translate("mainWindow", "Electrode Minimap"))
        self.menuWindow.setTitle(_translate("mainWindow", "Window"))
        self.menu_topleft.setTitle(_translate("mainWindow", "Top left..."))
        self.menu_topright.setTitle(_translate("mainWindow", "Top right..."))
        self.menu_bottomleft.setTitle(_translate("mainWindow", "Bottom left..."))
        self.menu_bottomright.setTitle(_translate("mainWindow", "Bottom right..."))
        self.menuHelp.setTitle(_translate("mainWindow", "Help"))
        self.menuSettings.setTitle(_translate("mainWindow", "Settings"))
        self.menuFilter_design.setTitle(_translate("mainWindow", "Filter"))
        self.actionNew_session.setText(_translate("mainWindow", "New real-time session..."))
        self.actionLoad_real_time_stream.setText(_translate("mainWindow", "Load real-time stream..."))
        self.action_changeLayout.setText(_translate("mainWindow", "Change layout"))
        self.actionDocumentation.setText(_translate("mainWindow", "Documentation"))
        self.actionParameter_1.setText(_translate("mainWindow", "Parameter 1"))
        self.actionParameter_2.setText(_translate("mainWindow", "Parameter 2"))
        self.actionParameter_3.setText(_translate("mainWindow", "Parameter 3"))
        self.actionPreferences.setText(_translate("mainWindow", "Preferences..."))
        self.actionAnalysis_parameters.setText(_translate("mainWindow", "Analysis parameters"))
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
from pyqtgraph import PlotWidget