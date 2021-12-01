import json
from dotenv import load_dotenv
import os
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

load_dotenv()

api_tts = os.environ.get("wt_tts_key")
authenticator = IAMAuthenticator(api_tts)
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)

text_to_speech.set_service_url("https://api.us-south.text-to-speech.watson.cloud.ibm.com")

voices = text_to_speech.list_voices().get_result()
# print(json.dumps(voices, indent=2)        # lista completa de vozes
# for voice in voices["voices"]:            # filtrar vozes por idioma
#     if "pt-BR" in voice["url"]:
#         print(json.dumps(voice, indent=2))
#         print("\n")



def speak(texto):
    with open('speach.wav', 'wb') as audio_file:     # criar arquivo .wav do text
        try:
            audio_file.write(
                text_to_speech.synthesize(
                    text=texto,
                    voice="pt-BR_IsabelaV3Voice",
                    accept='audio/wav'        
                ).get_result().content)
        except Exception as e:
            print("Exception: " + str(e))