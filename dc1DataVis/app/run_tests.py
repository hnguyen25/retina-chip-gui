import unittest

# not necessary, but a nice reference
from dc1DataVis.app.src.model.unit_tests.test_data import *
from dc1DataVis.app.src.model.unit_tests.test_interactivity import *
from dc1DataVis.app.src.model.unit_tests.test_performance import *
from dc1DataVis.app.src.model.unit_tests.test_modes import *
from dc1DataVis.app.src.model.unit_tests.test_windows import *

if __name__ == '__main__':
    testsuite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=1).run(testsuite)
