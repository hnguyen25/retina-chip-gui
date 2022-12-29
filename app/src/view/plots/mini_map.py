import numpy as np
import pyqtgraph as pg
import math
from PyQt5.QtGui import QColor

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

def update_mini_map_plot(app, next_packet, CURRENT_THEME, themes, extra_params):
    app.charts["miniMap"].clear()

    BAR_LENGTH = 4

    # same as self.settings['binSize'] but for the minimap.
    # so that the view doesn't freeze
    # TODO
    MIN_BIN_LENGTH = 4
    MAX_SPIKES = 16  # can't draw every spike or view will crash -> group spikes together

    curr_idxs = []
    for packet in next_packet['packet_data']:
        curr_idxs.append(packet['channel_idx'])

    # make a legend
    legend_loc_x = app.settings['cursor_row'] - 4 - 1.5
    legend_loc_y = app.settings['cursor_col'] - 2

    spike_indicator_base = pg.QtGui.QGraphicsRectItem(legend_loc_x * 5, legend_loc_y * 5, BAR_LENGTH, 0.2)
    spike_indicator_base.setPen(pg.mkPen(themes[CURRENT_THEME]['blue1']))
    spike_indicator_base.setBrush(pg.mkBrush(themes[CURRENT_THEME]['blue1']))

    legend_text = str(round(app.data.buffer_indexed[0]["time_elapsed"], 0)) + " ms"
    spike_indicator_text = pg.TextItem(legend_text,
                                       themes[CURRENT_THEME]['font_color'],
                                       anchor=(0, 0))
    spike_indicator_text.setPos(legend_loc_x * 5, legend_loc_y * 5)
    spike_indicator_text.setParentItem(spike_indicator_base)
    app.charts["miniMap"].addItem(spike_indicator_base)
    app.charts["miniMap"].addItem(spike_indicator_text)

    # now visualize the selected electrodes in the window of the minimap
    for row in range(app.settings['cursor_row'] - 4, app.settings['cursor_row'] + 4):
        for col in range(app.settings['cursor_col'] - 2, app.settings['cursor_col'] + 2):
            if (row > -2) and (col > -2):
                from app.src.model.data_loading import map2idx
                elec_idx = str(map2idx(col, row))
                spike_indicator_base = pg.QtGui.QGraphicsRectItem(row * 5, col * 5, BAR_LENGTH, 0.2)

                if elec_idx not in curr_idxs:
                    spike_indicator_base.setPen(pg.mkPen(themes[CURRENT_THEME]['blue1']))
                    spike_indicator_base.setBrush(pg.mkBrush(themes[CURRENT_THEME]['blue1']))
                else:
                    spike_indicator_base.setPen(pg.mkPen(themes[CURRENT_THEME]['orange']))
                    spike_indicator_base.setBrush(pg.mkBrush(themes[CURRENT_THEME]['orange']))

                spike_indicator_text = pg.TextItem(elec_idx,
                                                   themes[CURRENT_THEME]['font_color'],
                                                   anchor=(0, 0))
                spike_indicator_text.setPos(row * 5, col * 5)
                spike_indicator_text.setParentItem(spike_indicator_base)

                app.charts["miniMap"].addItem(spike_indicator_base)
                app.charts["miniMap"].addItem(spike_indicator_text)

                spike_bins = app.data.array_spike_times["spike_bins"][int(elec_idx)]
                spike_bins_max_amps = app.data.array_spike_times["spike_bins_max_amps"][int(elec_idx)]

                spikeLocs = np.argwhere(spike_bins == True)
                num_bins = len(spike_bins)

                for i in spikeLocs:
                    spike_loc_on_vis_bar = (i / num_bins) * BAR_LENGTH
                    spike_height_on_vis_bar = np.abs(spike_bins_max_amps[i] / 20)
                    spike_indicator = pg.QtGui.QGraphicsRectItem(row * 5 + spike_loc_on_vis_bar, col * 5, 0.03,
                                                                 spike_height_on_vis_bar)
                    spike_indicator.setPen(pg.mkPen(themes[CURRENT_THEME]['blue1']))
                    spike_indicator.setBrush(pg.mkBrush(themes[CURRENT_THEME]['blue1']))
                    spike_indicator.setParentItem(spike_indicator_base)
                    app.charts["miniMap"].addItem(spike_indicator)

