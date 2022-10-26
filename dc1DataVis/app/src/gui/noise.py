import pyqtgraph as pg
import numpy as np

def update_noise_heat_map(app, next_packet, CURRENT_THEME, themes, extra_params, debug=False):
    plot = app.charts["noiseHeatMap"]
    plot.clear()

    font = pg.QtGui.QFont()
    font.setPixelSize(20)

    plot.getAxis("bottom").tickFont = font
    plot.getAxis("bottom").setStyle(tickTextOffset=1)

    if app.first_time_plotting is False:
        data = app.data.array_indexed["stats_noise+std"]
        data = data.T
    else:
        data = None

    img = pg.ImageItem(data)
    cm = pg.colormap.get('plasma', source='matplotlib')
    plot.addItem(img)

    if app.noise_heat_map_color_bar is None:
        app.noise_heat_map_color_bar = app.charts["noiseHeatMap"].addColorBar(img, colorMap=cm, label="Noise SD",
                                                                                values=(0, 10))
    else:
        app.noise_heat_map_color_bar.setImageItem(img)

    app.first_time_plotting = False

    if debug:
        print("Data" + str(data))

def update_noise_histogram_plot(app, next_packet, CURRENT_THEME, themes, debug=False, colored=True):
    """
    @param debug: if true, prints helpful information
    @param colored: if true, plots normal range of histogram and colors according to bin. false plots single
    color with larger range, used primarily for debugging array_indexed
    @return:
    """

    app.charts["noiseHistogram"].clear()

    vals = app.data.array_indexed['stats_noise+std'].copy()
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