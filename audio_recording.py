#!/usr/bin/env python3
"""
Create a recording with arbitrary duration.
The soundfile module (https://python-soundfile.readthedocs.io/)
has to be installed!
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import queue
import sys

import sounddevice as sd
import soundfile as sf
import numpy as np


class Recorder:
    def __init__(self) -> None:
        self.q_rec = queue.Queue()
        self.q_plot = queue.Queue()
        self.channels = [1]  # input channels to plot -> int
        self.device = None  # input device (numeric ID or substring) -> int_or_str
        self.window = 200  # visible time slot, default=200 ms  -> float
        self.interval = 30  # minimum time between plot updates  -> float
        self.blocksize = 1024  # block size (in samples)
        self.samplerate = None  # sampling rate of audio device  -> float
        self.downsample = 10  # display every Nth sample, default=10  -> int
        self.filename = 'audio.wav'  # audio file to store recording to  -> str
        self.subtype = "PCM_16"  # sound file subtype (e.g. "PCM_24") -> str
        self.mapping = [c - 1 for c in self.channels]
        self.plotdata = None
        self.lines = None

    def callback_rec(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.q_rec.put(indata.copy())

    def callback_plot(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        # Fancy indexing with mapping creates a (necessary!) copy:
        self.q_plot.put(indata[::self.downsample, self.mapping])

    def record(self):
        try:
            if self.samplerate is None:
                device_info = sd.query_devices(self.device, 'input')
                # soundfile expects an int, sounddevice provides a float:
                self.samplerate = int(device_info['default_samplerate'])
            # Make sure the file is opened before recording anything:
            with sf.SoundFile(self.filename, mode='x', samplerate=self.samplerate,
                              channels=max(self.channels), subtype=self.subtype) as file:
                with sd.InputStream(samplerate=self.samplerate, device=self.device,
                                    channels=max(self.channels), callback=self.callback_rec):
                    print('#' * 80)
                    print('press esc or close signal window to stop the recording')
                    print('#' * 80)
                    while True:
                        file.write(self.q_rec.get())
        except KeyboardInterrupt:
            print('\nRecording finished: ' + repr(self.filename))
        except Exception as e:
            print(e)

    def update_plot(self, frame):
        """
        This is called by matplotlib for each plot update.
        Typically, audio callbacks happen more frequently than plot updates,
        therefore the queue tends to contain multiple blocks of audio data.
        """

        while True:
            try:
                data = self.q_plot.get_nowait()
            except queue.Empty:
                break
            shift = len(data)
            self.plotdata = np.roll(self.plotdata, -shift, axis=0)
            self.plotdata[-shift:, :] = data
        for column, line in enumerate(self.lines):
            line.set_ydata(self.plotdata[:, column])
        return self.lines

    def close_plot_by_escape(self, event):
        if event.key == 'escape':
            plt.close()

    def close_plot_by_closevent(self, event):
        print('Hossa!')
        # plt.close()

    def show_plot(self):
        if self.samplerate is None:
            device_info = sd.query_devices(self.device, 'input')
            self.samplerate = device_info['default_samplerate']

        length = int(self.window * self.samplerate / (1000 * self.downsample))
        self.plotdata = np.zeros((length, len(self.channels)))

        fig, ax = plt.subplots()
        fig.canvas.mpl_connect(
            'key_press_event', self.close_plot_by_escape)
        fig.canvas.mpl_connect('close_event', self.close_plot_by_closevent)
        fig.canvas.mpl_connect('button_press_event',
                               self.close_plot_by_closevent)
        self.lines = ax.plot(self.plotdata)
        if len(self.channels) > 1:
            ax.legend([f'channel {c}' for c in self.channels],
                      loc='lower left', ncol=len(self.channels))
        ax.axis((0, len(self.plotdata), -1, 1))
        ax.set_yticks([0])
        ax.yaxis.grid(True)
        ax.tick_params(bottom=False, top=False, labelbottom=False,
                       right=False, left=False, labelleft=False)
        fig.tight_layout(pad=0)

        stream = sd.InputStream(
            device=self.device, channels=max(self.channels),
            samplerate=self.samplerate, callback=self.callback_plot)
        ani = FuncAnimation(fig, self.update_plot,
                            interval=self.interval, blit=True)

        with stream:
            plt.show()
