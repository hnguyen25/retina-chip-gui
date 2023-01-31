"""
This is a separate data container to DC1DataContainer that just holds the trace data information processed.

> interfaces with npz to do saving
> interfaces with DC1datacontainer to save trace data
> interfaces in realtime with a temp folder to save only useful info
> saves temp file to disk
> a save prompt to save folder
> clear on exit
"""
import numpy as np
import time
from src.model.data_loading_mat import *
from ..model.filters import *
import warnings
import queue
import pandas as pd

class TracesDataContainer:


    def __init__(self, app):
        pass