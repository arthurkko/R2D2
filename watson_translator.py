import json
from dotenv import load_dotenv
import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

load_dotenv()

APIKey = os.environ.get("wt_translator_key")
url = os.environ.get("wt_translator_url")

authenticator = IAMAuthenticator(APIKey)
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)

language_translator.set_service_url('https://api.us-south.language-translator.watson.cloud.ibm.com')

# languages = language_translator.list_languages().get_result()
# for lang in languages['languages']:               #print por sigla
#     if lang['country_code']=="BR":
#         print(json.dumps(lang, indent=2))
    # print(json.dumps(languages, indent=2))        #print tudo

texto = "Hi, how are you?"
translation = language_translator.translate(
    text=texto,
    target='pt').get_result()
print(json.dumps(translation, indent=2, ensure_ascii=False))
print("\n\n")
print(translation['translations'][0]['translation'])
print("\n\n")