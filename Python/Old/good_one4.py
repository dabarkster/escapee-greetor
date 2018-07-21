#!/usr/bin/env python3


wav_file = '/home/pi/escapee-greetor/Python/temp.wav'
BUFFER = 300
BLOCK = 2048
channels = [1]
mapping = [0]

q = queue.Queue(maxsize=BUFFER)
event = threading.Event()



try:
    print("**************start main")
    from matplotlib.animation import FuncAnimation
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    import matplotlib.pyplot as plt
