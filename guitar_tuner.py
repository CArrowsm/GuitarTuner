################################################################
import sys
from PyQt5.QtWidgets import (QLabel, QMainWindow, QApplication, QPushButton,
                             QWidget, QAction, QHBoxLayout, QComboBox,
                             QStackedWidget, QVBoxLayout, QGridLayout)
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QPainterPath
from PyQt5.QtCore import ( pyqtSlot, pyqtSignal, QTimer,QThread, QObject,
                           QPointF, QPropertyAnimation, pyqtProperty )
import time
import numpy as np
from pyqtgraph.Qt import QtCore
import pyqtgraph as pg
import pandas as pd
pg.setConfigOption('background', (249,249,249))
pg.setConfigOption('foreground', 'k')
import signal_process as sp
import pyaudio as pa
################################################################


# Audio stream
class AudioStream(QThread):
    """Sets up the mic connection and passes data to widgets."""
    def __init__(self, parent):
        super(QThread, self).__init__(parent)

        # Initialize the audio connection
        self.data_arr = np.array([])
        (self.connection, self.stream,
        self.n, self.chunk, self.samp_rate) = sp.open_stream(self.process_stream)
        print("Connection: ", self.connection)
        print("Stream: ", self.stream)
        print("Chunks per second: ", self.n)
        print("Samples per Chunk: ", self.chunk)
        print("Sample Rate: ", self.samp_rate)

        ### Edit this Value ###
        self.ref_rate = 2                                      # GUI refresh rate (s^-1)
        ### --------------- ###

        # Don't touch this
        self.count, self.limit = 0, int(self.n / self.ref_rate)# Number of chunks per GUI refresh
        # self.N = self.limit * self.chunk
        parent.graph_tab.create_canvas([self.limit, self.chunk, self.n])

        # Begin stream
        self.stream.start_stream()
        print('Stream Started')


    def process_stream(self, in_data, frame_count, time_info, flag) :
        if flag:
            print("Playback Error: ", flag)

        raw = np.fromstring(in_data, dtype=np.int16)
        parent = self.parent()

        # If we have not reached right number of chunks, add another
        if self.count < (self.limit - 1) :
            self.data_arr = np.concatenate((self.data_arr, raw), axis=None)

        # If we've reached last chunk, add last and process them
        elif self.count == (self.limit - 1) :
            self.data_arr = np.concatenate((self.data_arr, raw), axis=None)

            # Process Data and send to GUI:
            freqs, fft = sp.spectrum(self.data_arr, self.samp_rate)
            if parent.currentWidget() == parent.graph_tab :
                parent.graph_tab.update_canvas(self.data_arr, freqs, fft)

            elif parent.tuner_tab.listen_note :
                peak = sp.peak_detect(freqs, fft)
                parent.tuner_tab.update_display(peak)

            # Reset Array
            self.data_arr = np.array([])

            # Reset counter
            self.count = -1

        self.count = self.count + 1

        return None, pa.paContinue


    # Start streaming
    def start_stream(self, stream):
        stream.start_stream()



class App(QStackedWidget):
    """main application class."""
    def __init__(self):
        super(App, self).__init__()
        self.initUI()

        self.show()

        # Initialize audio stream class
        self.s = AudioStream(self)

        try:
            sys.exit(app.exec_())
        except:
            self.close_app()

    # Build basic user interface
    def initUI(self) :
        # Initialize GUI
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

    def close_app(self) :
        sp.mic_close(self.s.connection, self.s.stream)
        print("CLOSING APP")

class AnimationIcon(QLabel):
    """Icon which will move on interactive tuning page."""
    def __init__(self, parent):
        super().__init__(parent)
        pix = QPixmap("icons/down_arrow.png")
        self.h = pix.height()
        self.w = pix.width()
        self.setPixmap(pix)

    def _set_pos(self, pos):
        self.move(pos.x() - self.w/2, pos.y() - self.h/2)

    pos = pyqtProperty(QPointF, fset=_set_pos)



