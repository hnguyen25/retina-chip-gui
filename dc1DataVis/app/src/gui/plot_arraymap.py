import numpy as np
import pyqtgraph as pg
import math

from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from dc1DataVis.app.src.gui.per_electrode_gui_rendering import *

def setupArrayMap(app, plot_widget, CURRENT_THEME, themes):
    plot_widget.showGrid(x=False, y=False, alpha=0)
    plot_widget.setAspectLocked()

    plot_widget.setLimits(xMin=-7, xMax=39,
                          yMin=-7, yMax=39,
                          minXRange=5, maxXRange=100,
                          minYRange=5, maxYRange=100)

    plot_widget.getPlotItem().hideAxis('top')
    plot_widget.getPlotItem().hideAxis('bottom')
    plot_widget.getPlotItem().hideAxis('left')
    plot_widget.getPlotItem().hideAxis('right')

    cm = pg.colormap.get('plasma', source='matplotlib')

    colors = np.array(app.data.df["spikes_avg_amp"]).reshape((32, 32))

    # the pyqtgraph color bar REQUIRES it to be set to an image
    # however, we don't want to use an image, we want it to be linked with our scatter plot
    # so we make it, and set it off the screen
    tr = QtGui.QTransform()  # prepare ImageItem transformation:
    tr.translate(200, 200)  # scoot image out of view
    image = pg.ImageItem(colors.T)  # for old pixel-based data
    image.setTransform(tr)

    # bound the LinearRegionItem to the plotted data
    app.charts["arrayMap"].addItem(image)
    app.array_map_color_bar = app.charts["arrayMap"].addColorBar(image, colorMap=cm, label="Spike Amplitude",
                                                                 values=(0, 150))  # values=(0, np.max(data)))
    app.array_map_color_bar.sigLevelsChanged.connect(lambda: on_color_bar_levels_changed(app))
    #app.charts["arrayMapHover"].region.setClipItem(image)

    update_minimap_indicator(app, CURRENT_THEME, themes)

    elecs_points = []
    for row in range(NUM_TOTAL_ROWS):
        for col in range(NUM_TOTAL_COLS):
            default_elec_dict = {'pos': (row, col), 'size': 0.1,
                         'pen': {'color': 'w'},
                         'brush': QColor(0, 0, 0, 0),
                         'symbol': 'o'}
            elecs_points.append(default_elec_dict)

    elecs_plot = pg.ScatterPlotItem(pxMode=False)
    elecs_plot.addPoints(elecs_points)
    app.update_subplot_element("arrayMap", 'default_elecs_plot', elecs_plot)

