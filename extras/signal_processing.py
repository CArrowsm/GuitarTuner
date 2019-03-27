from matplotlib.pyplot import *
from matplotlib.animation import FuncAnimation
import numpy as np
import sounddevice as sd


arguments = {"list-devices": False, 		# True or False
			 "input-device": 'default', 	# numeric ID or substring
			 "channels": [0],					# Indeces of audio input channels to plot (default: the first)
			 "window-size": 200,			# Amout of data visible in timeseries plot (ms)
			 "plot-interval": 30,			# Time between plot updates (ms)
			 "bock-duration": 50,			# Length of block in ms
			 "samplerate": 44100,			# How often to sample audio (44100 is default)
			 "gain": 10.,					# Audio input gain (10 default)
			 "f-range": [100, 2000] 		# Frequency range (Hz)
}

device_info = sd.query_devices(arguments['device'], 'input')
arguments['samplerate'] = device_info['default_samplerate']


def callback(indata, frames, time, status) :
	if status :
		print(status)
	queue.put(indata[:, channels])


def update_plot(frame) :
	global plotdata
	try :
		data = queue
	except Empty :
		return np.array([])
	plotdata = data
	return plotdata



length = np.ceil()

stream = sd.InputStream(channels=1, dtype='float64', callback=callback,
						device=arguments['device'], 
						samplerate=arguments['default_samplerate'])
with stream :
