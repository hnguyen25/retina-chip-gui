import unittest

from src.controller.windows.window_sessionstartup import SessionStartupGUI
from app.run import *
from PyQt5.QtTest import QTest
from PyQt5.Qt import Qt

import logging
logger = logging.getLogger(__name__)
logger.debug("testing 1 2 3!")

# test testing capability -> confirmed this works
def test_func_case_1():
    assert True
def test_func_case_2():
    assert 1 == 1

def test_initialization(qtbot):
    os.chdir("app")
    base_dir = os.getcwd()

    DEBUG_STARTUP = {
        'threshold_min': 1, 'threshold_max': 8, 'threshold_default': 4,
        'default_dataset_path': 'debugData/2022-02-18-0/data001'
    }
    widget = SessionStartupGUI(base_dir, DEBUG_STARTUP)
    qtbot.addWidget(widget)
    assert widget.chooseSpikeDetectionMethod.currentText() == "Noise-Based"

    # ex: click in the Greet button and make sure it updates the appropriate label
    # qtbot.mouseClick(widget.button_greet, qt_api.QtCore.Qt.MouseButton.LeftButton)