def update_array_map_plot(app, next_packet, CURRENT_THEME, themes, extra_params):
    # CURRENT ELECTRODE BOX INDICATOR
    curr_rec_elecs_box = []
    dot_scaling_changed = False

    for i in range(len(next_packet['packet_data'])):
        # get packet info
        chan_idx = next_packet['packet_data'][i]['channel_idx']
        from ..data.data_loading import idx2map
        row, col = idx2map(chan_idx)

        # add squares around electrodes currently being recorded from + visualized in spike trace
        spot_dict = {'pos': (col, row), 'size': 1,
                     'pen': {'color': pg.mkColor(themes[CURRENT_THEME]['light1']), 'width': 2},
                     'brush': QColor(255, 0, 255, 0),
                     'symbol': 's'}
        curr_rec_elecs_box.append(spot_dict)

        # check if scaling needs to be changed
        if app.data.stats['largest_spike_cnt'] < app.settings['spike_cnt_for_dot_size_saturation']:
            if app.data.df.at[chan_idx, "spikes_cnt"] > app.data.stats["largest_spike_cnt"]:
                if app.data.df.at[chan_idx, "spikes_cnt"] > app.settings['spike_cnt_for_dot_size_saturation']:
                    app.data.stats['largest_spikes_cnt'] = app.settings['spike_cnt_for_dot_size_saturation']
                else:
                    app.data.stats["largest_spike_cnt"] = app.data.df.at[chan_idx, "spikes_cnt"]
                dot_scaling_changed = True

    current_recording_elecs_indicator = pg.ScatterPlotItem(pxMode=False)
    current_recording_elecs_indicator.addPoints(curr_rec_elecs_box)
    app.update_subplot_element("arrayMap", "current_recording_elecs_indicator", current_recording_elecs_indicator)

    # update the dot information (color and size)
    idxs_to_change = []
    if dot_scaling_changed:  # all recalculate colors and sizes
        recalculate_all_colors(app)
        recalculate_all_sizes(app)
    else:  # calculate only for specific elecs in current buffer
        for i in range(len(next_packet['packet_data'])):
            chan_idx = next_packet['packet_data'][i]['channel_idx']
            idxs_to_change.append(chan_idx)
            calculate_one_elec_color_and_size(app, chan_idx)

    # render all the points
    elecs_points = []
    color_map = app.array_map_color_bar.colorMap()
    for row in range(NUM_TOTAL_ROWS):
        for col in range(NUM_TOTAL_COLS):
            from ..data.data_loading import map2idx
            idx = map2idx(row, col)
            color = color_map.map(app.data.df.at[idx, "array_dot_color"])

            default_elec_dict = {'pos': (col, row), 'size': app.data.df.at[idx, "array_dot_size"],
                                 'pen': color,
                                 'brush': color,
                                 'symbol': 'o'}
            elecs_points.append(default_elec_dict)
    elecs_plot = pg.ScatterPlotItem(pxMode=False)
    elecs_plot.addPoints(elecs_points)
    app.update_subplot_element("arrayMap", 'default_elecs_plot', elecs_plot)


def calculate_one_elec_color_and_size(app, idx):
    # calculate the dot color from electrode's average spike amplitude
    spike_avg_amp = app.data.df.at[idx, "spikes_avg_amp"]

    levels = app.array_map_color_bar.levels()
    spike_avg_amp = np.clip(spike_avg_amp, levels[0], levels[1])
    spike_avg_amp = (spike_avg_amp - levels[0]) / (levels[1] - levels[0])
    color = spike_avg_amp
    app.data.df.at[idx, "array_dot_color"] = color

    # calculate the dot size from electrode's average spike cou t
    spikes_cnt = app.data.df.at[idx, "spikes_cnt"]
    size = (spikes_cnt / app.data.stats["largest_spike_cnt"]) * app.settings["max_dot_size"]
    size = np.clip(size, app.settings["min_dot_size"], app.settings["max_dot_size"])
    app.data.df.at[idx, "array_dot_size"] = size
    return color, size

def recalculate_all_colors(app):
    spikes_avg_amp = np.array(app.data.df["spikes_avg_amp"])
    levels = app.array_map_color_bar.levels()

    spikes_avg_amp = np.clip(spikes_avg_amp, levels[0], levels[1])
    spikes_avg_amp = (spikes_avg_amp - levels[0]) / (levels[1] - levels[0])
    app.data.df["array_dot_color"] = spikes_avg_amp


def recalculate_all_sizes(app):
    spikes_cnt = np.array(app.data.df["spikes_cnt"])
    sizes = (spikes_cnt / app.data.stats["largest_spike_cnt"]) * app.settings["max_dot_size"]
    sizes = np.clip(sizes, app.settings["min_dot_size"], app.settings["max_dot_size"])
    app.data.df["array_dot_size"] = sizes



    if app.arrayMapHoverCoords is not None:
        x, y = app.arrayMapHoverCoords
        if 0 <= x <= 31 and 0 <= y <= 31:
            from dc1DataVis.app.src.data.DC1DataContainer import map2idx
            idx = map2idx(x, y)
            spike_cnt = app.data.df.at[idx, "spikes_cnt"]
            spike_amp = app.data.df.at[idx, "spikes_avg_amp"]
            # spike_cnt = app.data.array_indexed['stats_spikes+cnt'][y][x + 1]
            # spike_amp = app.data.array_indexed['stats_spikes+avg+amp'][y][x + 1]
            from ..data.data_loading import map2idx
            channel_idx = map2idx(y, x)
            tooltip_text = "<html>" + "Electrode Channel #" + str(channel_idx) + "<br>" + \
                           "Row " + str(y) + ", Column " + str(x) + "<br>" + \
                           "Spike Count: " + str(round(spike_cnt)) + "<br>" + \
                           "Spike Amplitude: " + str(round(spike_amp, 3)) + "<\html>"
            app.charts["arrayMap"].setToolTip(str(tooltip_text))


