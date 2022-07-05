from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
import numpy as np
import pyqtgraph as pg
import time

# TODO:
# 1. Mirror input to one text entry to other two, make update method correct
# 2. Dataframe/computation plan for non-trace plots

class IndividualChannelInformation(QWidget):

    session_parent = None
    current_elec = 0
    current_row = 0
    current_col = 0
    chan_charts = {} # dictionary for all different individual channel charts
    chan_charts_update_mapping = {} # dictionary for mapping charts to their update functions

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./src/gui/IndividualChannelWindow.ui", self)

        self.updateElectrodeNum.clicked.connect(self.setElecNum)
        self.updateRC.clicked.connect(self.setRC)

        self.chan_charts = {'ChannelTracePlot': None , 'SpikeRateHistPlot': None,
                            'AmplitudeHistPlot': None, 'SpikeRatePlot': None}

        #self.chan_charts_update_mapping = {'ChannelTracePlot': self.updateChannelTrace(), 'SpikeRateHistPlot': self.updateSpikeRateHist(),
                                           #'AmplitudeHistPlotPlot': self.updateAmplitudeHist(), 'SpikeRatePlot': self.updateSpikeRate()}




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

        self.SpikeRateHistPlot.setBackground('w')

        self.ChannelTracePlot.setBackground('w')


        #self.ElectrodeTraceZoomed
        #self.ElectrodeTraceAll
        self.LabelElectrodeInfo

# TODO: print profiling data?

    # Note: do not change name from update
    def update(self):
        print("Update individual channels()")
        self.updateAmplitudeHist()
        self.updateSpikeRate()
        self.updateChannelTrace()
        self.updateSpikeRateHist()



    def updateAmplitudeHist(self):
        vals = self.session_parent.LoadedData.array_stats['noise_std']
        vals = vals[np.nonzero(vals)]
        # get nonzero vals because zeros have not had noise calculation done yet

        y, x = np.histogram(vals, bins=np.linspace(0, 20, 40))
        curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
        self.AmplitudeHistPlot.addItem(curve)


    def updateSpikeRateHist(self):
        self.SpikeRateHistPlot.clear()
        # vals = self.session_parent.LoadedData.array_stats['spike_std'][self.current_row][self.current_col]
        # vals = vals[np.nonzero(vals)]
        # # TODO: is this necessary ?
        #
        # y, x = np.histogram(vals, bins=np.linspace(0, 20, 40))
        # curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
        #
        # self.SpikeRateHistPlot.addItem(curve)

    def updateSpikeRate(self):
        pass

    def updateChannelTrace(self):

        x = self.session_parent.LoadedData.filtered_data[self.current_elec]['times']
        y = self.session_parent.LoadedData.filtered_data[self.current_elec]['data']

        self.ChannelTracePlot.clear()

        self.ChannelTracePlot.plot(x, y, pen='b')
        self.ChannelTracePlot.setLabel('left', '#' + str(self.session_parent.LoadedData.filtered_data[self.current_elec]['channel_idx']))
        self.ChannelTracePlot.enableAutoRange(axis='y')
        self.ChannelTracePlot.setAutoVisible(y=True)

    def setRC(self):
        """ Set the row and column entries and textboxes given an electrode number """
        input = self.InputElectrodeNumber.toPlainText()
        if input.isnumeric():
            if 0 <= int(input) < 1024 and int(input) != self.current_elec:
                self.current_elec = int(input)
                self.current_row, self.current_col = self.idx2map(self.current_elec)
                self.InputElectrodeRow.setText(str(self.current_row))
                self.InputElectrodeCol.setText(str(self.current_col))
                self.updateElectrodeInfo()
            else:
                pass
                self.InputElectrodeNumber.setText(str(self.current_elec))
        else:
            pass
            self.InputElectrodeNumber.setText(str(self.current_elec))

    def setElecNum(self):
        """ Given a row and column value, set the electrode number textbox and display plots"""

        row = self.InputElectrodeRow.toPlainText()
        col = self.InputElectrodeCol.toPlainText()
        if row == "":
            self.current_row = 0
            self.InputElectrodeRow.setText("0")
        if col == "":
            self.current_col = 0
            self.InputElectrodeCol.setText("0")
        if row.isnumeric() and col.isnumeric():
            row = int(row)
            col = int(col)

            if 0 <= row < 32 and row != self.current_row:
                self.current_row = row

            if 0 <= col < 32 and col != self.current_col:
                self.current_col = col
            self.current_elec = self.map2idx(self.current_row, self.current_col)
            self.updateElectrodeInfo()
        self.InputElectrodeNumber.setText(str(self.current_elec))

    def updateElectrodeInfo(self):
        self.LabelElectrodeInfo.setText(">>> ELEC #" + str(int(self.current_elec)) +
                                        " | R" + str(int(self.current_row)) +
                                        " C" + str(int(self.current_col)) + " <<<")
        self.update()

    def map2idx(self, ch_row: int, ch_col: int) -> object:
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