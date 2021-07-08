import speech_recognition as sr
import pyaudio

r = sr.Recognizer()

mic = sr.Microphone()


p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(info['index'], info['name'])



try:
    with mic as source:
        print("recording")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=5)

    print(
        f"phrase: "
        f"{r.recognize_google(audio)}\n\n")
except:
    print("Could not get audio")