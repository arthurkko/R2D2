import speech_recognition as sr

def listen():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Estou ouvindo!")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        phrase = str(r.recognize_google(audio, language='pt-br'))
        print(phrase)
        
        return phrase

    except Exception as e:
        print("Exception: " + str(e))

