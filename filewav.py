import wave 
import numpy as np

with wave.open("/Users/arthurkunko/Desktop/R2D2/text2.wav") as w:
    framerate = w.getframerate()
    frames = w.getnframes()
    channels = w.getnchannels()
    width = w.getsampwidth()
    print('sampling rate:', framerate, 'Hz')
    print('length:', frames, 'samples')
    print('channels:', channels)
    print('sample width:', width, 'bytes')
    
    data = w.readframes(frames)

print(f"lenght data: {len(data)}\ntype data: {type(data)}")

print(data)
sig = np.frombuffer(data, dtype='<i2').reshape(-1, channels)
print(sig)