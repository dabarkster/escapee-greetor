import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import wave , sys , os , struct

wave_file = wave.open('temp.wav', 'r')
data_size = wave_file.getnframes()
sample_rate = wave_file.getframerate()

x = 0
while True:

    waveData = wave_file.readframes(10000)
    signal = np.fromstring(waveData , 'Int16')
    Time=np.linspace(0, len(signal), num=len(signal))

    plt.figure()
    fig = plt.figure(figsize=(3,3) , frameon=False)
    #fig = plt.figure(frameon=False)
    ax = fig.add_axes([0, 0, 1, 1])
    #ax.axis('off')

    plt.axis('off')
    line = plt.plot(Time,signal , 'w')
    plt.setp(line, linewidth=10)

    plt.savefig('signal.png')
    plt.close

    x+= 1
    if  wave_file.tell() == data_size:
            break