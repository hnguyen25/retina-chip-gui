from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
import numpy as np
import pyqtgraph as pg
import time
from src.model.spike_detection import *
from src.model.DC1DataContainer import *

class GUIProfiler(QWidget):
    app = None
    current_elec = 0
    current_row = 0
    current_col = 0
    model = None

    sortOption = None

    profiler_charts = {}
    profiler_charts_update_mapping = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./src/view/layouts/GUIProfiler.ui", self)
        self.sort_by = "row"
        ## self.chooseSortOption.activated.connect(self.setSortOption)

        self.profiler_charts = {
            "profiling_list": self.profiling_list,
            "profiling_plot": self.profiling_plot,
            "profiling_table": self.profiling_table
        }
        self.profiler_charts_update_mapping = {
            "profiling_list": None,
            "profiling_plot": None,
            "profiling_table": self.updateProfilingLog
        }

    def setSessionParent(self, session_parent):
        self.app = session_parent
        self.model = DataFrameModel(self.app.profiling_df)
        self.profiler_charts["profiling_table"].setModel(self.model)

    def update(self):
        for chart in self.profiler_charts_update_mapping.keys():
            if self.profiler_charts_update_mapping[chart] is not None:
                self.profiler_charts_update_mapping[chart]()

    def updateProfilingLog(self):
        print('updateProfilingLog()')
        print(self.app.profiling_df)
        self.model = DataFrameModel(self.app.profiling_df)
        self.model.sort(1)
        self.profiling_table.setModel(self.model)

    def setSortOption(self):
        self.sortOption = self.chooseSortOption.currentText()
        print("SORT OPTION: " + self.sortOption)
        self.update()

    def update_theme(self, current_theme, themes):
        background_color = themes[current_theme]["background_color"]
        background_border = themes[current_theme]["background_borders"]
        button_color = themes[current_theme]["button"]
        font_color = themes[current_theme]["font_color"]
        #self.setStyleSheet("background-color: " + background_border)

        self.profiler_charts["profiling_plot"].setBackground(background_color)


# from this stack overflow post:
# https://stackoverflow.com/questions/44603119/how-to-display-a-pandas-data-frame-with-pyqt5-pyside2
class DataFrameModel(QtCore.QAbstractTableModel):
    DtypeRole = QtCore.Qt.UserRole + 1000
    ValueRole = QtCore.Qt.UserRole + 1001

    def __init__(self, df=pd.DataFrame(), parent=None):
        super(DataFrameModel, self).__init__(parent)
        self._dataframe = df

    def setDataFrame(self, dataframe):
        self.beginResetModel()
        self._dataframe = dataframe.copy()
        self.endResetModel()

    def dataFrame(self):
        return self._dataframe

    dataFrame = QtCore.pyqtProperty(pd.DataFrame, fget=dataFrame, fset=setDataFrame)

    @QtCore.pyqtSlot(int, QtCore.Qt.Orientation, result=str)
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._dataframe.columns[section]
            else:
                return str(self._dataframe.index[section])
        return QtCore.QVariant()

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._dataframe.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return self._dataframe.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount() \
                                       and 0 <= index.column() < self.columnCount()):
            return QtCore.QVariant()
        row = self._dataframe.index[index.row()]
        col = self._dataframe.columns[index.column()]
        dt = self._dataframe[col].dtype

        val = self._dataframe.iloc[row][col]
        if role == QtCore.Qt.DisplayRole:
            return str(val)
        elif role == DataFrameModel.ValueRole:
            return val
        if role == DataFrameModel.DtypeRole:
            return dt
        return QtCore.QVariant()

    def roleNames(self):
        roles = {
            QtCore.Qt.DisplayRole: b'display',
            DataFrameModel.DtypeRole: b'dtype',
            DataFrameModel.ValueRole: b'value'
        }
        return roles

    # see MainWindow.update_theme() for how this is called
    def update_theme(self, current_theme, themes):

        pass