import speech_recognition as sr

r = sr.Recognizer()

try:
    with sr.Microphone() as source:
        print("recording")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    print(
        f"phrase: "
        f"{r.recognize_google(audio, language='pt-br')}\n\n")
    

except Exception as e:
    print("Exception: " + str(e))