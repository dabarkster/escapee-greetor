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
channels = [1,1]

q = queue.Queue(maxsize=BUFFER)
event = threading.Event()



def callback(outdata, frames, time, status):
    
    #print("**************audio callback")
    assert frames == BLOCK
    if status.output_underflow:
        print('Output underflow: increase blocksize?', file=sys.stderr)
        raise sd.CallbackAbort
    assert not status
    try:
        data = q.get_nowait()
        sig = np.frombuffer(data, dtype=np.float32, count=30)
        plt.plot(sig)
    except queue.Empty:
        print('Buffer is empty: increase buffersize?', file=sys.stderr)
        raise sd.CallbackAbort
    if len(data) < len(outdata):
        outdata[:len(data)] = data
        outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
        raise sd.CallbackStop
    else:
        outdata[:] = data
    

    #print("************outdata")
    #print(outdata)
    #q.put(outdata[::10, 1])
    #print(data)

def update_plot(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    print("**************update_plot callback")
    global plotdata
    while True:
        try:
            data = q.get_nowait()
            sig = np.frombuffer(data, dtype=np.float32)
            print(data)
        except queue.Empty:
        	print("======================break")
        	break
        shift = len(data)
        print("shift")
        print(shift)
        print("data")
        print(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        #print("plotdata")
        print(plotdata)
        #print(plotdata.size)
        plotdata[-shift:, :]  = data
        #print(plotdata.size)
        print(lines)

    for column, line in enumerate(lines):
        #print("column")
        #print(column)
        #print("line")
        #print(line)
        line.set_ydata(plotdata[:, column])
    return lines


try:
    print("**************start main")
    from matplotlib.animation import FuncAnimation
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    import matplotlib.pyplot as plt


    f = sf.read()

    length = int(200 * 44100 / (1000 * 10))
    print(length)
    length = 4096
    plotdata = np.zeros((length, len(channels)))
    print(length)
    
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



    stream = sd.RawOutputStream(
        samplerate=f.samplerate, blocksize=BLOCK,
        device=0, channels=f.channels, dtype='float32',
        callback=callback, finished_callback=event.set)

    interval = 30
    ani = FuncAnimation(fig, update_plot, interval=interval, blit=True)
    
    with stream:
        print("**************start stream")
        timeout = BLOCK * BUFFER / f.samplerate
        plt.show()
        while data:
            data = f.buffer_read(BLOCK, ctype='float')
            #sig = np.frombuffer(data, dtype=np.float32, count=30)
            #print("*************sig")
            #print(data)

            #print(sig.value)
            q.put(data, timeout=timeout)

        event.wait()  # Wait until playback is finished

except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except queue.Full:
    # A timeout occured, i.e. there was an error in the callback
    parser.exit(1)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
