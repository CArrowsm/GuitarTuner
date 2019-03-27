import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
import time


# Function to set up mic connection and return
def mic_connect():
    n = 20                # Number of updates per second
    RATE = 44100
    CHUNK = int(RATE / n) # RATE / number of updates per second
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
    return data


# Plot function which will be called recursively
def soundplot(data):
    t1=time.time()
    # pylab.clf()

    # Make figure for timeseries and FFT
    fig, ax =
    pylab.plot(data)
    # pylab.title(i)
    pylab.grid()
    # pylab.axis([0,len(data),-2**16/2,2**16/2])
    pylab.show()
    # time.sleep(5.5)
    print("took %.02f ms"%((time.time() - t1) * 1000))

if __name__== "__main__" :
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                  frames_per_buffer=CHUNK)

    # pylab.ion()
    # for i in range(int(20*RATE/CHUNK)): #do this for 10 seconds
    soundplot(stream)
    pylab.ioff()
    stream.stop_stream()
    stream.close()
    p.terminate()
