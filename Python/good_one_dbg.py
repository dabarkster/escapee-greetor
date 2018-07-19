#!/usr/bin/env python3
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
BUFFER = 200
BLOCK = 2048
channels = [1,1]
print("trest")
q = queue.Queue(maxsize=BUFFER)
event = threading.Event()

def callback(outdata, frames, time, status):
    
    print("**************audio callback")
    assert frames == BLOCK
    if status.output_underflow:
        print('Output underflow: increase blocksize?', file=sys.stderr)
        raise sd.CallbackAbort
    assert not status
    try:
        data = q.get_nowait()
        sig = np.frombuffer(data, dtype=np.float32, count=30)
        #print(sig)
    except queue.Empty:
        print('Buffer is empty: increase buffersize?', file=sys.stderr)
        raise sd.CallbackAbort
    if len(data) < len(outdata):
        outdata[:len(data)] = data
        outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
        raise sd.CallbackStop
    else:
        outdata[:] = data
    

def update_plot(frame):
    global plotdata
    
    while True:
        try:
            data = q.get_nowait()
            sig = np.frombuffer(data, dtype=np.float32, count=30)
            print(sig)
        except queue.Empty:
            break
        shift = len(sig)
        plotdata = np.roll(plotdata, -shift, axis=0)
        #print(shift)
        #print(data)
        #plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :]  = sig
        #print(lines)
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines        
