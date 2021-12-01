from libre import translate
from wolf import respond
from spacy_bow import chat
from watson_tts import speak
from sr import listen
from playsound import playsound

question = ""
tries = 0
response = {}
question = listen().lower()

while(question!="sair"):
    flag, response = chat(question, response)
    if flag==False:
        question = translate(question, "pt", "en")
        tries, response = respond(tries, question, response)
        r = translate(response["result"])
        print(f"{r}/n")
        speak(r)
        playsound("speach.wav")
    else:
        tries = 0
        r = response["result"]
        print(f"{r}/n")
        playsound("speach.wav")
        

    question = listen().lower()