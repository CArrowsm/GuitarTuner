import matplotlib.pyplot as plt
import struct
import numpy as np
import pyaudio as pa
import time
import sounddevice as sd
from multiprocessing import Process

'''
p = pa.PyAudio()

FORMAT = pa.paInt8
CHANNELS = 1
CHUNK = int( 44100/50)
RATE = 44100

# global t0
# t0 = time.time()


def f(in_data, frame_count, time_info, flag) :

    # print(flag, time_info)
    print(frame_count)

    data  = in_data

    # print(time.time() - t0)
    # t0 = time.time()
    return (data, pa.paContinue)


stream = pa.Stream(p,
                format=FORMAT,
                channels=CHANNELS,
                frames_per_buffer=CHUNK,
                input=True,
                output=True,
                rate=RATE,
                stream_callback=f,
                )
stream.start_stream()

time.sleep(10)

stream.stop_stream()
stream.close()

# close PyAudio (7)
p.terminate()
'''

'''
# from pysoundio import PySoundIo, SoundIoFormatFloat32LE
import pysoundio as ps

class Record(object) :
    def __init__(self, backend=None, input_device=None,
                 sample_rate=44100, blocksize=4096,
                 channels=1) :
        self.t0 = time.time()

        self.pysoundio = ps.PySoundIo(backend=backend)

        print(self.pysoundio.backend_count)

        self.pysoundio.start_input_stream(
            device_id=input_device,
            channels=channels,
            sample_rate=sample_rate,
            block_size=blocksize,
            dtype=ps.SoundIoFormatFloat32LE,
            read_callback=self.callback,
            overflow_callback=self.over_callback
        )


    def close(self) :
        self.pysoundio.close()

    def callback(self, data, length) :
        print(time.time() - self.t0)
        self.t0 = time.time()
        self.pysoundio.flush()

    def over_callback() :
        print("buffer overflow")




record = Record(sample_rate=None, blocksize=None,
                backend=None)


try :

    while True :
        time.sleep(5)


except KeyboardInterrupt:
    print("\nClosing")


record.close()

'''


import argparse
import queue
import sys

q = queue.Queue()

def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata)
    # print(len(q))




# from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd


# List devices
print(sd.query_devices())


# Get ideal sample rate
device_info = sd.query_devices(0, 'input')
samplerate = device_info['default_samplerate']
print(samplerate)

stream = sd.InputStream(
        device=0, channels=1,
        samplerate=44100, callback=audio_callback)

with stream:
    print("Starting Stream")
