# Development Getting Started Guide

Note: If you would like to know how to run a compiled version of the app, refer to [Intro to the GUI](intro-to-gui.md)

## 1. Setting up the development environment

The retina chip GUI is built completely in Python, the GUI is written with `PyQt5`, the plots with `PyQtGraph`, and the 
data is manipulated through a combination of `numpy`, `pandas`, and `scipy`.
Any IDE which can be used to edit Python code is suitable for development purposes.

### a. Conda environment

Install and setup [Anaconda](https://docs.anaconda.com/anaconda/install/).

Within the [Github Repository](https://github.com/hnguyen25/artifical-retina-pipeline-guis), the file **dc1_vis.yml** 
contains a list of all the packages needed to set up the development environment. A new conda environment with all the
necessary packages can be installed with the command:
`conda env create --name rc1-gui --file dc1_vis.yml`

Note: this package list contains the relevant packages to run on MacOS + Apple Silicon (Huy's current development environment.)
If certain packages don't install properly, this is probably because there are platform (i.e. Windows, MacOS Intel) 
specific packages for them. Just `conda install <insert-package-name>` the packages that do not install properly.

### b. Github Repository
Clone code from the [Github Repository](https://github.com/hnguyen25/artifical-retina-pipeline-guis).

### Additional Information: PyQt and PyQtGraph
Use PyQt5 (the latest version) and PyQtGraph (specifically the v0.12 builds).

For more information about the library, refers to these useful links:

**PyQt5 Official Documentation**: https://doc.qt.io/qtforpython/

**PyQt5 Useful Tutorials:**: https://www.pythonguis.com/pyqt5/

**PyQtGraph Official Documentation**: https://pyqtgraph.readthedocs.io/en/latest/developer_guide/index.html


## 2. Running developer build for the first time

This GUI can be run either within the terminal or inside a Python IDE such as PyCharm.

### a. To run in terminal
1. On new terminal session, `conda activate <name-of-env>` to load relevant Python libraries
2. Navigate to the location of `run.py` within the cloned repository
3. Execute command `python run.py`

### b. To run in PyCharm
1. The top-right bar should contain drop down menu to choose run configuration. Click on `Edit configurations...`
2. Create a new configuration or edit an existing one
3. Change the `Script path` to the location of `run.py`, i.e. `/dc1DataVis/app/run.py`
4. Setup Python interpreter to be the Conda environment which you setup in part 1
5. The GUI should load when you press the play button now

## 3. Notes on important files and where files are located (last updated Jan 2023)

Executing `/app/run.py` will startup the application. The beginning of the file contains editable parameters
that will be passed through to the application (`MainWindow.py`) for the session, which can be modified by the developer.
It will also be possible to toggle these parameters within the GUI in the future.

Other than `run.py`, the entire codebase for the GUI is located within the folder `dc1DataVis/app/src`. Every file
within the `src` folder should have a corresponding documentation page within this wiki.

### `src/MainWindow.py`
The main application for the entire GUI! Every other script links to this file or run.py. If unsure what a file does,
check where it is loaded in relation to this file.

The rest of the application logic is split in a standard MVC (model-view-control) pattern, as distinguished by folders
with the respective role.

#### `src/Model`
Files associated with loading, processing, and retrieving data for visualization.1

#### `src/View`
Files associated with the layout of the GUI elements themselves (designed in QtDesigner), and associated color themes

#### `src/Controller`
Any logic to show or manipulate GUI windows, whether through user input and automatically through the course of the
program.

### `src/Testing`
This contains all the test cases for unit testing the GUI.