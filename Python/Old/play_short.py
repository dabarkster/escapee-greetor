#!/usr/bin/env python3

import argparse


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

#parser = argparse.ArgumentParser(description=__doc__)
#parser.add_argument('filename', help='audio file to be played back')
#parser.add_argument('-d', '--device', type=int_or_str,
#                    help='output device (numeric ID or substring)')
#args = parser.parse_args()

try:
    import sounddevice as sd
    import soundfile as sf
    data, fs = sf.read('temp.wav', dtype='float32')
    sd.play(data, fs, device=0)
    status = sd.wait()
    if status:
        parser.exit('Error during playback: ' + str(status))
except KeyboardInterrupt:
    parser.exit('\nInterrupted by user')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))