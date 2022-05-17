import numpy as np
import pyqtgraph as pg

class HoverRegion():

    window = None
    region = None

    vLine, hLine = None, None
    vb = None
    proxy = None
    HoverFunc = None

    def __init__(self, window_ref, HoverFunc):
        self.window = window_ref
        self.region = pg.LinearRegionItem()
        self.HoverFunc = HoverFunc

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

    def update(self):
        self.region.setZValue(10)
        self.window.setXRange(-10, 40, padding=0)

    def updateRegion(self, window, viewRange):
        rgn = viewRange[0]
        self.region.setRegion(rgn)

    def mouseMoved(self, evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.window.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            self.HoverFunc(mousePoint.x(), mousePoint.y())


def setupArrayMap(plot_widget):
    plot_widget.setBackground('w')
    plot_widget.showGrid(x=True, y=True, alpha=0)
    plot_widget.setXRange(-10, 40, padding=0)
    plot_widget.setAspectLocked()
    plot_widget.setLimits(xMin=-10, xMax=45, yMin=-5, yMax=37)
    plot_widget.setLabel('top', "Spike Amplitude")
    plot_widget.setLabel('left', "Electrode No. (vertical)")
    plot_widget.setLabel('bottom', "Electrode No. (horizontal)")

def setupSpikeTrace(plot1, plot2, plot3, plot4):
    plot1.setBackground('w')
    plot2.setBackground('w')
    plot3.setBackground('w')
    plot4.setBackground('w')
    plot1.setLabel('left', "# XXX")
    plot2.setLabel('left', "# XXX")
    plot3.setLabel('left', "# XXX")
    plot4.setLabel('left', "# XXX")

def setupSpikeRatePlot(plot_widget):
    plot_widget.setLabel('top', "Channel Noise")
    plot_widget.setLabel('left', "Count")
    plot_widget.setLabel('bottom', "Std Dev")
    plot_widget.setLimits(xMin=0, yMin=0)
    plot_widget.setBackground('w')

    # init debug plot - make interesting distribution of values
    vals = np.hstack([np.random.normal(size=500), np.random.normal(size=260, loc=4)])

    # compute standard histogram
    y, x = np.histogram(vals, bins=np.linspace(-3, 8, 40))

    # We are required to use stepMode=True so that PlotCurveItem will interpret this data correctly.
    curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
    plot_widget.addItem(curve)

def setupNoiseHistogram(plot_widget):
    plot_widget.setBackground('w')
    plot_widget.showGrid(x=True, y=True, alpha=0)

    plot_widget.enableAutoRange(axis='x', enable=True)
    plot_widget.enableAutoRange(axis='y', enable=True)
    plot_widget.setLimits(xMin=0, yMin=0)

    plot_widget.setLabel('top', "Spike Rate")
    plot_widget.setLabel('left', "Spiking Frequency")
    plot_widget.setLabel('bottom', "Time (s)")

