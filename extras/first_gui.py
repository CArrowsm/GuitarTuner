import sys
from PyQt5.QtWidgets import (QLabel, QMainWindow, QApplication, QPushButton,
                             QWidget, QAction, QTabWidget,QHBoxLayout,
                             QStackedWidget, QVBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal

import time
import numpy as np
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5

from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


# Create main app class
class App(QStackedWidget):
    """docstring for App."""
    def __init__(self):
        super(App, self).__init__()

        self.initUI()

        self.show()
        sys.exit(app.exec_())

    # Build basic user interface
    def initUI(self) :
        self.setWindowTitle("Guitar Tuner")
        self.setGeometry(500, 100, 900, 600)
        self.setStyleSheet(open('style.css').read())
        self.window = QMainWindow()

        # Add custom tab header widget to window
        self.graph_tab = GraphWidget(self.window)
        self.tuner_tab = TunerWidget(self.window)
        self.addWidget(self.graph_tab)
        self.addWidget(self.tuner_tab)

        self.setCurrentWidget(self.tuner_tab)

        # Add menu button functionality
        self.tuner_tab.tunerButton.clicked.connect(lambda: self.setCurrentWidget(self.tuner_tab))
        self.tuner_tab.graphButton.clicked.connect(lambda: self.setCurrentWidget(self.graph_tab))
        self.graph_tab.tunerButton.clicked.connect(lambda: self.setCurrentWidget(self.tuner_tab))
        self.graph_tab.graphButton.clicked.connect(lambda: self.setCurrentWidget(self.graph_tab))

# Widget for interactive tuning
class TunerWidget(QWidget):
    """Page which displays interavtive tuning features"""
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.styleSheet = open('style.css').read()

        ### Add menu bar to widget ###
        self.hlayout = QHBoxLayout()
        self.vlayout = QVBoxLayout(self)

        ## Make buttons ##
        # Tuner tab
        self.tunerButton = QPushButton("Tune", self)
        self.tunerButton.setToolTip("Interactive Guitar Tuner")
        self.tunerButton.setObjectName("header")
        self.hlayout.addWidget(self.tunerButton)

        # Graphing tab
        self.graphButton = QPushButton("Plots", self)
        self.graphButton.setToolTip("Live Waveform Plotting")
        self.graphButton.setObjectName("header")
        self.hlayout.addWidget(self.graphButton)

        # Make buttons appear at the top
        self.vlayout.addLayout(self.hlayout)
        self.vlayout.addStretch(1)
        ### End menu bar ###

        # Add tuning label (says which tuning we're listening for)
        self.tuning_label = QLabel("Standard", self)
        self.tuning_label.setObjectName("tuning")
        self.tuning_label.setGeometry(10, 30, 200, 100)


# Widget for interactive tuning
class GraphWidget(QWidget):
    """Page which displays interavtive tuning features"""
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.styleSheet = open('style.css').read()

        ### Add menu bar to widget ###
        self.hlayout = QHBoxLayout()
        self.vlayout = QVBoxLayout(self)

        ## Make buttons ##
        # Tuner tab
        self.tunerButton = QPushButton("Tune", self)
        self.tunerButton.setToolTip("Interactive Guitar Tuner")
        self.tunerButton.setObjectName("header")
        self.hlayout.addWidget(self.tunerButton)

        # Graphing tab
        self.graphButton = QPushButton("Plots", self)
        self.graphButton.setToolTip("Live Waveform Plotting")
        self.graphButton.setObjectName("header")
        self.hlayout.addWidget(self.graphButton)

        # Make buttons appear at the top
        self.vlayout.addLayout(self.hlayout)
        ### End menu bar ###

        # Add tuning label (says which tuning we're listening for)
        self.tuning_label = QLabel("Standard2", self)
        self.tuning_label.setObjectName("tuning")
        self.tuning_label.setGeometry(10, 30, 200, 100)

        ### Live Audio Plots ###
        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.vlayout.addWidget(dynamic_canvas)

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._timer = dynamic_canvas.new_timer(
            100, [(self._update_canvas, (), {})])
        self._timer.start()

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()
        ### End of Audio Plots ###


if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ex = App()
