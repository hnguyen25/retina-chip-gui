from PyQt5.QtGui import QColor

NUM_TOTAL_ROWS, NUM_TOTAL_COLS = 32, 32
import pyqtgraph as pg

class PGPlotPerElectrodeRendering():
    """
    Code to visualize spatial data in an efficient data. Since not all electrodes receive information at once
    from array, just update the electrodes with new information, keeping the rest static.

    Useful for entire array map + minimap.
    """
    CENTER_X, CENTER_Y = 0, 0
    LIST_OF_ELECTRODES_WITHIN_BOUNDS = []

    def __init__(self, app_ref, plot_ref, WIDTH, HEIGHT, data_keys, gui_update_fn):
        """
        Args
            app_ref:
            plot_ref: TODO write documentation
            NUM_ROWS
            NUM_COLS
            data_keys
            vis_update_fn
            data_update_fn

        Example
            PGPlotPerElectrodeRendering(array_map_plot, 32, 32,
                                        ["spike_count", "avg_spike_amp", "last_update", "channel_noise"],
                                        array_gui_update_fn)
            def array_gui_update_fn:
                ...
                ...
            def array_data_update_fn:
                ...
                ...

            OR

            PGPlotPerElectrodeRendering(minimap_plot, 8, 4,
                            ["spike_times", "spike_amps"],
                            minimap_gui_update_fn)

        """
        self.app = app_ref
        self.plot_ref = plot_ref
        self.gui_update_fn = gui_update_fn

        self.update_map_bounds(16, 16)  # 16/32, 16/32
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        data_dict = {key: -1 for key in data_keys}
        self.data = [data_dict for i in range(NUM_TOTAL_ROWS * NUM_TOTAL_COLS)]
        self.refs = [{} for i in range(NUM_TOTAL_ROWS * NUM_TOTAL_COLS)]

    def update_map_bounds(self, NEW_CENTER_X, NEW_CENTER_Y):
        self.CENTER_X, self.CENTER_Y = NEW_CENTER_X, NEW_CENTER_Y
        self.LIST_OF_ELECTRODES_WITHIN_BOUNDS = []
        for i in range(NEW_CENTER_X - self.WIDTH // 2, NEW_CENTER_X + self.WIDTH // 2):
            for j in range(NEW_CENTER_Y - self.HEIGHT // 2, NEW_CENTER_Y + self.HEIGHT // 2):
                self.LIST_OF_ELECTRODES_WITHIN_BOUNDS.append(map2idx(i, j))

    def update_electrode_data(self, idx, new_data_dict):
        for key in new_data_dict.keys():
            self.data[idx][key] = new_data_dict[key]

    def update_vis_electrode(self, plot, idx):
        x, y = idx2map(idx)

        # clear prior references
        if len(self.refs[idx]) > 0:
            prior_elec_refs = self.refs[idx]
            for ref in prior_elec_refs:
                self.plot_ref.removeItem(ref)
            self.refs[idx] = {}

        # update with new info
        self.refs[idx] = self.gui_update_fn(x, y, self.data[idx])
        for ref in self.refs[idx]:
            self.plot_ref.addItem(ref)

    def update_vis_list_of_electrodes(self, plot, list_of_idx):
        to_update = list(set(list_of_idx) & set(self.LIST_OF_ELECTRODES_WITHIN_BOUNDS))
        for idx in to_update:
            self.update_vis_electrode(plot, idx)

    def refresh_vis_all_array(self, plot):
        for idx in self.LIST_OF_ELECTRODES_WITHIN_BOUNDS:
            self.update_vis_electrode(plot, idx)

def array_gui_update_fn(x, y, data):
    size, color = data["size"], data["color"]

    # draw a circle with a certain size and color
    circle_ref = pg.QtGui.QGraphicsEllipseItem(x, y, size, size)  # x, y, width, height
    circle_ref.setPen(pg.mkPen(color))
    circle_ref.setBrush(pg.mkBrush(color))
    return {'circle_ref': circle_ref}

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

def idx2map(ch_idx: int):
    """ Given a channel index, return the channel's row and col
    Args:
        ch_idx: single numerical index for array (up to 1024)

    Returns:
        channel row and channel index
    """
    if ch_idx > 1023 or ch_idx < 0:
        print('Chan num out of range')
        return -1
    else:
        ch_row = int(ch_idx / 32)
        ch_col = int(ch_idx - ch_row * 32)
    return ch_row, ch_col
def map2idx(ch_row: int, ch_col: int):
    """ Given a channel's row and col, return channel's index

    Args:
        ch_row: row index of channel in array (up to 32)
        ch_col: column index of channel in array (up to 32)

    Returns: numerical index of array
    """
    if ch_row > 31 or ch_row <0:
        print('Row out of range')
    elif ch_col >31 or ch_col<0:
        print('Col out of range')
    else:
        ch_idx = int(ch_row*32 + ch_col)
    return ch_idx