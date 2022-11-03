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

class ElectrodeListInformation(QWidget):

    session_parent = None
    current_elec = 0
    current_row = 0
    current_col = 0

    sortOption = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./src/layouts/AllChannelsList.ui", self)

        self.chooseSortOption.activated.connect(self.setSortOption)

        data = [
            [4, 9, 2],
            [1, 0, 0],
            [3, 5, 0],
            [3, 3, 2],
            [7, 8, 9],
            [4, 9, 2],
            [1, 0, 0],
            [3, 5, 0],
            [3, 3, 2],
            [7, 8, 9],
            [4, 9, 2],
            [1, 0, 0],
            [3, 5, 0],
            [3, 3, 2],
            [7, 8, 9],
            [4, 9, 2],
            [1, 0, 0],
            [3, 5, 0],
            [3, 3, 2],
            [7, 8, 9]
        ]
        self.model = TableModel(data)
        self.electrodeTable.setModel(self.model)


    def setSessionParent(self, session_parent):
        self.session_parent = session_parent
        self.setupCharts()

    def setupCharts(self):
        pass

    def update(self):
        pass

    def setSortOption(self):
        self.sortOption = self.chooseSortOption.currentText()
        print("SORT OPTION: " + self.sortOption)
        self.update()

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])



