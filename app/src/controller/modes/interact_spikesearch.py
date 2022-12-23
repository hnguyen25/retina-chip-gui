import pyqtgraph as pg

def resetSpikeSearchPlotParams(app):
    app.yMax.setValue(20)
    app.yMin.setValue(30)
    app.timeZoom = True
    app.timeStep = 0
    app.update_spike_search_plots()

def switchTimeZoom(app):
    app.timeZoom = not app.timeZoom
    app.timeStep = 0
    app.update_spike_search_plots()

def nextPage(app):
    if app.pageNum < 28:
        app.pageNum += 1
        app.FigureLabel.setText("Page: " + str(app.pageNum))
        app.timeStep = 0
        app.update_spike_search_plots()


def backPage(app):
    if app.pageNum > 0:
        app.pageNum -= 1
        app.FigureLabel.setText("Page: " + str(app.pageNum))
        app.timeStep = 0
        app.update_spike_search_plots()

def timeStepUp(app):
    if app.timeStep < app.numberOfTimeSteps - 1:
        app.timeStep += 1
        app.update_spike_search_plots()

def timeStepDown(app):
    if app.timeStep > 0:
        app.timeStep -= 1
        app.update_spike_search_plots()
