import numpy as np
import pyqtgraph as pg
import math

from PyQt5 import QtGui
from PyQt5.QtGui import QColor

NUM_TOTAL_ROWS, NUM_TOTAL_COLS = 32, 32


def setupArrayMap(app, plot_widget, CURRENT_THEME: str, themes: dict):
    """

    Args:
        app: MainWindow
        plot_widget: reference to pyqtgraph widget
        CURRENT_THEME: current GUI theme
        themes: dictionary of theme colors

    Returns:
        None

    """
    plot_widget.showGrid(x=False, y=False, alpha=0)
    plot_widget.setAspectLocked()

    plot_widget.setLimits(xMin=-4, xMax=35,
                          yMin=-4, yMax =35,
                          minXRange=5, maxXRange=100,
                          minYRange=5, maxYRange=100)

    plot_widget.getPlotItem().hideAxis('top')
    plot_widget.getPlotItem().hideAxis('bottom')
    plot_widget.getPlotItem().hideAxis('left')
    plot_widget.getPlotItem().hideAxis('right')

    # plot_widget.setTitle(f'Array Map, Summary View', size='14pt', color=themes[CURRENT_THEME]['font_color'])
    print("SetupArrayMap is running.")

    cm = pg.colormap.get('autumn', source='matplotlib')

    colors = np.array(app.data.df["spikes_avg_amp"]).reshape((32, 32))

    # the pyqtgraph color bar REQUIRES it to be set to an image
    # however, we don't want to use an image, we want it to be linked with our scatter plot
    # so we make it, and set it off the screen
    tr = QtGui.QTransform()  # prepare ImageItem transformation:
    tr.translate(200, 200)  # scoot image out of view
    image = pg.ImageItem(colors.T)  # for old pixel-based model
    image.setTransform(tr)

    # bound the LinearRegionItem to the plotted model
    app.charts["arrayMap"].addItem(image)
    # TODO check if average spike amplitude makes sense w/ colors
    app.array_map_color_bar = app.charts["arrayMap"].addColorBar(image, colorMap=cm, label="Spike Amplitude",
                                                                values=(-10, 20))  # values=(0, np.max(model)))
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

