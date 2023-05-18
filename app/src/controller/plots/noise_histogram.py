import pyqtgraph as pg
import numpy as np
import pandas as pd
import time

def setupNoiseHistogramPlot(plot_widget, CURRENT_THEME, themes):
    """

    Args:
        plot_widget:
        CURRENT_THEME:
        themes:

    Returns:

    """
    print("set up noise histogram. ")
    plot_widget.getAxis("left").setTextPen(themes[CURRENT_THEME]['font_color'])
    plot_widget.getAxis("bottom").setTextPen(themes[CURRENT_THEME]['font_color'])
    plot_widget.getAxis('top').setTextPen(themes[CURRENT_THEME]['font_color'])
    plot_widget.setLabel('left', "Num Channels")
    plot_widget.setLabel('bottom', "Standard Deviations")
    plot_widget.setTitle('Channel Noise', size='14pt', color=themes[CURRENT_THEME]['font_color'])

    plot_widget.setLimits(xMin=0, yMin=0)
    font = pg.Qt.QtGui.QFont()
    font.setPixelSize(20)
    plot_widget.getAxis("bottom").tickFont = font
    plot_widget.getAxis("bottom").setStyle(tickTextOffset=1)
    plot_widget.getPlotItem().hideAxis('top')

def update_noise_histogram_plot(app, next_packet, CURRENT_THEME, themes, debug=False, colored=True):
    """

    Args:
        app:
        next_packet:
        CURRENT_THEME:
        themes:
        debug: if true, prints helpful information
        colored: if true, plots normal range of histogram and colors according to bin. false plots single
    color with larger range, used primarily for debugging array_indexed

    Returns:

    """

    start_time = time.time ()
    app.charts["noiseHistogram"].clear()

    vals = np.array(app.data.df["noise_std"]).copy()
    #vals = app.model.array_indexed['stats_noise+std'].copy()
    vals = vals[np.nonzero(vals)]

    cm = pg.colormap.get('autumn', source='matplotlib')

    if debug:
        print("updating noise histogram plot")
        print("vals: " + str(vals))

    if colored:
        y, x = np.histogram(vals, bins=np.linspace(0, 20, 50))

        colors = cm.getColors()

        scale = (int(len(colors) / 10))

        for i in range(len(x) - 1):
            bins = [x[i], x[i + 1]]
            values = [y[i]]

            color = int(scale * x[i])

            if color > 255:
                color = 255

            curve = pg.PlotCurveItem(bins, values, stepMode=True, fillLevel=0,
                                     brush=colors[color])

            app.charts["noiseHistogram"].addItem(curve)


    else:
        y, x = np.histogram(vals, bins=np.linspace(0, 50, 100))
        curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
        app.charts["noiseHistogram"].addItem(curve)

def update_noise_histogram_plot(app, next_packet, CURRENT_THEME, themes, debug=False, colored=True):
    """
    @param debug: if true, prints helpful information
    @param colored: if true, plots normal range of histogram and colors according to bin. false plots single
    color with larger range, used primarily for debugging array_indexed
    @return:
    """

    start_time = time.time()
    app.charts["noiseHistogram"].clear()
    vals = np.array(app.data.df["noise_std"])
    #vals = app.model.array_indexed['stats_noise+std'].copy()
    vals = vals[np.nonzero(vals)]

    cm = pg.colormap.get('plasma', source='matplotlib')

    if debug:
        print("updating noise histogram plot")
        print("vals: " + str(vals))

    if colored:
        y, x = np.histogram(vals, bins=np.linspace(0, 20, 50))

        colors = cm.getColors()

        scale = (int(len(colors) / 10))

        for i in range(len(x) - 1):
            bins = [x[i], x[i + 1]]
            values = [y[i]]

            color = int(scale * x[i])

            if color > 255:
                color = 255

            curve = pg.PlotCurveItem(bins, values, stepMode=True, fillLevel=0,
                                     brush=colors[color])

            app.charts["noiseHistogram"].addItem(curve)


    else:
        y, x = np.histogram(vals, bins=np.linspace(0, 50, 100))
        curve = pg.PlotCurveItem(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
        app.charts["noiseHistogram"].addItem(curve)

    elapsed_time = round(time.time() - start_time, 5)
    app.profiling_dict["update noise histogram"].append(elapsed_time)
    app.profiling_df = pd.DataFrame({key:pd.Series(value) for key, value in app.profiling_dict.items()})

    #app.profiling_df.to_csv('/Users/sahilsmac/Documents/Test Modules/diagnostics.csv')
    print("Time elapsed (update noise histogram): " + str(elapsed_time))