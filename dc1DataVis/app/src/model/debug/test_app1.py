import sys
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

class MyApp(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.central_layout = QtGui.QVBoxLayout()
        self.plot_boxes_layout = QtGui.QHBoxLayout()
        self.boxes_layout = QtGui.QVBoxLayout()
        self.setLayout(self.central_layout)

        # Lets create some widgets inside
        self.label = QtGui.QLabel('Plots and Checkbox below:')

        # Here is the plot widget from pyqtgraph
        self.plot_widget = pg.PlotWidget()

        # Now the Check Boxes (lets make 3 of them)
        self.num = 6
        self.check_boxes = [QtGui.QCheckBox(f"Box {i + 1}") for i in range(self.num)]

        # Here will be the model of the plot
        self.plot_data = [None for _ in range(self.num)]

        # Now we build the entire GUI
        self.central_layout.addWidget(self.label)
        self.central_layout.addLayout(self.plot_boxes_layout)
        self.plot_boxes_layout.addWidget(self.plot_widget)
        self.plot_boxes_layout.addLayout(self.boxes_layout)
        for i in range(self.num):
            self.boxes_layout.addWidget(self.check_boxes[i])
            # This will conect each box to the same action
            self.check_boxes[i].stateChanged.connect(self.box_changed)

        # For optimization let's create a list with the states of the boxes
        self.state = [False for _ in range(self.num)]

        # Make a list to save the model of each box
        self.box_data = [[[0], [0]] for _ in range(self.num)]
        x = np.linspace(0, 3.14, 100)
        self.add_data(x, np.sin(x), 0)
        self.add_data(x, np.cos(x), 1)
        self.add_data(x, np.sin(x) + np.cos(x), 2)
        self.add_data(x, np.sin(x) ** 2, 3)
        self.add_data(x, np.cos(x) ** 2, 4)
        self.add_data(x, x * 0.2, 5)

    def add_data(self, x, y, ind):
        self.box_data[ind] = [x, y]
        if self.plot_data[ind] is not None:
            self.plot_data[ind].setData(x, y)

    def box_changed(self):
        for i in range(self.num):
            if self.check_boxes[i].isChecked() != self.state[i]:
                self.state[i] = self.check_boxes[i].isChecked()
                if self.state[i]:
                    if self.plot_data[i] is not None:
                        self.plot_widget.addItem(self.plot_data[i])
                    else:
                        self.plot_data[i] = self.plot_widget.plot(*self.box_data[i])
                else:
                    self.plot_widget.removeItem(self.plot_data[i])
                break


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())