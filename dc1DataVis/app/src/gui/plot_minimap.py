import numpy as np
import pyqtgraph as pg
import math
from PyQt5.QtGui import QColor
from dc1DataVis.app.src.gui.per_electrode_gui_rendering import *

bar_color = QColor(100, 0, 0, 100)
spike_color = QColor(0, 100, 0, 100)
def minimap_gui_update_fn(x, y, data):
    spike_times, spike_amps, elec_idx = data["spike_times_normed"], data["spike_amps_normed"], data["idx"]

    # draw a horizontal bar at the bottom with the index of the electrode
    bar_ref = pg.QtGui.QGraphicsRectItem(x, y,
                                         4, 0.5)  # width, height
    bar_ref.setPen(pg.mkPen(data["themes"][data["CURRENT_THEME"]]['bar_color']))
    bar_ref.setBrush(pg.mkPen(data["themes"][data["CURRENT_THEME"]]['bar_color']))

    # draw a number next to the bar
    elec_idx = data["idx"]
    bar_text_ref = pg.TextItem(elec_idx,
                                       data["themes"][data["CURRENT_THEME"]]['font_color'],
                                       anchor=(0, 0))
    bar_text_ref.setPos(x, y)
    bar_text_ref.setParentItem(bar_ref)

    # and then draw the spikes
    BAR_LENGTH = 2
    list_of_spike_refs = []
    for (spike_time, spike_amp) in zip(spike_times, spike_amps):
        spike_ref = pg.QtGui.QGraphicsRectItem(x + spike_time * BAR_LENGTH, y,
                                               0.5, spike_amp)
        spike_ref.setPen(pg.mkPen(spike_color))
        spike_ref.setBrush(pg.mkBrush(spike_color))
        list_of_spike_refs.append(spike_ref)

    shape_refs = {'bar': bar_ref, 'bar_text': bar_text_ref, 'spikes': list_of_spike_refs}
    return shape_refs

def setupMiniMapPlot(app, plot_widget, CURRENT_THEME, themes, center_row=16, center_col=16):
    plot_widget.showGrid(x=True, y=True, alpha=0)
    plot_widget.getPlotItem().hideAxis('bottom')
    plot_widget.getPlotItem().hideAxis('left')
    plot_widget.enableAutoRange(axis='x', enable=True)
    plot_widget.enableAutoRange(axis='y', enable=True)
    plot_widget.setAspectLocked()

    PGPlotPerElectrodeRendering(app, plot_widget, 8, 4,
                                ["spike_times", "spike_amps", "elec_idx"],
                                minimap_gui_update_fn)

def update_mini_map_plot(app, next_packet, CURRENT_THEME, themes, extra_params):

    # TODO update PGPlotPerElectrodeRendering

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