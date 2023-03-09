#!/usr/bin/env python3
"""
Create a recording with arbitrary duration.
The soundfile module (https://python-soundfile.readthedocs.io/)
has to be installed!
"""

import queue
import sys

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback

assert numpy  # avoid "imported but unused" message (W0611)


class Recorder:
    def __init__(self) -> None:
        self.q = queue.Queue()
        self.channels = [1]  # input channels to plot -> int
        # input device (numeric ID or substring) -> int_or_str
        self.device = None
        self.window = 200  # visible time slot, default=200 ms  -> float
        self.interval = 30  # minimum time between plot updates  -> float
        self.blocksize = 1024  # block size (in samples)
        self.samplerate = None  # sampling rate of audio device  -> float
        self.downsample = 10  # display every Nth sample, default=10  -> int
        self.filename = 'audio.wav'  # audio file to store recording to  -> str
        self.subtype = "PCM_16"  # sound file subtype (e.g. "PCM_24") -> str
        self.mapping = [c - 1 for c in self.channels]

    def callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())

    def record(self):
        try:
            if self.samplerate is None:
                device_info = sd.query_devices(self.device, 'input')
                # soundfile expects an int, sounddevice provides a float:
                samplerate = int(device_info['default_samplerate'])
            # Make sure the file is opened before recording anything:
            with sf.SoundFile(self.filename, mode='x', samplerate=samplerate,
                              channels=max(self.channels), subtype=self.subtype) as file:
                with sd.InputStream(samplerate=samplerate, device=self.device,
                                    channels=max(self.channels), callback=self.callback):
                    print('#' * 80)
                    print('press esc or close signal window to stop the recording')
                    print('#' * 80)
                    while True:
                        file.write(self.q.get())
        except KeyboardInterrupt:
            print('\nRecording finished: ' + repr(self.filename))
        except Exception as e:
            print(e)
