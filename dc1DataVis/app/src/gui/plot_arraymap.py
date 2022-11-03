import numpy as np
import pyqtgraph as pg
import math
from PyQt5.QtGui import QColor
from dc1DataVis.app.src.gui.per_electrode_gui_rendering import *

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
        self.region = pg.LinearRegionItem()
        self.HoverFunc = HoverFunc
        self.ClickFunc = ClickFunc

        self.window.addItem(self.region, ignoreBounds=True)
        self.window.sigRangeChanged.connect(self.updateRegion)

        self.region.setZValue(10)
        self.region.setRegion([-10, 50])
        self.region.sigRegionChanged.connect(self.update)

        self.vb = self.window.plotItem.vb
        self.proxy = pg.SignalProxy(self.window.scene().sigMouseMoved,
                                    rateLimit=10,
                                    slot=self.mouseMoved)
        #self.proxy2 = pg.SignalProxy(self.window.scene().sigMouseClicked,
        #                             rateLimit=60,
        #                             slot=self.mouseClicked)
        self.window.scene().sigMouseClicked.connect(self.mouseClicked)

    def update(self):
        self.region.setZValue(10)
        self.window.setXRange(-10, 40, padding=0)

    def updateRegion(self, window, viewRange):
        rgn = viewRange[0]
        self.region.setRegion(rgn)

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

def get_array_map_data(app):
    app.charts["arrayMap"].clear()
    colors = app.data.array_indexed['stats_spikes+avg+amp']
    max_dot = 50

    # AX1) Size by Number of Samples
    spike_cnt = app.data.array_indexed['stats_spikes+cnt']
    scaling_den = np.max(spike_cnt) - np.min(spike_cnt[spike_cnt != 0])
    if scaling_den == 0:
        scale1 = 1
    else:
        scale1 = (max_dot - 15) / (np.max(spike_cnt) - np.min(spike_cnt[spike_cnt != 0]))
    b_add = max_dot - (np.max(spike_cnt) * scale1)
    sizes = np.round(spike_cnt * scale1 + b_add)
    sizes[sizes < 15] = 10  # TODO fix saturation point
    return colors, sizes

def array_gui_update_fn(x, y, data):
    size, color = data["size"], data["color"]

    # draw a circle with a certain size and color
    circle_ref = pg.QtGui.QGraphicsEllipseItem(x, y, size, size)  # x, y, width, height
    circle_ref.setPen(pg.mkPen(color))
    circle_ref.setBrush(pg.mkBrush(color))
    return {'circle_ref': circle_ref}

def setupArrayMap(app, plot_widget, CURRENT_THEME, themes):
    plot_widget.showGrid(x=False, y=False, alpha=0)
    plot_widget.setAspectLocked()

    plot_widget.setLimits(xMin=-5, xMax=37,
                          yMin=-2, yMax=33,
                          minXRange=5, maxXRange=55,
                          minYRange=5, maxYRange=42)

    plot_widget.getPlotItem().hideAxis('top')
    plot_widget.getPlotItem().hideAxis('bottom')
    plot_widget.getPlotItem().hideAxis('left')
    plot_widget.getPlotItem().hideAxis('right')

    cm = pg.colormap.get('plasma', source='matplotlib')
    colors, sizes = get_array_map_data(app)

    # bound the LinearRegionItem to the plotted data
    image = pg.ImageItem(colors.T)  # for old pixel-based data
    app.charts["arrayMap"].addItem(image)
    app.array_map_color_bar = app.charts["arrayMap"].addColorBar(image, colorMap=cm, label="Spike Amplitude",
                                                                 values=(0, 150))  # values=(0, np.max(data)))
    app.array_map_color_bar.sigLevelsChanged.connect(on_color_bar_levels_changed)
    app.charts["arrayMapHover"].region.setClipItem(image)

    PGPlotPerElectrodeRendering(app, plot_widget, 32, 32,
                                ["colors", "sizes"],
                                array_gui_update_fn)

def update_array_map_plot(app, next_packet, CURRENT_THEME, themes, extra_params):
    print('update array map indicators()')
    update_array_map_indicators(app, next_packet, CURRENT_THEME, themes)

    colors, sizes = get_array_map_data(app)

    print('update array map data()')
    update_array_map_data(app, colors, sizes)
    print('update array map tooltip()')
    update_array_map_tooltip(app, colors)

def update_array_map_indicators(app, next_packet, CURRENT_THEME, themes):
    update_curr_scanning_elecs(app, next_packet, CURRENT_THEME, themes)
    update_minimap_indicator(app, CURRENT_THEME, themes)

def update_curr_scanning_elecs(app, next_packet, CURRENT_THEME, themes):
    print('update curr scanning elecs')
    # add squares around electrodes currently being recorded from + visualized in spike trace
    current_elec_scatter = pg.ScatterPlotItem(pxMode=False)
    current_recording_electrodes = []

    for i in range(len(next_packet['packet_data'])):
        chan_idx = next_packet['packet_data'][i]['channel_idx']

        from ..data.data_loading import idx2map
        row, col = idx2map(chan_idx)
        print('i', i, 'chan idx', chan_idx, 'r', row, 'c', col)
        spot_dict = {'pos': (col, row), 'size': 1,
                     'pen': {'color': pg.mkColor(themes[CURRENT_THEME]['light1']), 'width': 3},
                     'brush': QColor(255, 0, 255, 0),
                     'symbol': 's'}
        current_recording_electrodes.append(spot_dict)
    current_elec_scatter.addPoints(current_recording_electrodes)
    print('added current elec scatter')
    app.charts["arrayMap"].addItem(current_elec_scatter)

