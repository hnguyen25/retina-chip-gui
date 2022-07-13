from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtWidgets import *
from PyQt5 import uic
import os
import numpy as np
import pyqtgraph as pg
import time
from ..data.spikeDetection import *

# TODO:
# 1. Spikes and spike rate

class IndividualChannelInformation(QWidget):

    session_parent = None
    current_elec = 0
    current_row = 0
    current_col = 0
    has_data = None
    electrode_times = []
    electrode_data = []

    electrode_packets = []


    chan_charts = {} # dictionary for all different individual channel charts
    chan_charts_update_mapping = {} # dictionary for mapping charts to their update functions

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./src/gui/IndividualChannelWindow.ui", self)

        self.updateElectrodeNum.clicked.connect(self.setElecNum)
        self.updateRC.clicked.connect(self.setRC)

        self.chan_charts = {'ChannelTracePlot': None,
                            'AmplitudeHistPlot': None,
                            'SpikeRatePlot': None}

    def setSessionParent(self, session_parent):
        self.session_parent = session_parent
        self.setupCharts()

    def setupCharts(self):
        self.AmplitudeHistPlot.setBackground('w')
        self.AmplitudeHistPlot.setLabel('left', 'Number of data points')
        self.AmplitudeHistPlot.setLabel('bottom', 'Standard Deviations')

        self.SpikeRatePlot.setBackground('w')
        self.SpikeRatePlot.setLabel('left', 'Spikes per second')


        self.ChannelTracePlot.setBackground('w')
        self.ChannelTracePlot.setLabel('bottom','Time (sec)')
        self.ChannelTracePlot.setLabel('left', 'Counts')
        self.ChannelTracePlot.enableAutoRange


# TODO: print profiling data?

    # Note: do not change name from update
    def update(self):
        print("Update individual channels()")
        self.updateElectrodeData()
        self.updateAmplitudeHist()
        self.updateSpikeRate()
        self.updateChannelTrace()
        self.totalSamples.setText("Total number of samples: " + str(len(self.electrode_data)))
        self.timeRecorded.setText("Total time recording electrode: "
                                  + str(round((len(self.electrode_data)) * 0.05,2))
                                  + "ms")
        #print(str(self.session_parent.LoadedData.array_stats["spike_cnt"][self.current_row][self.current_col]))

    def updateElectrodeData(self):
        match = False
        len_filtered_data = len(self.session_parent.LoadedData.filtered_data)

        self.electrode_packets.clear()
        self.electrode_data.clear()
        self.electrode_times.clear()

        # Create a list of dictionaries of data packets for the selected electrode
        for i in range(len_filtered_data):
            if self.session_parent.LoadedData.filtered_data[i]['channel_idx'] == self.current_elec:
                self.electrode_packets.append(self.session_parent.LoadedData.filtered_data[i])
                match = True
        if not match:
            print("No data from this electrode yet")

        # Get lists of times and data from each packet for the selected electrode
        for i in range(len(self.electrode_packets)):
            self.electrode_times.extend(self.electrode_packets[i]['times'])
            self.electrode_data.extend(self.electrode_packets[i]['data'])

# TODO
    def updateAmplitudeHist(self):
        vals = self.electrode_data
        std = np.std(vals)
        vals = abs(vals/std)
        #vals = vals[np.nonzero(vals)]
        # get nonzero vals because zeros have not had noise calculation done yet
        self.AmplitudeHistPlot.clear()
        y, x = np.histogram(vals, bins=np.linspace(0, 20, 40))
        curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
        self.AmplitudeHistPlot.addItem(curve)

    def updateSpikeRate(self):
        self.SpikeRatePlot.clear()
        recordedTime = len(self.electrode_data)*0.05
        if self.electrode_data:
            findSpikesGMM(self.electrode_data,self.current_elec, debug = False)

        # x = self.electrode_times
        # y = self.session_parent.LoadedData.array_stats["spike_cnt"][self.current_row][self.current_col]/recordedTime
        # print("x len: " + str(len(x)))
        # print("y len: " + str(len(y)))
        # line_plot = self.SpikeRatePlot.plot(x,y,pen='b', symbol='o', symbolPen='b',
        #                      symbolBrush=0.2)

    def updateChannelTrace(self):
        self.ChannelTracePlot.clear()
        self.ChannelTracePlot.plot(self.electrode_times, self.electrode_data, pen='b')
        self.ChannelTracePlot.enableAutoRange(axis='y')
        self.ChannelTracePlot.setAutoVisible(y=True)
        self.ChannelTracePlot.setLabel('top', '#' + str(self.current_elec))

    def setRC(self):
        """ Set the row and column entries and textboxes given an electrode number.

        Connected to "Update Row and Column" button

         """
        input = self.InputElectrodeNumber.toPlainText()
        if input.isnumeric():
            if 0 <= int(input) < 1024 and int(input) != self.current_elec:
                self.current_elec = int(input)
                self.current_row, self.current_col = self.idx2map(self.current_elec)
                self.InputElectrodeRow.setText(str(self.current_row))
                self.InputElectrodeCol.setText(str(self.current_col))
                self.update()
            else:
                pass
                self.InputElectrodeNumber.setText(str(self.current_elec))
        else:
            pass
            self.InputElectrodeNumber.setText(str(self.current_elec))

    def setElecNum(self):
        """ Given a row and column value, set the electrode number textbox and display plots

        Connected to the
        """

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
            else:
                pass
                self.InputElectrodeRow.setText(str(self.current_row))

            if 0 <= col < 32 and col != self.current_col:
                self.current_col = col
            else:
                pass
                self.InputElectrodeCol.setText(str(self.current_col))

            self.current_elec = self.map2idx(self.current_row, self.current_col)
            self.update()
        self.InputElectrodeNumber.setText(str(self.current_elec))

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