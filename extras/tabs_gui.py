import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random

# Create main app class
class App(QMainWindow):
    """docstring for App."""
    def __init__(self):
        super().__init__()
        self.left = 0
        self.top = 0
        self.title = 'PyQt5 matplotlib'
        self.width = 900
        self.height = 680
        self.initUI()

    # Build basic user interface
    def initUI(self) :
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet(open('style.css').read())

        # Add custom tab widget to window
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        # Show entire app
        self.show()


# Create table widget to store tabs
class MyTableWidget(QWidget) :
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(10,5)
        self.tabs.setStyleSheet(open('style.css').read())

        # Build tabs
        self.build_tab1(self.tabs, self.tab1)
        self.build_tab2(self.tabs, self.tab2)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    # Build first tab
    def build_tab1(self, tabs, tab) :
        tabs.addTab(tab, "Tuner")
        tab.layout = QVBoxLayout(self)
        self.button1 = QPushButton("PyQt5 button", self)
        self.button1.setToolTip("This is an example button")
        self.button1.setGeometry(25, 20, 250,40)
        self.button1.setObjectName("button1")
        tab.layout.addWidget(self.button1)
        self.button1.setStyleSheet(open('style.css').read())
        tab.setLayout(self.tab1.layout)

    # Build second tab
    def build_tab2(self, tabs, tab) :
        tabs.addTab(tab, "Plot")
        tab.layout = QVBoxLayout(self)
        # m = PlotCanvas(self, width=5, height=4)
        #
        # class PlotCanvas(FigureCanvas):
        #
        #     def __init__(self, parent=None, width=5, height=4, dpi=100):
        #         fig = Figure(figsize=(width, height), dpi=dpi)
        #         self.axes = fig.add_subplot(111)
        #
        #         FigureCanvas.__init__(self, fig)
        #         self.setParent(parent)
        #
        #         FigureCanvas.setSizePolicy(self,
        #                 QSizePolicy.Expanding,
        #                 QSizePolicy.Expanding)
        #         FigureCanvas.updateGeometry(self)
        #         self.plot()
        #
        #
        #     def plot(self):
        #         data = [random.random() for i in range(25)]
        #         ax = self.figure.add_subplot(111)
        #         ax.plot(data, 'r-')
        #         ax.set_title('PyQt Matplotlib Example')
        #         self.draw()


    # @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())




if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
