from PyQt5.QtGui import QColor

from dc1DataVis.app.src.gui.setup_charts import *
from dc1DataVis.app.src.gui.array_map import *

import numpy as np
import math
from dc1DataVis.app.src.gui.gui_individualchannel import IndividualChannelInformation
from dc1DataVis.app.src.data.data_loading import *
import pyqtgraph as pg

def update_noise_heat_map(app, next_packet, CURRENT_THEME, themes, extra_params, debug=False):
    plot = app.charts["noiseHeatMap"]
    plot.clear()

    font = pg.QtGui.QFont()
    font.setPixelSize(20)

    plot.getAxis("bottom").tickFont = font
    plot.getAxis("bottom").setStyle(tickTextOffset=1)

    if app.first_time_plotting is False:
        data = app.data.array_indexed["stats_noise+std"]
        data = data.T
    else:
        data = None

    img = pg.ImageItem(data)
    cm = pg.colormap.get('plasma', source='matplotlib')
    plot.addItem(img)

    if app.noise_heat_map_color_bar is None:
        app.noise_heat_map_color_bar = app.charts["noiseHeatMap"].addColorBar(img, colorMap=cm, label="Noise SD",
                                                                                values=(0, 10))
    else:
        app.noise_heat_map_color_bar.setImageItem(img)

    app.first_time_plotting = False

    if debug:
        print("Data" + str(data))

def update_channel_trace_plot(app, next_packet, CURRENT_THEME, themes, extra_params):
    """
    This function updates the data for the trace plots when a new packet arrives. The plots are updated even faster
    through 'continuouslyUpdateTracePlotData()', which scans through the packet slowly to visualize data as realtime.
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

        from ..data.data_loading import idx2map
        row, col = idx2map(chan_idx)

        # crop to area where data != 0
        nonzero_data = np.where(data != 0.)[0]
        first_nonzero_index = nonzero_data[0]
        last_nonzero_index = nonzero_data[-1]

        # TODO [later] check why the dims of times and data don't match
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

        channel_noise_mean = app.data.array_indexed["stats_noise+mean"][row][col]
        channel_noise_std = app.data.array_indexed["stats_noise+std"][row][col]
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

def update_noise_histogram_plot(app, next_packet, CURRENT_THEME, themes, debug=False, colored=True):
    """
    @param debug: if true, prints helpful information
    @param colored: if true, plots normal range of histogram and colors according to bin. false plots single
    color with larger range, used primarily for debugging array_indexed
    @return:
    """

    app.charts["noiseHistogram"].clear()

    vals = app.data.array_indexed['stats_noise+std'].copy()
    vals = vals[np.nonzero(vals)]

    cm = pg.colormap.get('plasma', source='matplotlib')

    if debug:
        print("updating noise histogram plot")
        print("vals: " + str(vals))

    if colored:
        y, x = np.histogram(vals, bins=np.linspace(0, 20, 50))

        colors = cm.getColors()

        scale = (int(len(colors) / 10))

        for i in range(len(x) - 1):
            bins = [x[i], x[i + 1]]
            values = [y[i]]

            color = int(scale * x[i])

            if color > 255:
                color = 255

            curve = pg.PlotCurveItem(bins, values, stepMode=True, fillLevel=0,
                                     brush=colors[color])

            app.charts["noiseHistogram"].addItem(curve)


    else:
        y, x = np.histogram(vals, bins=np.linspace(0, 50, 100))
        curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
        app.charts["noiseHistogram"].addItem(curve)

def update_mini_map_plot(app, next_packet, CURRENT_THEME, themes, extra_params):
    print('update mini map plot')
    app.charts["miniMap"].clear()
    BAR_LENGTH = 4
    MAX_SPIKES = 16  # can't draw every spike or gui will crash -> group spikes together

    for row in range(app.settings['cursor_row'] - 4, app.settings['cursor_row'] + 4):
        for col in range(app.settings['cursor_col'] - 2, app.settings['cursor_col'] + 2):
            if (row > -2) and (col > -2):
                spike_indicator_base = pg.QtGui.QGraphicsRectItem(row * 5, col * 5, BAR_LENGTH, 0.2)
                spike_indicator_base.setPen(pg.mkPen(themes[CURRENT_THEME]['blue1']))
                spike_indicator_base.setBrush(pg.mkBrush(themes[CURRENT_THEME]['blue1']))

                from ..data.data_loading import map2idx
                elec_idx = str(map2idx(col, row))
                spike_indicator_text = pg.TextItem(elec_idx,
                                                   themes[CURRENT_THEME]['font_color'],
                                                   anchor=(0, 0))
                spike_indicator_text.setPos(row * 5, col * 5)
                spike_indicator_text.setParentItem(spike_indicator_base)

                app.charts["miniMap"].addItem(spike_indicator_base)
                app.charts["miniMap"].addItem(spike_indicator_text)
                '''
                #times = [0, 1, 3, 5, 10, 11, 14]
                if np.random.random() > 0.5:
                    times = np.random.randint(0, 20, (3,), dtype='int64')
                    for i in times:
                        spike_indicator = pg.QtGui.QGraphicsRectItem(row*5 + i/5, col*5, 0.1, 1.5)
                        spike_indicator.setPen(pg.mkPen((0, 0, 0, 100)))
                        spike_indicator.setBrush(pg.mkBrush((50, 50, 200)))
                        spike_indicator.setParentItem(spike_indicator_base)
                        app.charts["miniMap"].addItem(spike_indicator)

                app.charts["miniMap"].addItem(spike_indicator_base)
                app.charts["miniMap"].addItem(spike_indicator_text)
                '''

    LAST_N_BUFFER_DATA = 100

    # TODO add spike locs for minimap
    """
    to_search = app.data.preprocessed_data[-LAST_N_BUFFER_DATA:]
    spikes_within_view = []
    for data_packet in to_search:
        chan_idx = data_packet['channel_idx']

        from ..data.data_loading import idx2map
        c, r = idx2map(chan_idx)
        if (app.settings['cursor_row'] - 4 <= r) & (r < app.settings['cursor_row'] + 4) & \
                (app.settings['cursor_col'] - 2 <= c) & (c < app.settings['cursor_col'] + 2):
            spikes_within_view.append(data_packet)

    for data_packet in spikes_within_view:
        chan_idx = data_packet['channel_idx']
        from ..data.data_loading import idx2map
        row, col = idx2map(chan_idx)
        spikeBins = data_packet['spikeBins']
        spikeBinsMaxAmp = data_packet['spikeBinsMaxAmp']
        spikeLocs = np.argwhere(spikeBins == True)

        num_bins = data_packet['num_bins_in_buffer']
        for i in spikeLocs:
            spike_loc_on_vis_bar = (i / num_bins) * BAR_LENGTH
            spike_height_on_vis_bar = spikeBinsMaxAmp[i] / 50
            spike_indicator = pg.QtGui.QGraphicsRectItem(col * 5 + spike_loc_on_vis_bar, row * 5, 0.1,
                                                         spike_height_on_vis_bar)
            spike_indicator.setPen(pg.mkPen(themes[CURRENT_THEME]['blue1']))
            spike_indicator.setBrush(pg.mkBrush(themes[CURRENT_THEME]['blue1']))
            spike_indicator.setParentItem(spike_indicator_base)
            app.charts["miniMap"].addItem(spike_indicator)
    """