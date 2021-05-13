import speech_recognition as sr
import pyaudio
import time

r = sr.Recognizer()

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    data = stream.read(1024)
    return (data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=pyaudio.paInt24,
                channels=2,
                rate=44100,
                input_device_index=0,
                input=True,
                stream_callback=callback)
print("\n\nrecording..\n\n")

# wait for stream to finish (5)
while stream.is_active():
    audio = stream.read(1024)
    print(f"{r.audio}\n")
pritn("\n\ndone recording!\n\n")

# stop stream (6)
stream.stop_stream()
stream.close()

# close PyAudio (7)
p.terminate()

