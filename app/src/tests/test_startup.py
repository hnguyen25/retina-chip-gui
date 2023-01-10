import unittest

from app.run import *
from PyQt5.QtTest import QTest
from PyQt5.Qt import Qt

# test testing capability
def test_func_case_1():
    assert True
def test_func_case_2():
    assert 1 == 1

def start_app_for_testing():
    base_dir = os.path.dirname(__file__)
    os.chdir(base_dir)
    print("Application starting from base directory", base_dir)

    if os.path.basename(os.getcwd()) == "tests":
        os.chdir("../../")
        print(os.getcwd())

    if DEBUG_SETTINGS['is_mode_multithreading']: mp.set_start_method('spawn')

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  # fix Windows scaling issue
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)  # use high DPI icons
    app.setStyleSheet("QWidget { font: 14px; }")
    app.setStyleSheet("""QToolTip { 
                                   background-color: black; 
                                   color: white; 
                                   border: black solid 1px
                                   }""")
    app.setStyleSheet("QStatusBar{padding-left:8px;color:white;font-weight:bold;font-family:'Arial'}")

    session_startup = SessionStartupGUI(base_dir, DEBUG_STARTUP)  # load initial startup window where user can specify session
    return app, session_startup
    """
    if session_startup.exec():  # continue running app only if user has successfully completed startup window

        SESSION_SETTINGS = session_startup.settings
        print("SESSION_SETTINGS", SESSION_SETTINGS)
        settings = {**SESSION_SETTINGS, **DEBUG_SETTINGS} # get all settings, both from user and developer

        # start analysis window of choice
        window = MainWindow(settings=settings, window_title=APP_TITLE)
        window.resize(WINDOWED_APP_SIZE[0], WINDOWED_APP_SIZE[1])
        window.show()
        app.exec()

    print('Application completed. Killing process...')
    app.quit()
    """

"""
class TestStartupSessionGUI(unittest.TestCase):
    def test_defaultView(self):
        
        # prepare test
        app, session_startup = start_app_for_testing()

        # asserts
        self.assertEqual(session_startup.chooseVisStyle.currentText(), "Spike Finding")
        self.assertEqual(session_startup.chooseSpikeThreshold.value(), 400) # value * 100 TODO fix
        #self.assertEqual(session_startup)
"""

class TestData(unittest.TestCase):

    # TODO test that data has 1024 rows

    # TODO test that each data column is in the right type

    # TODO sanity check that each data column is within a reasonable range

    """ examples
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    """
    pass
