"""
ElectrodeMinimap
--------------

@authors Huy Nguyen
"""
from PyqtGraphParams import * # parent class

class ElectrodeMinimap(PyqtGraphParams):

    def __init__(self, param_dict : dict):
        super().__init__(self, param_dict)

    def update_graph(self): #overloaded
        pass