''' Script for testing speed of the audio stream'''
import pyaudio as pa
import numpy as np
from signal_process import mic_connect, stream_audio, mic_close
import time


def stream_speed() :
    fmax = 500.0                   # Highest frequency we are looking for in Hz
    n = 20                         # Number of chunks per second
    RATE = int((5*fmax))           # Audio sampling rate
    print(1/n)
    CHUNK = int(RATE / n)          # Number of samples per update
    p = pa.PyAudio()
    stream = p.open(format=pa.paInt16,
                    channels=1,
                    rate=int(RATE),
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback
                    )
    stream.start_stream()
    return p, stream


def callback(in_data, frame_count, time_info, flag):
    t1 = time.time()
    print(flag)
    data = np.fromstring(in_data, dtype=np.float64)
    print(time.time() - t1)
    return None, pa.paContinue

def stop_stream(pyaudio_connection, stream) :
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__=="__main__" :
    stream_speed()