def update_array_map_plot(app, next_packet, CURRENT_THEME: str, themes: dict, extra_params):
    """

    Args:
        app: MainWindow
        next_packet: data from the chip on the next buffer to be displayed
        CURRENT_THEME: current GUI theme
        themes: dictionary of theme colors
        extra_params:

    Returns:
        None

    """
    mode = extra_params
    app.charts["arrayMap"].setTitle(f'Array Map, {mode} View', size='14pt', color=themes[CURRENT_THEME]['font_color'])

    # CURRENT ELECTRODE BOX INDICATOR
    curr_rec_elecs_box = []
    dot_scaling_changed = False

    current_chan_idx = 0
    current_row = 0
    current_col = 0

    for i in range(len(next_packet['packet_data'])):
        # get packet info
        chan_idx = next_packet['packet_data'][i]['channel_idx']
        from src.model.data_loading_mat import idx2map
        row, col = idx2map(chan_idx)

        # add squares around electrodes currently being recorded from + visualized in spike trace
        spot_dict = {'pos': (col, row), 'size': 1,
                     'pen': {'color': pg.mkColor(themes[CURRENT_THEME]['blue1']), 'width': 2},
                     'brush': QColor(0, 0, 0, 0),
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
        recalculate_all_sizes(app)
        for i in range(len(next_packet['packet_data'])):
            chan_idx = next_packet['packet_data'][i]['channel_idx']
            idxs_to_change.append(chan_idx)
            if chan_idx not in app.indexesRec:
                app.indexesRec.append(chan_idx)
            calculate_one_elec_color_and_size(app, chan_idx)
            current_chan_idx = chan_idx
    else:  # calculate only for specific elecs in current buffer
        for i in range(len(next_packet['packet_data'])):
            chan_idx = next_packet['packet_data'][i]['channel_idx']
            idxs_to_change.append(chan_idx)
            if chan_idx not in app.indexesRec:
                app.indexesRec.append(chan_idx)
            calculate_one_elec_color_and_size(app, chan_idx)
            current_chan_idx = chan_idx
    

    # render all the points
    elecs_points = []
    color_map = app.array_map_color_bar.colorMap()
    for row in range(NUM_TOTAL_ROWS):
        for col in range(NUM_TOTAL_COLS):
            from src.model.data_loading_mat import map2idx
            idx = map2idx(row, col)
            if mode == 'Real-Time':
                if idx in idxs_to_change:
                    array_dot_color_idx = app.data.df.at[idx, "array_dot_color"]
                    color = color_map.map(array_dot_color_idx)
                    default_elec_dict = {'pos': (col, row), 'size': app.data.df.at[idx, "array_dot_size"],
                                'pen': color,
                                'brush': color,
                                'symbol': 'o'}
                else:
                    default_elec_dict = {'pos': (col, row), 'size': 0.1,
                                'pen': {'color': 'w'},
                                'brush': QColor(0, 0, 0, 0),
                                'symbol': 'o'}
            elif mode == 'Summary':
                if idx in app.indexesRec:
                    array_dot_color_idx = app.data.df.at[idx, "array_dot_color"]
                    color = color_map.map(array_dot_color_idx)
                    default_elec_dict = {'pos': (col, row), 'size': app.data.df.at[idx, "array_dot_size"],
                                    'pen': color,
                                    'brush': color,
                                    'symbol': 'o'}
                else:
                    default_elec_dict = {'pos': (col, row), 'size': 0.1,
                                'pen': {'color': 'w'},
                                'brush': QColor(0, 0, 0, 0),
                                'symbol': 'o'}
            elecs_points.append(default_elec_dict)

    elecs_plot = pg.ScatterPlotItem(pxMode=False)
    elecs_plot.addPoints(elecs_points)
    app.update_subplot_element("arrayMap", 'default_elecs_plot', elecs_plot)


def calculate_one_elec_color_and_size(app, idx: int):
    """

    Args:
        app: MainWindow
        idx: the index of the electrode (0-1023) to be calculated

    Returns:
        None

    """
    # calculate the dot color from electrode's average spike amplitude
    spike_avg_amp = app.data.df.at[idx, "spikes_avg_amp"]

    levels = app.array_map_color_bar.levels()
    spike_avg_amp = np.clip(spike_avg_amp, levels[0], levels[1])
    spike_avg_amp = (spike_avg_amp - levels[0]) / (levels[1] - levels[0])
    color = spike_avg_amp
    app.data.df.at[idx, "array_dot_color"] = color

    # calculate the dot size from electrode's average spike count
    spikes_cnt = app.data.df.at[idx, "spikes_cnt"]
    if app.data.stats["largest_spike_cnt"] == 0:
        size = app.settings["min_dot_size"]
    else:
        size = (spikes_cnt / app.data.stats["largest_spike_cnt"]) * app.settings["max_dot_size"]
        size = np.clip(size, app.settings["min_dot_size"], app.settings["max_dot_size"])
    app.data.df.at[idx, "array_dot_size"] = size
    return color, size

def recalculate_all_colors(app):
    """

    Args:
        app: MainWindow

    Returns:
        None

    """
    spikes_avg_amp = np.array(app.data.df["spikes_avg_amp"])
    levels = app.array_map_color_bar.levels()
    spikes_avg_amp = np.clip(np.abs(spikes_avg_amp), levels[0], levels[1])
    spikes_avg_amp = (spikes_avg_amp - levels[0]) / (levels[1] - levels[0])

    app.data.df["array_dot_color"] = spikes_avg_amp

def recalculate_all_sizes(app):
    """

    Args:
        app: MainWindow

    Returns:
        None

    """
    spikes_cnt = np.array(app.data.df["spikes_cnt"])
    if app.data.stats["largest_spike_cnt"] == 0:
        sizes = app.settings["min_dot_size"]
    else:
        sizes = (spikes_cnt / app.data.stats["largest_spike_cnt"]) * app.settings["max_dot_size"]
        sizes = np.clip(sizes, app.settings["min_dot_size"], app.settings["max_dot_size"])
    app.data.df["array_dot_size"] = sizes

    if app.arrayMapHoverCoords is not None:
        x, y = app.arrayMapHoverCoords
        if 0 <= x <= 31 and 0 <= y <= 31:
            from src.model.DC1DataContainer import map2idx
            idx = map2idx(x, y)
            spike_cnt = app.data.df.at[idx, "spikes_cnt"]
            spike_amp = app.data.df.at[idx, "spikes_avg_amp"]
            # spike_cnt = app.model.array_indexed['stats_spikes+cnt'][y][x + 1]
            # spike_amp = app.model.array_indexed['stats_spikes+avg+amp'][y][x + 1]
            from src.model.data_loading_mat import map2idx
            channel_idx = map2idx(y, x)
            tooltip_text = "<html>" + "Electrode Channel #" + str(channel_idx) + "<br>" + \
                           "Row " + str(y) + ", Column " + str(x) + "<br>" + \
                           "Spike Count: " + str(round(spike_cnt)) + "<br>" + \
                           "Spike Amplitude: " + str(round(spike_amp, 3)) + "<\html>"
            app.charts["arrayMap"].setToolTip(str(tooltip_text))


def on_color_bar_levels_changed(app):
    """ called when the color bar is interacted with by the user in the viewing mode, changes the
    colors of the dots on the array map

    Args:
        app: MainWindow

    Returns:
        None

    """
    recalculate_all_colors(app)
    elecs_points = []
    color_map = app.array_map_color_bar.colorMap()
    for row in range(NUM_TOTAL_ROWS):
        for col in range(NUM_TOTAL_COLS):
            from src.model.data_loading_mat import map2idx
            idx = map2idx(row, col)

            array_dot_color_idx = app.data.df.at[idx, "array_dot_color"]
            color = color_map.map(array_dot_color_idx)
            # color = color_map.map(app.data.df.at[idx, "array_dot_color"])

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
        """Updated when the mouse is moved by the user

        Args:
            evt: event encoded by PyQt

        Returns:
            None

        """
        pos = evt[0]  # using signal proxy turns original arguments into a tuple
        if self.window.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            self.last_mouse_x = mousePoint.x()
            self.last_mouse_y = mousePoint.y()
            self.HoverFunc(mousePoint.x(), mousePoint.y())

    def mouseClicked(self, evt):
        """Update when the mouse is clicked by the user

        Args:
            evt: event encoded by PyQt

        Returns:

        """
        pos = (self.last_mouse_x, self.last_mouse_y)
        #if self.window.sceneBoundingRect().contains(pos):
            # mousePoint = self.vb.mapSceneToView(pos)
        # print('entering click func')
        self.ClickFunc(self.last_mouse_x, self.last_mouse_y)


def update_minimap_indicator(app, CURRENT_THEME: str, themes: dict): # this is called on cursor click + on setup
    """add a square around electrodes displayed in the minimap

    Args:
        app: MainWindow
        CURRENT_THEME: current GUI theme
        themes: dictionary of theme colors

    Returns:
        None

    """

    minimap_square_indicator = pg.QtGui.QGraphicsRectItem(app.settings['cursor_row'] - 4.5,
                                                          app.settings['cursor_col'] - 2.5, 8, 4)
    minimap_square_indicator.setPen(pg.mkPen(themes[CURRENT_THEME]['light1']))
    minimap_square_indicator.setBrush(QColor(0, 0, 0, 0))
    app.update_subplot_element("arrayMap", 'minimap_square_indicator', minimap_square_indicator)


def update_mini_map_plot(app, next_packet, CURRENT_THEME, themes, extra_params):
    """

    Args:
        app:
        next_packet:
        CURRENT_THEME:
        themes:
        extra_params: 

    Returns:

    """
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
                from src.model.data_loading_mat import map2idx
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