class TunerWidget(QWidget):
    """Page which displays interactive tuning features"""
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
        self.vlayout.addStretch(0.5)
        ### End menu bar ###

        # Add tuning dropdown (says which tuning we're listening for)
        self.tuning = "Standard"
        self.listen_note = None
        tuning_dropdown = QComboBox(self)
        tuning_dropdown.setObjectName("tuning")
        tuning_dropdown.setGeometry(30, 50, 225, 100)
        self.names = pd.read_csv("names.csv", index_col="tuning")
        for i in self.names.index.values :
            tuning_dropdown.addItem(i)
        # Change Bottom buttons if dropdown selected
        tuning_dropdown.activated[str].connect(self.set_tuning)

        # Create Graphic and button for each note
        self.create_graphic()
        self.vlayout.addStretch(0.3)
        self.create_buttons()

    def create_graphic(self) :
        # Make moveable icon
        self.tune_icon = QLabel("Hi")
        self.tune_icon.setObjectName('tune_icon')
        ani_box = QHBoxLayout(self)
        ani_box.addStretch(1)
        ani_box.addWidget(self.tune_icon)
        ani_box.addStretch(1)
        # self.tune_icon.pos = pyqtProperty(QPointF, fset=self.update_display)
        self.vlayout.addLayout(ani_box)
        # self.tune_icon.pos = QPointF(0, 0)
        # self.tune_icon.path = QPainterPath()
        # self.tl = QtCore.QTimeLine(1000)
        # self.tl.setFrameRange(0, 100)
        # self.a = QPropertyAnimation()
        # self.a.setItem(self.tune_icon)
        # self.a.setTimeLine(self.tl)

        # Make grid bar (which is stationary)
        bar = QHBoxLayout(self)
        bar.setSpacing(0)
        self.vlayout.addLayout(bar)
        bar.addStretch(0.5)
        bar.addWidget(QLabel("Too Flat   "))
        for i in range(0, 8) :
            section = QPushButton("")
            section.setObjectName("bar")
            bar.addWidget(section)
        bar.addWidget(QLabel("   Too Sharp"))
        bar.addStretch(0.5)

        # Make Text saying if we're in tune
        self.text = QLabel("Choose a Note and Pluck the String", self)
        self.text.setGeometry(100, 200, 500, 400)
        hgrid = QGridLayout(self)
        hgrid.addWidget(QLabel("", self), 0, 0)
        hgrid.addWidget(self.text, 0, 1, 1, 3)
        hgrid.addWidget(QLabel("", self), 0, 2)
        self.vlayout.addLayout(hgrid)

    def create_buttons(self) :
        try :
            layout = self.tune_buttons
            for i in range(layout.count()):
                layout.itemAt(i).widget().deleteLater()
        except AttributeError :
            pass
        finally :
            self.notes = pd.read_csv("names.csv", index_col="tuning").loc[self.tuning,:].values
            self.freqs = pd.read_csv("frequencies.csv",
                                     index_col="tuning").loc[self.tuning,:].values
            self.tune_buttons = QGridLayout(self)
            self.tune_buttons.setSpacing(0)
            self.vlayout.addLayout(self.tune_buttons)
            for i in range(len(self.notes)) :
                button = QPushButton(self.notes[i])
                button.setObjectName("note-button")
                button.clicked.connect(self.set_note)
                self.tune_buttons.addWidget(button, 0.5, i)

    def set_tuning(self, text) :
        self.tuning = text
        self.listen_note = None
        self.listen_freq = None
        self.text.setText("Choose a Note and Pluck the String")
        self.create_buttons()

    def set_note(self) :
        button = self.sender()
        self.listen_note = button.text()
        self.listen_freq = self.freqs[self.tune_buttons.indexOf(button)]


    def update_display(self, peak):
        string = "Listening For "+str(self.listen_note)+" ("\
                  + str(self.listen_freq)[0:5]+") Hz\n"     \
                  + "Current Note: " + str(peak)[0:5] + " Hz"
        self.text.setText(string)

        # Animation
        # self.a.setPosAt(0, QtCore.QPointF(0, -10))
        # self.a.setRotationAt(1, 360)
        # self.tl.start()

        # self.tune_icon.path.moveTo(50, 200)
        # self.anim = QPropertyAnimation(self.tune_icon, b'pos')
        # self.anim.setDuration(100)
        # self.anim.setStartValue(QPointF(0, 30))
        #
        # vals = [p/100 for p in range(0, 101)]
        #
        # for i in vals:
        #     self.anim.setKeyValueAt(i, self.tune_icon.path.pointAtPercent(i))
        # self.anim.setEndValue(QPointF(0, 3))
        # self.anim.start()
        print('animating')


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
        self.title = QLabel("Audio Input Graphs", self)
        self.title.setObjectName("tuning")
        self.title.setGeometry(10, 30, 200, 100)
        self.vlayout.addWidget(self.title)

        ### Live Audio Plots ###
        self.win = pg.GraphicsWindow()
        self.vlayout.addWidget(self.win)

    def create_canvas(self, stream_params) :
        tmin = 0
        tmax = stream_params[0] * (1/stream_params[2])
        dt = 1/(stream_params[1]*stream_params[2])
        self.t_ax = self.win.addPlot(row=0, col=0,
                    labels={'left': "PCM", 'bottom': "Time [s]"})
        self.f_ax = self.win.addPlot(row=1, col=0,
                    labels={'left': "Amplitude", 'bottom': "Frequency [Hz]"})
        self.t_plot = self.t_ax.plot()
        self.f_plot = self.f_ax.plot()
        self.t_plot.setPen("k")
        self.f_plot.setPen("k")
        self.t_ax.setXRange(tmin, tmax)
        self.t_ax.setYRange(-5000.0, 5000.0)
        self.f_ax.setYRange(0, 100.0)
        self.tdata = np.arange(tmin, tmax, dt)

    def update_canvas(self, data, freqs, fft):
        self.t_plot.setData(y=data[:len(self.tdata)], x=self.tdata)
        self.f_plot.setData(x=freqs, y=fft)
        app.processEvents()   # Forces total re-draw
        ### End of Audio Plots ###

def main() :
    global app, ex
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icons/guitar_icon.png"))
    # app.setWindowTitle("Guitar Tuner")
    ex = App()

if __name__ == '__main__' :
    main()
