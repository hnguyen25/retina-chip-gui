"""
array specific data
such as noise statistics
spiking statistics

"""
import numpy as np


NUM_ROWS, NUM_COLS = 32, 32

class ArrayStatsContainer:

    data = np.zeros((NUM_ROWS, NUM_COLS,))
    def __init__(self):
        pass

    def update(self, data):
        pass