def update_minimap_indicator(app, CURRENT_THEME, themes):
    # add a square around electrodes displayed in the minimap
    minimap_square_indicator = pg.QtGui.QGraphicsRectItem(app.settings['cursor_row'] - 4.5,
                                                          app.settings['cursor_col'] - 2.5, 8, 4)
    minimap_square_indicator.setPen(pg.mkPen(themes[CURRENT_THEME]['blue3']))
    minimap_square_indicator.setBrush(QColor(255, 0, 255, 0))
    app.charts["arrayMap"].addItem(minimap_square_indicator)

def update_array_map_data(app, colors, sizes):
    # Set pxMode=False to allow spots to transform with the view
    scatter = pg.ScatterPlotItem(pxMode=False)

    # creating empty list for spots
    spots = []
    for i in range(32):
        for j in range(32):
            # creating  spot position which get updated after each iteration
            # of color which also get updated

            color_map = app.array_map_color_bar.colorMap()
            levels = app.array_map_color_bar.levels()

            value = colors[i, j]
            if value < levels[0]:
                value = levels[0]
            elif value > levels[1]:
                value = levels[1]

            adjusted_value = (value - levels[0]) / (levels[1] - levels[0])
            color_indicator = color_map.map(adjusted_value)

            spot_dic = {'pos': (j, i), 'size': sizes[i, j] / 60,
                        'pen': {'color': 'w', 'width': sizes[i, j] / 60},
                        'brush': pg.mkColor(color_indicator)}  # TODO fix coloring

            # used to be 'brush': pg.intColor(color_indicator, 100)
            # adding spot_dic in the list of spots
            spots.append(spot_dic)

        scatter.addPoints(spots)  # adding spots to the scatter plot
        app.charts["arrayMap"].addItem(scatter)  # adding scatter plot to the plot window

def update_array_map_tooltip(app, colors):
    image = pg.ImageItem(colors.T)  # for old pixel-based data # update
    #app.charts["arrayMap"].addItem(image)

    if app.arrayMapHoverCoords is not None:
        x, y = app.arrayMapHoverCoords
        if -1 <= x < 31 and 0 <= y < 32:
            spike_cnt = app.data.array_indexed['stats_spikes+cnt'][y][x + 1]
            spike_amp = app.data.array_indexed['stats_spikes+avg+amp'][y][x + 1]
            from ..data.data_loading import map2idx
            channel_idx = map2idx(y, x)

            tooltip_text = "<html>" + "Electrode Channel #" + str(channel_idx) + "<br>" + \
                           "Row " + str(y) + ", Column " + str(x) + "<br>" + \
                           "Spike Count: " + str(round(spike_cnt)) + "<br>" + \
                           "Spike Amplitude: " + str(round(spike_amp, 3)) + "<\html>"

            app.charts["arrayMap"].setToolTip(str(tooltip_text))

def on_color_bar_levels_changed(app):
    app.charts["arrayMap"].clear()

    colors = app.data.array_indexed['spike_avg']
    data = colors.T  # for old pixel-based data

    max_dot = 75
    # AX1) Size by Number of Samples
    spike_cnt = app.data.array_indexed['spike_cnt']
    scale1 = (max_dot - 15) / (np.max(spike_cnt) - np.min(spike_cnt[spike_cnt != 0]))
    b_add = max_dot - (np.max(spike_cnt) * scale1)
    size = np.round(spike_cnt * scale1 + b_add)
    size[size < 15] = 10  # TODO fix saturation point

    # Set pxMode=False to allow spots to transform with the view
    scatter = pg.ScatterPlotItem(pxMode=False)

    # creating empty list for spots
    spots = []

    # color modulated by amplitude
    import matplotlib as plt
    cmap = plt.cm.get_cmap("jet")

    for i in range(32):
        for j in range(32):
            # creating  spot position which get updated after each iteration
            # of color which also get updated

            import random
            if app.first_time_plotting is True:
                spot_dic = {'pos': (i, j), 'size': random.random() * 0.5 + 0.5,
                            'pen': {'color': 'w', 'width': 2},
                            'brush': pg.intColor(i * 10 + j, 100)}
            else:
                color_map = app.array_map_color_bar.colorMap()
                levels = app.array_map_color_bar.levels()

                value = colors[i, j]
                if value < levels[0]:
                    value = levels[0]
                elif value > levels[1]:
                    value = levels[1]

                adjusted_value = (value - levels[0]) / (levels[1] - levels[0])
                color_indicator = color_map.map(adjusted_value)

                spot_dic = {'pos': (j, i), 'size': size[i, j] / 60,
                            'pen': {'color': 'w', 'width': size[i, j] / 60},
                            'brush': pg.mkColor(color_indicator)}  # TODO fix coloring

                # used to be 'brush': pg.intColor(color_indicator, 100)
            # adding spot_dic in the list of spots
            spots.append(spot_dic)

    app.charts["arrayMap"].clear()
    scatter.addPoints(spots)  # adding spots to the scatter plot
    app.charts["arrayMap"].addItem(scatter)  # adding scatter plot to the plot window

# =====================
# NEW CODE
# ======================

def on_packet_update():
    pass

def on_color_bar_update():
    pass
