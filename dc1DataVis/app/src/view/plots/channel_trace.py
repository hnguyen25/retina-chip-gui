import numpy as np
import pyqtgraph as pg
import math
from PyQt5.QtGui import QColor

def setupSpikeTrace(list_of_plots, CURRENT_THEME, themes):
    for plot in list_of_plots:
        plot.getAxis("left").setTextPen(themes[CURRENT_THEME]['font_color'])
        plot.getAxis("bottom").setTextPen(themes[CURRENT_THEME]['font_color'])
        plot.getAxis('top').setTextPen(themes[CURRENT_THEME]['font_color'])
        plot.setLabel('left', '# ???')
        plot.setLabel('bottom', 'Time (ms)')

def update_channel_trace_plot(app, next_packet, CURRENT_THEME, themes, extra_params):
    """
    This function updates the model for the trace plots when a new packet arrives. The plots are updated even faster
    through 'continuouslyUpdateTracePlotData()', which scans through the packet slowly to visualize model as realtime.
    Args:
        trace_plots:

    Returns:
    """
    trace_plots = extra_params

    # Generate subplots
    for m, plt in enumerate(trace_plots):
        plt.clear()

        times = next_packet["packet_data"][m]["times"]
        data = next_packet["packet_data"][m]["filtered_data"]

        chan_idx = next_packet["packet_data"][m]["channel_idx"]

        from dc1DataVis.app.src.model.data_loading import idx2map
        row, col = idx2map(chan_idx)

        # crop to area where model != 0
        nonzero_data = np.where(data != 0.)[0]
        first_nonzero_index = nonzero_data[0]
        last_nonzero_index = nonzero_data[-1]

        # TODO [later] check why the dims of times and model don't match
        # crop to range
        data = data[first_nonzero_index:last_nonzero_index]
        times = times[first_nonzero_index:last_nonzero_index]

        begin_time = times[0]
        end_time = times[-1]

        # TODO [later] more principled way of doing x and y range
        WIDTH_OF_TIME_TO_DISPLAY = 250
        center_time = (end_time - begin_time) / 2
        #plt.setXRange(begin_time + center_time - WIDTH_OF_TIME_TO_DISPLAY/2,
        #              begin_time + center_time + WIDTH_OF_TIME_TO_DISPLAY/2,
        #              padding=0)


        channel_noise_mean = app.data.df.at[chan_idx, "noise_mean"]
        channel_noise_std = app.data.df.at[chan_idx, "noise_std"]
        # channel_noise_mean = app.model.array_indexed["stats_noise+mean"][row][col]
        # channel_noise_std = app.model.array_indexed["stats_noise+std"][row][col]
        plt.setYRange(channel_noise_mean - 10 * channel_noise_std,
                      channel_noise_mean + 10 * channel_noise_std,
                      padding=0)

        tooltip_text = '<html>Trace signal of electrode #' + str(chan_idx) + \
                       '<br>Row ' + str(row) + ', Column ' + str(col) + \
                       '<br>From time ' + str(round(begin_time, 2)) + 's to ' + str(round(end_time, 2)) + \
                       's after this recording started.' + \
                       '<\html>'

        plt.setToolTip(tooltip_text)

        # TODO add channel name as the background
        plt.getAxis("left").setTextPen(themes[CURRENT_THEME]['font_color'], size='20pt')
        plt.setLabel('left', 'Ch ' + str(next_packet['packet_data'][m]['channel_idx']))
        plt.plot(times, data)