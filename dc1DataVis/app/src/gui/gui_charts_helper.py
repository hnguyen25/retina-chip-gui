import numpy as np
import pyqtgraph as pg

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
    plot_widget.setLabel('top', "Noise")
    plot_widget.setLabel('left', "Count")
    plot_widget.setLabel('bottom', "Standard Dev")
    plot_widget.setLimits(xMin=0, yMin=0)
    plot_widget.setBackground('w')

    # init debug plot - make interesting distribution of values
    vals = np.hstack([np.random.normal(size=500), np.random.normal(size=260, loc=4)])

    # compute standard histogram
    y, x = np.histogram(vals, bins=np.linspace(-3, 8, 40))

    # We are required to use stepMode=True so that PlotCurveItem will interpret this data correctly.
    curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
    plot_widget.addItem(curve)