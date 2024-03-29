import pyqtgraph as pg
from src.model.DC1DataContainer import *
from src.MainWindow import *

def setupSpikeRatePlot(plot_widget, CURRENT_THEME, themes):
    """

    Args:
        plot_widget:
        CURRENT_THEME:
        themes:

    Returns:

    """
    plot_widget.getAxis("left").setTextPen(themes[CURRENT_THEME]['font_color'])
    plot_widget.getAxis("bottom").setTextPen(themes[CURRENT_THEME]['font_color'])
    plot_widget.getAxis('top').setTextPen(themes[CURRENT_THEME]['font_color'])
    plot_widget.showGrid(x=True, y=True, alpha=0)

    plot_widget.enableAutoRange(axis='x', enable=True)
    plot_widget.enableAutoRange(axis='y', enable=True)
    plot_widget.setLimits(xMin=0, yMin=0)

    plot_widget.getPlotItem().hideAxis('top')
    plot_widget.setLabel('left', "Spike Rate",  size = '12pt', color=themes[CURRENT_THEME]['font_color'])
    plot_widget.setLabel('bottom', "Time (ms)",  size = '12pt', color=themes[CURRENT_THEME]['font_color'])
    plot_widget.setTitle("Array Spike Rate",  size = '14pt', color=themes[CURRENT_THEME]['font_color'])
    plot_widget.setLimits(xMin=0, yMin=0, minXRange=5)
    plot_widget.setLimits(xMin=0, yMin=-5, minXRange=5)
    plot_widget.enableAutoRange(axis='x')

def update_spike_rate_plot(app, next_packet, CURRENT_THEME, themes, extra_params, debug=False):
    """

    Args:
        app:
        next_packet:
        CURRENT_THEME:
        themes:
        extra_params:
        debug:

    Returns:

    """
    app.charts["spikeRatePlot"].clear()

    #print("avgspikerate x/y", app.model.avg_spike_rate_x, app.model.avg_spike_rate_y)
    app.charts["spikeRatePlot"].plot(app.data.avg_spike_rate_x,
                                     app.data.avg_spike_rate_y,
                                     pen=pg.mkPen(themes[CURRENT_THEME]['font_color'], width=5))
    #app.charts["spikeRatePlot"].setYRange(0, max(app.model.avg_spike_rate_y) + 5, padding=0.1)



