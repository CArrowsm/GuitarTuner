import pyaudio as pa
import numpy as np
import time
from scipy.signal import find_peaks

import threading

import sys
from PyQt5.QtWidgets import (QLabel, QMainWindow, QApplication, QPushButton,
                             QWidget, QAction, QHBoxLayout, QComboBox,
                             QStackedWidget, QVBoxLayout, QGridLayout)
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QPainterPath
from PyQt5.QtCore import ( pyqtSlot, pyqtSignal, QTimer,QThread, QObject,
                           QPointF, QPropertyAnimation, pyqtProperty )
import time
from pyqtgraph.Qt import QtCore
import pyqtgraph as pg
import pandas as pd
pg.setConfigOption('background', (249,249,249))
pg.setConfigOption('foreground', 'k')

import matplotlib.pyplot as plt

class AudioStream() :
    """Sets up the mic connection and passes data to widgets."""
    def __init__(self):
        # super(object, self).__init__(parent)


        (self.connection, self.stream,
        self.n, self.chunk, self.samp_rate) = self.open_stream(self.callback)

        self.time = time.time()

        self.lock = threading.Lock()

        self.latencies = []


        # self.start_stream(self.stream)


    def open_stream(self, callback) :
        fmax = 500.0                   # Highest frequency we are looking for in Hz
        n = 60                          # Number of chunks per second (must be integer multiple of GUI refresh rate)
        # RATE = int((10*fmax))        # Audio sampling rate
        RATE = 44100
        CHUNK = int(RATE / n)          # Number of samples per chunk
        p = pa.PyAudio()
        print(p.get_default_input_device_info())
        stream = p.open(format=pa.paInt16,
                        channels=1,
                        rate=int(RATE),
                        input=True,
                        output=False,
                        start=False,
                        frames_per_buffer=int(44100/100),
                        stream_callback=callback
                        )
        return p, stream, n, CHUNK, RATE


    def start_stream(self, stream):
            stream.start_stream()


    # define callback (2)
    def callback(self, in_data, frame_count, time_info, status):
        data = np.frombuffer(in_data, dtype=np.int16)
        if status:
            print("Playback Error: %i" % status)
        with self.lock :
            t = time.time()
            # print(t - self.time)
            self.latencies.append(t - self.time)
            self.time = t
            # print(len(data))
        return (data.tobytes(), pa.paContinue)

    def stream_audio(self, audio_connection, stream, CHUNK):
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False),dtype=np.int16)
        print(stream.get_input_latency())
        return data, pa.paContinue

    def mic_close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.connection.terminate()


    # Function takes array of times and array of y values and outputs f, W
    def spectrum(self, y, sampling_rate):
        # time1 = time.time()
        N, dt = len(y), 1.0/sampling_rate

        # Apply Hanning window
        n = np.arange(0, N, 1)
        w = 1 - np.cos(2*np.pi*n/N)
        y = y * w

        Y = np.absolute(np.fft.fft( y/max(y) ))
        f = np.fft.fftfreq(N, dt)

        # Restrict f range
        f, Y = f[(0 < f) & (f < fmax)], Y[(0 < f) & (f < fmax)]
        # print(time.time() - time1)
        return f, Y

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

    def initUI(self) :
        # Initialize GUI
        self.setWindowTitle("Guitar Tuner")
        self.setGeometry(500, 100, 900, 600)
        self.setStyleSheet(open('style.css').read())
        self.window = QMainWindow()

        # Add custom tab header widget to window
        self.graph_tab = GraphWidget(self.window)
        self.addWidget(self.graph_tab)

        # self.setCurrentWidget(self.tuner_tab)

    def close_app(self) :
        self.s.mic_close(self.s.connection, self.s.stream)
        print("CLOSING APP")

class GraphWidget(QWidget):
    """Page which displays interavtive tuning features"""
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.styleSheet = open('style.css').read()

        self.vlayout = QVBoxLayout(self)

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
    # main()
    s = AudioStream()
    s.start_stream(s.stream)

    time.sleep(10)
    s.mic_close()

    t = np.linspace(0, 5, len(s.latencies))
    plt.figure()
    plt.xlabel("Iteration")
    plt.ylabel("Time [s]")
    plt.plot(t, s.latencies)
    plt.show()
