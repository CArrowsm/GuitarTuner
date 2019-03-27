import pyaudio
import numpy as np
import time
from scipy.signal import find_peaks

def callback(in_data, frame_count, time_info, flag):
    global mic_data
    t1 = time.time()
    mic_data = np.fromstring(in_data, dtype=np.float64)
    print(time.time() - t1)
    return None, pa.paContinue

# Function to set up mic connection and return
def mic_connect():
    global fmax
    fmax = 500.0                   # Highest frequency we are looking for in Hz
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


def stream_audio(audio_connection, stream, CHUNK):
    data = np.fromstring(stream.read(CHUNK, exception_on_overflow=False),dtype=np.int16)
    print(stream.get_input_latency())
    return data

def mic_close(audio_connection, stream):
    stream.stop_stream()
    stream.close()
    audio_connection.terminate()


# Function takes array of times and array of y values and outputs f, W
def spectrum(y, sampling_rate, N):
    Y = np.abs(np.fft.fft(y))/np.sqrt(N)
    f = np.fft.fftfreq(N,1/sampling_rate)

    return f[ : int(N/2)], Y[ : int(N/2)]


# Return location of peak with lowest x-value
def peak_detect(x, y) :
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
