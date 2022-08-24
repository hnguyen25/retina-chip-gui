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
from ..data.DC1DataContainer import *

# TODO:
#1. Fix hist

class IndividualChannelInformation(QWidget):

    session_parent = None
    current_elec = 0
    current_row = 0
    current_col = 0
    recordedTime = None
    has_data = None

    # List of dictionaries containing data packets with electrode info (data, times, spikes, etc)
    electrode_packets = []

    # Lists containing values stored in the associated key in electrode_packets dictionaries
    electrode_times = []
    electrode_data = []
    electrode_spikes = []
    electrode_spike_times = []

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
        self.SpikeRatePlot.setLabel('bottom','Time (ms)')


        self.ChannelTracePlot.setBackground('w')
        self.ChannelTracePlot.setLabel('bottom','Time (ms)')
        self.ChannelTracePlot.setLabel('left', 'Counts')
        self.ChannelTracePlot.enableAutoRange


# TODO: print profiling data?

    # Note: do NOT change name from "update"
    def update(self):
        start = time.time()
        print("Update individual channels: " + str(self.current_elec))
        self.updateElectrodeData()
        self.updateAmplitudeHist()
        self.updateSpikeRate()
        self.updateChannelTrace()
        self.totalSamples.setText("Total number of samples: " + str(len(self.electrode_data)))
        self.timeRecorded.setText("Total time recording electrode: "
                                  + str(self.recordedTime)
                                  + "ms")
        self.numSpikes.setText("Number of spikes: " + str(sum(self.electrode_spikes)))
        end = time.time()
        if self.session_parent.gui_state['is_mode_profiling']:
            print("Individual Channel update time: " + str(np.round(end-start,2)))
        #print(self.session_parent.LoadedData.)

    def updateElectrodeData(self, debug = False):
        self.electrode_packets.clear()
        self.electrode_spikes.clear()
        self.electrode_spike_times.clear()
        self.electrode_data.clear()
        self.electrode_times.clear()

        match = False
        len_filtered_data = len(self.session_parent.LoadedData.filtered_data)

        # Create a list of dictionaries of data packets for the selected electrode
        for i in range(len_filtered_data):
            if self.session_parent.LoadedData.filtered_data[i]['channel_idx'] == self.current_elec:
                self.electrode_packets.append(self.session_parent.LoadedData.filtered_data[i])
                match = True
        if debug:
            if not match:
                print("No data from this electrode yet")

        # Get lists of times and data from each packet for the selected electrode
        for i in range(len(self.electrode_packets)):
            self.session_parent.LoadedData.\
                calculate_realtime_spike_info_for_channel_in_buffer(self.electrode_packets[i], filtered=True)
            self.electrode_spikes.extend(self.electrode_packets[i]["spikeBins"])
            self.electrode_spike_times.extend(self.electrode_packets[i]["incom_spike_times"])
            self.electrode_times.extend(self.electrode_packets[i]['times'])
            self.electrode_data.extend(self.electrode_packets[i]['data'])

        self.recordedTime = round((len(self.electrode_data)) * 0.05, 2)
        
    def updateAmplitudeHist(self):
        vals = self.electrode_data
        std = np.std(vals)
        vals = abs(vals/std)
        self.AmplitudeHistPlot.clear()
        y, x = np.histogram(vals, bins=np.linspace(0, 20, 40))
        curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
        self.AmplitudeHistPlot.addItem(curve)

    def updateSpikeRate(self, movingAverage = True, windowSize = 5, numberOfUpdates = 10, debug=False):
        """
        movingAverage: If false, divide up the range into numberOfUpdates bins and average to find spike rate

        windowSize: Size of moving average window in milliseconds

        numberOfUpdates: How many times you want to update the spike rate if not doing moving average.
        Function divides the range of data into numberOfUpdates bins to time average spikes.

        debug: Print helpful data.
        """
        self.SpikeRatePlot.clear()
        spikeList = self.electrode_spikes
        indexes = np.linspace(0, len(spikeList), numberOfUpdates+1)
        indexes = [int(i) for i in indexes]
        t = []
        spike_rate = []

        # Only run if electrode has been recorded
        if self.recordedTime != 0:
            # Perform moving average on spike list
            if movingAverage:
                moving_averages = []
                i = 0
                while i < len(spikeList) - windowSize + 1:
                    window_average = round(np.sum(spikeList[i:i+windowSize]) / windowSize, 2)
                    moving_averages.append(1000*window_average) # multiply by 1000 to go to spikes/sec
                    i += 1
                t = np.linspace(self.electrode_times[0],self.electrode_times[-1],len(spikeList)-windowSize+1)
                spike_rate = moving_averages

            # Window mode
            else:
                num_spikes = []
                for i in range(numberOfUpdates):
                    window = spikeList[indexes[i]:indexes[i+1]]
                    num_spikes.append(sum(window))
                    spike_rate = [1000*num_spike/(self.recordedTime/numberOfUpdates) for num_spike in num_spikes]
                t = np.linspace(self.electrode_times[0], self.electrode_times[-1], numberOfUpdates)
                t = [int(i) for i in t]
        else:
            spike_rate = [0 for i in range(numberOfUpdates)]
            t = [0 for i in range(numberOfUpdates)]

        self.SpikeRatePlot.plot(t, spike_rate, pen=pg.mkPen(themes[CURRENT_THEME]['blue1'], width=5))

        if debug:
            print("length of recording: " + str(len(self.electrode_times)) + " data points")
            print("electrode times: " + str(self.electrode_times[0]) + "-" + str(self.electrode_times[-1]))
            print("spikes: " + str(self.electrode_spikes))
            #print("double binned spikes: " + str(num_spikes))
            print("number of spike bins: " + str(len(self.electrode_spikes)))
            print("incoming spike times: " + str(self.electrode_spike_times))
            print("noise mean: " + str(self.session_parent.LoadedData.array_stats['noise_mean'][self.current_row, self.current_col]))
            print("noise std: " + str(self.session_parent.LoadedData.array_stats['noise_std'][self.current_row, self.current_col]))

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