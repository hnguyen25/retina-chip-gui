import numpy as np
import pyqtgraph as pg

CURRENT_THEME = 'light'

light_theme_colors = {
    'dark1': '#2E3440',
    'dark2': '#3B4252',
    'background_light': '#ECEFF4',
    'background_light2': '#E5E9F0',
    'background_light3': '#D8DEE9',
    'blue1': '#5E81AC',
    'blue2': '#81A1C1',
    'blue3': '#88C0D0',
    'blue4': '#8FBCBB',
    'red': '#BF616A',
    'orange': '#D08770',
    'yellow': '#EBCB8B',
    'green': '#A3BE8C',
    'purple': '#B48EAD'
}

dark_theme_colors = {
}

themes = {
    'light': light_theme_colors,
    'dark': dark_theme_colors
}

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

        # cross hair
        #self.vLine = pg.InfiniteLine(angle=90, movable=False)
        #self.hLine = pg.InfiniteLine(angle=0, movable=False)
        #self.window.addItem(self.vLine, ignoreBounds=True)
        #self.window.addItem(self.hLine, ignoreBounds=True)
        self.vb = self.window.plotItem.vb
        self.proxy = pg.SignalProxy(self.window.scene().sigMouseMoved,
                                    rateLimit=60,
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

def setupArrayMap(plot_widget):
    plot_widget.showGrid(x=True, y=True, alpha=0)
    plot_widget.setAspectLocked()
    plot_widget.setLimits(xMin=-5, xMax=37,
                          yMin=-2, yMax=33,
                          minXRange=5, maxXRange=55,
                          minYRange=5, maxYRange=42)
    plot_widget.getPlotItem().hideAxis('top')
    plot_widget.getPlotItem().hideAxis('bottom')
    plot_widget.getPlotItem().hideAxis('left')
    plot_widget.getPlotItem().hideAxis('right')

def setupMiniMapPlot(plot_widget, center_row=16, center_col=16):
    plot_widget.showGrid(x=True, y=True, alpha=0)
    plot_widget.getPlotItem().hideAxis('bottom')
    plot_widget.getPlotItem().hideAxis('left')
    plot_widget.enableAutoRange(axis='x', enable=True)
    plot_widget.enableAutoRange(axis='y', enable=True)
    plot_widget.setAspectLocked()


def setupSpikeTrace(list_of_plots):
    for plot in list_of_plots:

        plot.setLabel('left', '# ???')
        plot.getAxis('left').setTextPen(themes[CURRENT_THEME]['dark1'])
        #plot.getPlotItem().hideAxis('bottom')
        plot.getAxis("bottom").setTextPen(themes[CURRENT_THEME]['dark1'])
        plot.setLabel('bottom', 'Time (ms)')



def setupOneSpikeTrace(plot_widget,label):
    color = 'g'
    if CURRENT_THEME == 'light':
        color = 'k'
        print("here")
    plot_widget.setTitle('Ch #  ' + str(label), color = color, size = '10pt')
    plot_widget.setLabel('bottom', 'time')



# TODO: fix the swap on the next two functions
def setupNoiseHistogramPlot(plot_widget):

    plot_widget.setLabel('left', "Num Channels")
    plot_widget.setLabel('bottom', "Standard Deviations")
    plot_widget.setLabel('top', 'Channel Noise')

    plot_widget.setLimits(xMin=0, yMin=0)

    plot_widget.getPlotItem().getAxis('top').setTextPen(pg.mkPen(None))
    plot_widget.getPlotItem().hideAxis('top')
    plot_widget.getAxis("left").setTextPen("#2E3440")
    plot_widget.getAxis("bottom").setTextPen("#2E3440")


def setupSpikeRatePlot(plot_widget):

    plot_widget.showGrid(x=True, y=True, alpha=0)

    plot_widget.enableAutoRange(axis='x', enable=True)
    plot_widget.enableAutoRange(axis='y', enable=True)
    plot_widget.setLimits(xMin=0, yMin=0)

    plot_widget.getPlotItem().hideAxis('top')
    plot_widget.setLabel('left', "Spike Rate")
    plot_widget.getAxis("left").setTextPen(themes[CURRENT_THEME]['dark1'])

    plot_widget.setLabel('bottom', "Time (ms)")
    plot_widget.getAxis("bottom").setTextPen(themes[CURRENT_THEME]['dark1'])
    plot_widget.setLimits(xMin=0, yMin=0, minXRange=5)


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
