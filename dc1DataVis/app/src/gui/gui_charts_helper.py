import numpy as np
import pyqtgraph as pg

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
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.window.addItem(self.vLine, ignoreBounds=True)
        self.window.addItem(self.hLine, ignoreBounds=True)
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
        print('entering click func')
        self.ClickFunc(self.last_mouse_x, self.last_mouse_y)

def setupArrayMap(plot_widget):
    plot_widget.showGrid(x=True, y=True, alpha=0)
    plot_widget.setXRange(-10, 40, padding=0)
    plot_widget.setAspectLocked()
    plot_widget.setLimits(xMin=-10, xMax=45, yMin=-5, yMax=37)
    plot_widget.setLabel('top', "Spike Amplitude")
    plot_widget.setLabel('left', "Electrode No. (vertical)")
    plot_widget.setLabel('bottom', "Electrode No. (horizontal)")

def setupMiniMapPlot(plot_widget, center_row=16, center_col=16):
    plot_widget.showGrid(x=True, y=True, alpha=0)
    plot_widget.getPlotItem().hideAxis('bottom')
    plot_widget.getPlotItem().hideAxis('left')
    plot_widget.enableAutoRange(axis='x', enable=True)
    plot_widget.enableAutoRange(axis='y', enable=True)
    plot_widget.setAspectLocked()

    for row in range(center_row-5, center_row+5):
        for col in range(center_col-3, center_col+3):

            spike_indicator_base = pg.QtGui.QGraphicsRectItem(row*5, col*5, 4, 0.2)
            spike_indicator_base.setPen(pg.mkPen((0, 0, 0, 100)))
            spike_indicator_base.setBrush(pg.mkBrush((50, 50, 200)))

            elec_idx = str(map2idx(col, row))
            spike_indicator_text = pg.TextItem(elec_idx,
                                               'k',
                                               anchor=(0,0))
            spike_indicator_text.setPos(row*5, col*5)
            spike_indicator_text.setParentItem(spike_indicator_base)

            plot_widget.addItem(spike_indicator_base)
            plot_widget.addItem(spike_indicator_text)


def setupSpikeTrace(plot1, plot2, plot3, plot4):
    plot1.setLabel('left', "# XXX")
    plot2.setLabel('left', "# XXX")
    plot3.setLabel('left', "# XXX")
    plot4.setLabel('left', "# XXX")

def setupOneSpikeTrace(plot_widget):
    plot_widget.setLabel('left', '# XXX')
    plot_widget.setLabel('bottom', 'time')

def setupSpikeRatePlot(plot_widget):
    plot_widget.setLabel('top', "Channel Noise")
    plot_widget.setLabel('left', "Count")
    plot_widget.setLabel('bottom', "Std Dev")

    plot_widget.setLimits(xMin=0, yMin=0)

    # init debug plot - make interesting distribution of values
    vals = np.hstack([np.random.normal(size=500), np.random.normal(size=260, loc=4)])

    # compute standard histogram
    y, x = np.histogram(vals, bins=np.linspace(-3, 8, 40))

    # We are required to use stepMode=True so that PlotCurveItem will interpret this data correctly.
    curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
    plot_widget.addItem(curve)

def setupNoiseHistogram(plot_widget):

    plot_widget.showGrid(x=True, y=True, alpha=0)

    plot_widget.enableAutoRange(axis='x', enable=True)
    plot_widget.enableAutoRange(axis='y', enable=True)
    plot_widget.setLimits(xMin=0, yMin=0)

    plot_widget.setLabel('top', "Spike Rate")
    plot_widget.setLabel('left', "Spiking Frequency")
    plot_widget.setLabel('bottom', "Time (s)")

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
