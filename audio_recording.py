#!/usr/bin/env python3
"""Create a recording with arbitrary duration.

The soundfile module (https://python-soundfile.readthedocs.io/)
has to be installed!

"""
import tempfile
import queue
import sys

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback

assert numpy  # avoid "imported but unused" message (W0611)

q = queue.Queue()


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())


channels = [1]  # input channels to plot -> int
device = None# input device (numeric ID or substring) -> int_or_str
window = 200  # visible time slot, default=200 ms  -> float
interval = 30  # minimum time between plot updates  -> float
blocksize = 1024  # block size (in samples)
samplerate = None  # sampling rate of audio device  -> float
downsample = 10  # display every Nth sample, default=10  -> int
filename = 'audio.wav'  # audio file to store recording to  -> str
subtype = "PCM_24"  # sound file subtype (e.g. "PCM_24") -> str

mapping = [c - 1 for c in channels]

try:
    if samplerate is None:
        device_info = sd.query_devices(device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        samplerate = int(device_info['default_samplerate'])
    # Make sure the file is opened before recording anything:
    with sf.SoundFile(filename, mode='x', samplerate=samplerate,
                      channels=max(channels), subtype=subtype) as file:
        with sd.InputStream(samplerate=samplerate, device=device,
                            channels=max(channels), callback=callback):
            print('#' * 80)
            print('press esc or close signal window to stop the recording')
            print('#' * 80)
            while True:
                file.write(q.get())
except KeyboardInterrupt:
    print('\nRecording finished: ' + repr(filename))
except Exception as e:
    print(e)
