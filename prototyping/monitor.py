# Print out realtime audio volume as ascii bars

import sounddevice as sd
import numpy as np

duration = 10  # seconds

def print_sound(indata):
    volume_norm = np.linalg.norm(indata)*10
    print("|" * int(volume_norm))


def callback(indata, frames, time, status):
    if status:
        print(status)
    print_sound(indata)


with sd.InputStream(channels=2, callback=callback, latency='low'):
    sd.sleep(int(duration * 1000))
