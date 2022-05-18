from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
import numpy as np
import pyqtgraph as pg

class IndividualChannelInformation(QWidget):

    session_parent = None
    current_elec = 0
    current_row = 0
    current_col = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./src/gui/IndividualChannelWindow.ui", self)

        self.InputElectrodeNumber.textChanged.connect(self.setElecNumber)
        self.InputElectrodeRow.textChanged.connect(self.setElecRow)
        self.InputElectrodeCol.textChanged.connect(self.setElecCol)


    def setSessionParent(self, session_parent):
        self.session_parent = session_parent
        self.setupCharts()

    def setupCharts(self):
        self.AmplitudeHistPlot.setBackground('w')
        vals = self.session_parent.LoadedData.array_stats['noise_std']
        vals = vals[np.nonzero(vals)]
        # get nonzero vals because zeros have not had noise calculation done yet

        y, x = np.histogram(vals, bins=np.linspace(0, 20, 40))
        curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
        self.AmplitudeHistPlot.addItem(curve)

        self.SpikeRatePlot.setBackground('w')

        self.ElectrodeTraceZoomed
        self.ElectrodeTraceAll
        self.LabelElectrodeInfo

    def update(self):
        print("Update individual channels()")
        self.updateNoiseHistogram()

    def updateNoiseHistogram(self):
        vals = self.session_parent.LoadedData.array_stats['noise_std']
        vals = vals[np.nonzero(vals)]
        # get nonzero vals because zeros have not had noise calculation done yet

        y, x = np.histogram(vals, bins=np.linspace(0, 20, 40))
        curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
        self.AmplitudeHistPlot.addItem(curve)

    # TODO handle recursive loops
    def setElecNumber(self):
        input = self.InputElectrodeNumber.toPlainText()

        if input.isnumeric():
            if 0 <= int(input) < 1024 and int(input) != self.current_elec:
                self.current_elec = int(input)
                self.current_row, self.current_col = self.idx2map(self.current_elec)
                self.updateElectrodeInfo()
            else:
                pass
                self.InputElectrodeNumber.setText(str(self.current_elec))

        elif input == "":
            self.current_elec = 0
            self.current_col = 0
            self.current_row = 0
            self.InputElectrodeNumber.setText("0")
            self.updateElectrodeInfo()
        else:
            pass
            self.InputElectrodeNumber.setText(str(self.current_elec))

    def setElecRow(self):
        input = self.InputElectrodeRow.toPlainText()
        if input.isnumeric():
            if 0 <= int(input) < 32 and int(input) != self.current_row:
                self.current_row = int(input)
                self.current_elec = self.map2idx(self.current_row, self.current_col)
                self.updateElectrodeInfo()
            else:
                pass
                self.InputElectrodeRow.setText(str(self.current_row))
        elif input == "":
            self.current_row = 0
            self.InputElectrodeRow.setText("0")
            self.updateElectrodeInfo()
        else:
            pass
            self.InputElectrodeRow.setText(str(self.current_row))

    def setElecCol(self):
        input = self.InputElectrodeCol.toPlainText()
        if input.isnumeric():
            if 0 <= int(input) < 32 and int(input) != self.current_col:
                self.current_col = int(input)
                self.current_elec = self.map2idx(self.current_row, self.current_col)
                self.updateElectrodeInfo()
            else:
                pass
                self.InputElectrodeCol.setText(str(self.current_col))
        elif input == "":
            self.current_col = 0
            self.InputElectrodeCol.setText("0")
            self.updateElectrodeInfo()
        else:
            pass
            self.InputElectrodeCol.setText(str(self.current_col))

    def updateElectrodeInfo(self):
        self.LabelElectrodeInfo.setText(">>> ELEC #" + str(int(self.current_elec)) +
                                        " | R" + str(int(self.current_row)) +
                                        " C" + str(int(self.current_col)) + " <<<")

    def map2idx(self, ch_row: int, ch_col: int):
        """ Given a channel's row and col, return channel's index

        Args:
            ch_row: row index of channel in array (up to 32)
            ch_col: column index of channel in array (up to 32)

        Returns: numerical index of array
        """
        if ch_row > 31 or ch_row < 0:
            print('Row out of range')
        elif ch_col > 31 or ch_col < 0:
            print('Col out of range')
        else:
            ch_idx = int(ch_row * 32 + ch_col)
        return ch_idx

    def idx2map(self, ch_idx: int):
        """ Given a channel index, return the channel's row and col

        Args:
            ch_idx: single numerical index for array (up to 1024)

        Returns:
            channel row and channel index
        """
        if ch_idx > 1023 or ch_idx < 0:
            print('Chan num out of range')
        else:
            ch_row = int(ch_idx / 32)
            ch_col = int(ch_idx - ch_row * 32)
        return ch_row, ch_col




