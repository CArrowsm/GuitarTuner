''' Script for testing speed of the audio stream'''
import pyaudio as pa
import numpy as np
import time
import signal_process




def stream_speed() :
    stream = signal_process.open_stream(callback_speed)


def callback_speed():
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
