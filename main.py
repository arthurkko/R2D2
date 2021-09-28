import speech_recognition as sr
import json
import requests
from playsound import playsound
from dotenv import load_dotenv
import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import TextToSpeechV1


load_dotenv()

api_translator = os.environ.get("wt_translator_key")
url_translator = os.environ.get("wt_translator_url")
authenticator = IAMAuthenticator(api_translator)
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)

language_translator.set_service_url('https://api.us-south.language-translator.watson.cloud.ibm.com')

api_tts = os.environ.get("wt_tts_key")
authenticator = IAMAuthenticator(api_tts)
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)

text_to_speech.set_service_url("https://api.us-south.text-to-speech.watson.cloud.ibm.com")

r = sr.Recognizer()

def conversational_api(app_id):

    error =  ""
    question = "question"
    tries = 0

    while (question!="sair"):
        try:
            with sr.Microphone() as source:
                print("Pergunte!\n")
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)

            question = r.recognize_google(audio, language='pt-br')
            print(f"phrase: {question}\n\n")
                
        except Exception as e:
            print("Exception: " + str(e))

        if question!="sair":
            translation = language_translator.translate(
                text=question,
                model_id='pt-en').get_result()
            print("translation:")
            print(json.dumps(translation, indent=2, ensure_ascii=False))
            print("\n\n")

            question = translation['translations'][0]['translation'].replace(" ", "+")       # formatar a pergunta no formato da url

            if tries==0:
                url = "http://api.wolframalpha.com/v1/conversation.jsp?appid="+app_id+"&i="+question
                response = json.loads(requests.get(url).text)
                if "error" in response:
                    error = response["error"]
                else:
                    print(f"{response['result']}\n")
                    tries += 1

            else:                                       # a continuação da conversa ocorre em outra url
                if "Wolfram|Alpha" not in error:
                    conv_id = response["conversationID"]
                    host = response["host"]
                    if "s" in response:                 # raros casos que response possui a key 's'
                        s = response["s"]
                        url = "http://"+host+"/api/v1/conversation.jsp?appid="+app_id+"&conversationid="+conv_id+"&i="+question+"&s="+s
                    else:
                        url = "http://"+host+"/api/v1/conversation.jsp?appid="+app_id+"&conversationid="+conv_id+"&i="+question

                response = json.loads(requests.get(url).text)
                if "error" in response:
                    error = response["error"]
                else:
                    print(f"{response['result']}\n")
                    translation = language_translator.translate(
                        text=response['result'],
                        target='pt').get_result()
                    print(json.dumps(translation, indent=2, ensure_ascii=False))
                    with open('text.wav', 'wb') as audio_file:     # criar arquivo .wav do text
                        try:
                            audio_file.write(
                                text_to_speech.synthesize(
                                    text=translation['translations'][0]['translation'],
                                    voice="pt-BR_IsabelaV3Voice",
                                    accept='audio/wav'        
                                ).get_result().content)
                        except Exception as e:
                            print("Exception: " + str(e))
                    playsound("text.wav")
                    error = ""

            if error!="":
                if ("No result is available" in error) and question!="": # 
                    print("\nNão sei responder a pergunta :/")
            else:
                print(f"{response['result']}\n")
                translation = language_translator.translate(
                    text=response['result'],
                    target='pt').get_result()
                print(json.dumps(translation, indent=2, ensure_ascii=False))
                with open('text.wav', 'wb') as audio_file:     # criar arquivo .wav do text
                    try:
                        audio_file.write(
                            text_to_speech.synthesize(
                                text=translation['translations'][0]['translation'],
                                voice="pt-BR_IsabelaV3Voice",
                                accept='audio/wav'        
                            ).get_result().content)
                    except Exception as e:
                        print("Exception: " + str(e))
                playsound("text.wav")

    return error

app_id = os.environ.get("wolframalpha_key")

error = conversational_api(app_id)
if error == "No result is available":
    print ("Tchau\n")


