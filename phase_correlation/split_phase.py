import librosa as rs
import soundfile as sf
import numpy as np
import sys

CHANNELS = ['left', 'right']
if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = 'stereo.wav'

waveform, sr = rs.load(filename, mono=False)

for ch in range(waveform.shape[0]):
    w = waveform[ch]
    pos = np.zeros_like(w)
    neg = np.zeros_like(w)
    pos[w > 0] = w[w > 0]
    neg[w <= 0] = w[w <= 0]
    sf.write(f'{CHANNELS[ch]}_neg.wav', neg, sr)
    sf.write(f'{CHANNELS[ch]}_pos.wav', pos, sr)
