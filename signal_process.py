import pyaudio as pa
import numpy as np
import time
from scipy.signal import find_peaks

############
global fmin, fmax, hanning
fmin = 70.0                    # Lowest frequency we are looking for in Hz
fmax = 1500.0                   # Highest frequency we are looking for in Hz
############

# Create PyAudio connection to mic and open stream (but dont start streaming)
def open_stream(callback) :
    fmax = 500.0                   # Highest frequency we are looking for in Hz
    n = 8                          # Number of chunks per second (must be integer multiple of GUI refresh rate)
    # RATE = int((10*fmax))        # Audio sampling rate
    RATE = 44100.0
    CHUNK = int(RATE / n)          # Number of samples per chunk
    p = pa.PyAudio()
    print(p.get_default_input_device_info())
    stream = p.open(format=pa.paInt16,
                    channels=1,
                    rate=int(RATE),
                    input=True,
                    start=False,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback
                    )
    return p, stream, n, CHUNK, RATE

def start_stream(stream):
        stream.start_stream()

'''
# Function to set up mic connection and return
def mic_connect():
    n = 20                         # Number of chunks per second
    RATE = int((5*fmax))           # Audio sampling rate
    CHUNK = int(RATE / n) # Number of samples per update
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=int(RATE),
                    input=True,    # Indicates we are getting mic's output
                    start=True,    # Stream starts running immediately
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)
    return p, stream, n, CHUNK, RATE
'''


def stream_audio(audio_connection, stream, CHUNK):
    data = np.fromstring(stream.read(CHUNK, exception_on_overflow=False),dtype=np.int16)
    print(stream.get_input_latency())
    return data

def mic_close(audio_connection, stream):
    stream.stop_stream()
    stream.close()
    audio_connection.terminate()


# Function takes array of times and array of y values and outputs f, W
def spectrum(y, sampling_rate):
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


# Return location of peak with lowest x-value
def peak_detect(x, y) :
    x, y = x[fmin < x], y[fmin < x]
    cutoff = max(y) * (1/3)
    peaks, _ = find_peaks(y, height=cutoff, distance=None)

    try :
        return x[min(peaks)]
    except ValueError :
        return None

def test() :
    p, stream, n, CHUNK, RATE = mic_connect()
    pass

if __name__== "__main__" :
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                  frames_per_buffer=CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()
