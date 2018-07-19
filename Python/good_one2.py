#!/usr/bin/env python3
"""Play an audio file using a limited amount of memory.

The soundfile module (http://PySoundFile.rtfd.io/) must be installed for
this to work.  NumPy is not needed.

In contrast to play_file.py, which loads the whole file into memory
before starting playback, this example program only holds a given number
of audio blocks in memory and is therefore able to play files that are
larger than the available RAM.

"""
from __future__ import division, print_function
import argparse
try:
    import queue  # Python 3.x
except ImportError:
    import Queue as queue  # Python 2.x
import sys
import threading

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

wav_file = '/home/pi/escapee-greetor/Python/temp.wav'
BUFFER = 300
BLOCK = 2048
channels = [1]
mapping = [0]

q = queue.Queue(maxsize=BUFFER)
event = threading.Event()



def audio_callback(outdata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    print(outdata)
    q.put(outdata[:, mapping])
    

    print("************audio")
    #print(outdata)
    #q.put(outdata[::10, 1])
    #print(data)

def update_plot(frame):
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


try:
    print("**************start main")
    from matplotlib.animation import FuncAnimation
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    import matplotlib.pyplot as plt


    f = sf.SoundFile(wav_file)
    data = f.read(frames=100, dtype='float')
    q.put(data)  # Pre-fill queue
    
    stream = sd.OutputStream(
        samplerate=f.samplerate, blocksize=BLOCK,
        device=0, channels=f.channels, dtype='float32',
        callback=audio_callback, finished_callback=event.set)

    #sd.play(data)
    print(len(data))

    length = int(200 * 44100 / (1000 * 10))
    plotdata = np.zeros((length, len(channels)))  
    fig, ax = plt.subplots()
    lines = ax.plot(plotdata)
    if len(channels) > 1:
        ax.legend(['channel {}'.format(c) for c in channels],
                  loc='lower left', ncol=len(channels))
    ax.axis((0, len(plotdata), -.01, .01))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.tick_params(bottom='off', top='off', labelbottom='off',
                   right='off', left='off', labelleft='off')
    fig.tight_layout(pad=0)





    interval = 30
    ani = FuncAnimation(fig, update_plot, interval=interval, blit=True)
    
    #data = q.get_nowait()
 
    with stream:
        print("**************start stream")
        timeout = BLOCK * BUFFER / f.samplerate
        plt.show()

        #while len(data) > 1:
        #    print("++++++++++++get data")
        data = f.read(frames=100, dtype='float')
        q.put(data, timeout=timeout)

        #event.wait()  # Wait until playback is finished
    
    sd.wait()
    print(len(data))
    print("done")
    while 1:
        pass


    with sd.Stream(channels=f.channels, callback=audio_callback):
        print("**************start stream")
        #timeout = BLOCK * BUFFER / f.samplerate
        plt.show()
        print("++++++++++++get data")
        #data = f.read(frames=-1, dtype='float')
        #q.put(data, timeout=timeout)

        event.wait()  # Wait until playback is finished

    while 1:
        pass



except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except queue.Full:
    # A timeout occured, i.e. there was an error in the callback
    parser.exit(1)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
