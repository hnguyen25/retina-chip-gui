"""
NoisePlot
--------------

@authors Huy Nguyen
"""
from PyqtGraphParams import * # parent class

class NoisePlot(PyqtGraphParams):

    def __init__(self, param_dict : dict):
        super().__init__(self, param_dict)

    def update_graph(self): #overloaded
        pass