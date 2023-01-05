#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib.

Matplotlib and NumPy have to be installed.

"""
import queue
import sys
import subprocess
import signal

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd


def close_plot_by_escape(event):
    if event.key == 'escape':
        print(f'escape is pressed! Sending SIGINT to process {process.pid}')
        process.send_signal(signal.SIGINT)
        plt.close()


def close_plot_by_closevent(event):
    print(f'Close event!! Sending SIGINT to process {process.pid}')
    process.send_signal(signal.SIGINT)
    plt.close()


channels = [1]  # input channels to plot -> int
device = None  # input device (numeric ID or substring) -> int_or_str
window = 200  # visible time slot, default=200 ms  -> float
interval = 30  # minimum time between plot updates  -> float
blocksize = None  # block size (in samples)  -> int
samplerate = None  # sampling rate of audio device  -> float
downsample = 10  # display every Nth sample, default=10  -> int
filename = 'audio'  # audio file to store recording to  -> str
subtype = "PCM_24"  # sound file subtype (e.g. "PCM_24") -> str

mapping = [c - 1 for c in channels]

q = queue.Queue()


def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata[::downsample, mapping])


def update_plot(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global plotdata
    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines


process = subprocess.Popen(["venv/bin/python3", "audio_recording.py"], start_new_session=True)
print(f'Start recording script as PID: {process.pid}')

try:
    if samplerate is None:
        device_info = sd.query_devices(device, 'input')
        samplerate = device_info['default_samplerate']

    length = int(window * samplerate / (1000 * downsample))
    plotdata = np.zeros((length, len(channels)))

    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('key_press_event', close_plot_by_escape)
    fig.canvas.mpl_connect('close_event', close_plot_by_closevent)
    lines = ax.plot(plotdata)
    if len(channels) > 1:
        ax.legend([f'channel {c}' for c in channels],
                  loc='lower left', ncol=len(channels))
    ax.axis((0, len(plotdata), -1, 1))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.tick_params(bottom=False, top=False, labelbottom=False,
                   right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)

    stream = sd.InputStream(
        device=device, channels=max(channels),
        samplerate=samplerate, callback=audio_callback)
    ani = FuncAnimation(fig, update_plot, interval=interval, blit=True)

    with stream:
        plt.show()

except (Exception, KeyboardInterrupt) as e:
    process.send_signal(signal.SIGINT)
