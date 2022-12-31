import pyqtgraph as pg
import numpy as np
import math

def clearSpikeSearchPlots(app):
    for chart in app.charts:
        app.charts[chart].clear()

def update_spike_search_plots(app, next_packet, CURRENT_THEME, themes, extra_params):
    """
    Returns:
    """
    # First, clear the plots
    clearSpikeSearchPlots(app)

    # Second, set up the plot figures for every electrode on the page
    # TODO make this code work
    #for elec in getTracesToPlot(app):
    #    row, col = electrodeToPlotGrid(app, elec)
    #    setupOneSpikeTrace(app.charts["r" + str(row) + "c" + str(col)], elec, CURRENT_THEME)

    from src.view.windows.window_individualchannel import IndividualChannelInformation
    individualChannel = IndividualChannelInformation()
    individualChannel.setSessionParent(app)

    pen = pg.mkPen(color=themes[CURRENT_THEME]['tracePlotting'])

    # Third, fill in plots with what model you have
    for elec in app.getTracesToPlot():
        individualChannel.current_elec = elec
        individualChannel.updateElectrodeData()

        # The Y range we display is [mean-app.yMin, mean+app.yMax]
        mean = np.nanmean(individualChannel.electrode_data)
        if math.isnan(mean):
            mean = 0
        lowerYBound = mean - int(app.yMin.value())
        upperYBound = mean + int(app.yMax.value())

        # If timeZoom, we want to zoom in on specific time windows of each trace
        if app.timeZoom:
            # The X range we display is based on which time step the user is on
            totalTime = len(individualChannel.electrode_times)
            if totalTime == 0:
                xRange = [0, 0]
            else:
                windowLength = int(totalTime / app.numberOfTimeSteps)
                startIdx = app.timeStep * windowLength
                xRange = [individualChannel.electrode_times[startIdx],
                          individualChannel.electrode_times[startIdx + windowLength - 1]]
            row, col = app.electrodeToPlotGrid(elec)
            gridToPlot = "r" + str(row) + "c" + str(col)
            app.charts[gridToPlot].plot(individualChannel.electrode_times,
                                         individualChannel.electrode_data, pen=pen)
            app.charts[gridToPlot].setYRange(lowerYBound, upperYBound, padding=0)
            app.charts[gridToPlot].setXRange(xRange[0], xRange[1], padding=0)

        # If timeZoom is false, we just want to display the whole trace, not zoomed in portions
        else:
            row, col = app.electrodeToPlotGrid(elec)
            gridToPlot = "r" + str(row) + "c" + str(col)
            app.charts[gridToPlot].plot(individualChannel.electrode_times,
                                         individualChannel.electrode_data, pen=pen)
            app.charts[gridToPlot].setYRange(lowerYBound, upperYBound, padding=0)
            app.charts[gridToPlot].enableAutoRange(axis='x', enable=True)

        # Spike highlighting
        if len(individualChannel.electrode_times) > 25:
            for spike in individualChannel.electrode_spike_times:
                lr = pg.LinearRegionItem([spike - 2, spike + 2])
                lr.setBrush(pg.mkBrush(themes[CURRENT_THEME]["spikeHighlighting"]))
                lr.setZValue(-5)
                app.charts[gridToPlot].addItem(lr)

# ================
# HELPER FUNCTIONS
def electrodeToPlotGrid(app, electrodeNum):
    """
    Args:
        electrodeNum: electrode number on RC array (0-1023)

    Returns: row, col (each between 0 and 5) for the 6x6 plot grid

    """
    electrodeNum = electrodeNum - 36 * app.pageNum
    row = int(electrodeNum / 6)
    col = int(electrodeNum - row * 6)
    return row, col

def getTracesToPlot(app):
    """
    Function to determine which electrodes to plot given what page of spike
    search GUI user is on

    Returns: 36 electrodes #s in a list

    """
    app.tracesToPlot.clear()
    for i in range(36):
        app.tracesToPlot.append(app.pageNum * 36 + i)
        app.FigureLabel.setText("Figure " + str(app.pageNum)
                                 + ": Ch " + str(app.tracesToPlot[0]) + " to Ch " + str(app.tracesToPlot[-1]))
    return app.tracesToPlot