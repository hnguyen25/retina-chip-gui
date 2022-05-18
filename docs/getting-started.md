## Conda Environment - dc1_vis.yml
Contains all the packages needed to run visualizations

## Development - Important Files

### dc1DataVis/run.py
Startup file

### dc1DataVis/src/gui/gui_base.py
Basis for the entire GUI. Every other script links to this file! If unsure what a file does, check where it is loaded in relation to this file.

## Development - GUI stuff
### dc1DataVis/src/gui/*.ui
All of these files were made and can be viewed using software called Qt Designer. These files layout out the structure for every GUI panel. Associated .py files with the same filename generate from these .ui files and are convenient to know how to reference different pyqtgraph elements.

### dc1DataVis/src/gui/gui_charts_helper.py
Code to setup every analysis chart

## Development - data processing

### dc1DataVis/src/data/DC1DataContainer.py
this class is instantiated in gui_base and basically holds all the possible data that is loaded up during the session runtime

### dc1DataVis/src/data/data_loading.py
misc functions related to loading .MAT / .NPZ files

### dc1DataVis/src/data/preprocessing.py
contains functions that sorts out the relevant channels that are being recorded at any one time

### dc1DataVis/src/data/filters.py
self explanatory