def on_color_bar_levels_changed(app):
    recalculate_all_colors(app)
    elecs_points = []
    color_map = app.array_map_color_bar.colorMap()
    for row in range(NUM_TOTAL_ROWS):
        for col in range(NUM_TOTAL_COLS):
            from ..data.data_loading import map2idx
            idx = map2idx(row, col)
            color = color_map.map(app.data.df.at[idx, "array_dot_color"])


            default_elec_dict = {'pos': (col, row), 'size': app.data.df.at[idx, "array_dot_size"],
                                 'pen': color,
                                 'brush': color,
                                 'symbol': 'o'}
            elecs_points.append(default_elec_dict)
    elecs_plot = pg.ScatterPlotItem(pxMode=False)
    elecs_plot.addPoints(elecs_points)
    app.update_subplot_element("arrayMap", 'default_elecs_plot', elecs_plot)


class HoverRegion():
    window = None
    region = None
    vLine, hLine = None, None
    vb = None
    proxy = None
    proxy2 = None
    HoverFunc, ClickFunc = None, None
    last_mouse_x, last_mouse_y = None, None

    def __init__(self, window_ref, HoverFunc, ClickFunc):
        self.window = window_ref
        #self.region = pg.LinearRegionItem()
        self.HoverFunc = HoverFunc
        self.ClickFunc = ClickFunc

        #self.window.addItem(self.region, ignoreBounds=True)
        #self.window.sigRangeChanged.connect(self.updateRegion)

        #self.region.setZValue(10)
        #self.region.setRegion([-10, 50])
        #self.region.sigRegionChanged.connect(self.update)

        self.vb = self.window.plotItem.vb
        self.proxy = pg.SignalProxy(self.window.scene().sigMouseMoved,
                                    rateLimit=10,
                                    slot=self.mouseMoved)
        #self.proxy2 = pg.SignalProxy(self.window.scene().sigMouseClicked,
        #                             rateLimit=60,
        #                             slot=self.mouseClicked)
        self.window.scene().sigMouseClicked.connect(self.mouseClicked)
    #def update(self):
    #    self.region.setZValue(10)
    #   self.window.setXRange(-10, 40, padding=0)

    #def updateRegion(self, window, viewRange):
    #    rgn = viewRange[0]
    #    self.region.setRegion(rgn)

    def mouseMoved(self, evt):
        pos = evt[0]  # using signal proxy turns original arguments into a tuple
        if self.window.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            self.last_mouse_x = mousePoint.x()
            self.last_mouse_y = mousePoint.y()
            self.HoverFunc(mousePoint.x(), mousePoint.y())

    def mouseClicked(self, evt):
        pos = (self.last_mouse_x, self.last_mouse_y)
        #if self.window.sceneBoundingRect().contains(pos):
            # mousePoint = self.vb.mapSceneToView(pos)
        # print('entering click func')
        self.ClickFunc(self.last_mouse_x, self.last_mouse_y)


def update_minimap_indicator(app, CURRENT_THEME, themes): # this is called on cursor click + on setup
    # add a square around electrodes displayed in the minimap

    minimap_square_indicator = pg.QtGui.QGraphicsRectItem(app.settings['cursor_row'] - 4.5,
                                                          app.settings['cursor_col'] - 2.5, 8, 4)
    minimap_square_indicator.setPen(pg.mkPen(themes[CURRENT_THEME]['blue3']))
    minimap_square_indicator.setBrush(QColor(255, 0, 255, 0))
    app.update_subplot_element("arrayMap", 'minimap_square_indicator', minimap_square_indicator)