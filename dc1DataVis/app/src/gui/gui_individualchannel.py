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

        self.UpdateInput.clicked.connect(self.setElecNumber)
        #self.InputElectrodeNumber.textChanged.connect(self.setElecNumber)
        self.InputElectrodeRow.textChanged.connect(self.setElecRow)
        self.InputElectrodeCol.textChanged.connect(self.setElecCol)

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
        # for chart in self.chan_charts.keys():
        #     chart_type = type(self.chan_charts[chart])
        #     if str(chart_type) == "<class 'pyqtgraph.widgets.PlotWidget.PlotWidget'>": # TODO: make sure this works
        #         start = time.time()
        #         self.chan_charts_update_mapping[chart]()
        #         end = time.time()

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


# TODO handle recursive loops

    def setElecNumber(self):
        input = self.InputElectrodeNumber.toPlainText()
        print(input) # debugging

        if input.isnumeric():
            if 0 <= int(input) < 1024 and int(input) != self.current_elec:
                self.current_elec = int(input)
                self.current_row, self.current_col = self.idx2map(self.current_elec)
                self.updateElectrodeInfo()
            else:
                pass
                self.InputElectrodeNumber.setText(str(self.current_elec))

        elif input == "":
            print("elif triggered") # debugging
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
        self.update()

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