import os
import sys
import time
import logging
import queue

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sounddevice as sd
import soundfile as sf
import numpy as np


class Recorder:
    def __init__(self) -> None:
        self.channels = [1]  # input channels to plot -> int
        # input device (numeric ID or substring) -> int_or_str
        self.device = None
        self.window = 200  # visible time slot, default=200 ms  -> float
        self.interval = 30  # minimum time between plot updates  -> float
        self.blocksize = 1024  # block size (in samples)
        self.downsample = 10  # display every Nth sample, default=10  -> int
        # audio file to store recording to  -> str
        self.subtype = "PCM_16"  # sound file subtype (e.g. "PCM_24") -> str
        self.mapping = [c - 1 for c in self.channels]
        device_info = sd.query_devices(self.device, 'input')
        # sampling rate of audio device. soundfile expects int -> int
        self.samplerate = int(
            device_info['default_samplerate'])   # type: ignore

        # If output audiofilename already exists, inc counter by one
        base_filename = 'output'
        filename_num = 1
        while os.path.exists(f"{base_filename}_{filename_num}.wav"):
            filename_num += 1
        self.filename = f"{base_filename}_{filename_num}.wav"

        self.q_rec = queue.Queue()
        self.q_plot = queue.Queue()

    def callback_record(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        self.q_rec.put(indata.copy())
        self.q_plot.put(indata[::self.downsample, self.mapping])

    def record(self, max_duration=20):
        try:
            fig = self.prepare_plot()
            ani = FuncAnimation(fig, self.update_plot,
                                interval=self.interval, blit=True)

            self.stream = sd.InputStream(samplerate=self.samplerate,
                                         device=self.device,
                                         channels=max(self.channels),
                                         callback=self.callback_record)

            # Make sure the file is opened before recording anything:
            with sf.SoundFile(self.filename, mode='x', samplerate=self.samplerate,
                              channels=max(self.channels), subtype=self.subtype) as file:
                print('#' * 71)
                print(
                    '# press esc or close the audio waveform window to stop the recording #')
                print('#' * 71)
                with self.stream:
                    """
                    This part of the code is based on the solution provided in the following StackOverflow post:
                    https://stackoverflow.com/a/33050617/16480807.

                    It allows for updating the plot and writing the audio data to a file from the same stream 
                    and in the same process.
                    """
                    t_end = time.time() + max_duration
                    while time.time() < t_end and plt.fignum_exists(fig.number):  # Records max timeout seconds # type: ignore
                        plt.pause(0.001)
                        file.write(self.q_rec.get())
                    plt.close()
                    logging.info(
                        'Recording finished due to closing of the audio waveform window.')
                    logging.info(f'Write temporary audiofile.')

        except KeyboardInterrupt:
            plt.close()
            logging.info('Recording finished due to keyboard interruption.')
            logging.info('Recording finished: ' + repr(self.filename))

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
        plt.close()

    def prepare_plot(self):
        if self.samplerate is None:
            device_info = sd.query_devices(self.device, 'input')
            self.samplerate = device_info['default_samplerate']  # type: ignore

        length = int(self.window * self.samplerate / (1000 * self.downsample))
        self.plotdata = np.zeros((length, len(self.channels)))

        fig, ax = plt.subplots()
        fig.canvas.mpl_connect(
            'key_press_event', self.close_plot_by_escape)
        fig.canvas.mpl_connect('close_event', self.close_plot_by_closevent)
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

        return fig
