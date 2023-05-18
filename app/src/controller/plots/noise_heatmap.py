import pandas as pd
import pyqtgraph as pg
import numpy as np
import time

def update_noise_heat_map(app, next_packet, CURRENT_THEME, themes, extra_params, debug=False):
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
    start_time = time.time ()
    plot = app.charts["noiseHeatMap"]
    plot.clear()

    font = pg.QtGui.QFont()
    font.setPixelSize(20)

    plot.getAxis("bottom").tickFont = font
    plot.getAxis("bottom").setStyle(tickTextOffset=1)

    if app.first_time_plotting is False:
        data = app.data.df["noise_std"]
        #model = app.model.array_indexed["stats_noise+std"]
        data = data.T
    else:
        data = None

    img = pg.ImageItem(data)
    cm = pg.colormap.get('autumn', source='matplotlib')
    plot.addItem(img)

    if app.noise_heat_map_color_bar is None:
        app.noise_heat_map_color_bar = app.charts["noiseHeatMap"].addColorBar(img, colorMap=cm, label="Noise SD",
                                                                                values=(0, 5))
    else:
        app.noise_heat_map_color_bar.setImageItem(img)

    app.first_time_plotting = False

    if debug:
        print("Data" + str(data))

    # new_data = {
    #     "name": plot,
    #     "type": "update noise heat map",
    #     "time elapsed": round(time.time() - start_time, 5),
    #     "timestamp": round(start_time, 5)
    # }
    #
    # app.profiling_df.append (new_data, ignore_index=True)
    # app.profiling_df.to_csv ('retina-chip-gui/diagnostics.csv')
    # print ("Time elapsed (update noise heatmap): " + str(new_data["time elapsed"]))




def update_noise_heat_map(app, next_packet, CURRENT_THEME, themes, extra_params, debug=False):
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
    start_time = time.time()
    plot = app.charts["noiseHeatMap"]
    plot.clear()

    font = pg.QtGui.QFont()
    font.setPixelSize(20)

    plot.getAxis("bottom").tickFont = font
    plot.getAxis("bottom").setStyle(tickTextOffset=1)
    if app.first_time_plotting is False:
        data = app.data.df["noise_std"]
        #app.data.df["noise_std"] is a 1024x1 pandas array, transform this into a 32x32 numpy array
        data = np.array(data).reshape((32,32))
        data = data.T
    else:
        data = None

    img = pg.ImageItem(data)
    cm = pg.colormap.get('plasma', source='matplotlib')
    plot.addItem(img)

    if app.noise_heat_map_color_bar is None:
        app.noise_heat_map_color_bar = app.charts["noiseHeatMap"].addColorBar(img, colorMap=cm, label="Noise SD",
                                                                                values=(0, 5))
    else:
        app.noise_heat_map_color_bar.setImageItem(img)

    app.first_time_plotting = False

    if debug:
        print("Data" + str(data))

    elapsed_time = round(time.time() - start_time, 5)
    app.profiling_dict["update noise heatmap"].append(elapsed_time)
    app.profiling_df = pd.DataFrame({key:pd.Series(value) for key, value in app.profiling_dict.items()})

    #app.profiling_df.to_csv('/Users/sahilsmac/Documents/Test Modules/diagnostics.csv')
    print("Time elapsed (update noise heatmap): " + str(elapsed_time))