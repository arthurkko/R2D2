from dotenv import load_dotenv
import os
import requests
import json

# import wolframalpha


#     A biblioteca 'wolframalpha' é limitada. Ela traz o conteúdo direto do site com filtro razo (results).

#     Para a aplicação no robô, Wolfram|Alpha possui uma API específica, capaz de retornar em maior quantidade
#     respostas curtas, tendo em vista esta aplicação como alvo. 

#     Mais info: https://products.wolframalpha.com/conversational-api/documentation/


# question = input('Question: ')
# app_id = os.environ.get("wolframalpha_key")
# client = wolframalpha.Client(app_id)

# res = client.query(question)
# answer = next(res.results).text
# # answer = res.pod

# print(answer)




load_dotenv()
app_id = os.environ.get("wolframalpha_key")

def respond(tries=False, question='', response=None):

    # question = question.replace(" ", "+")

    if tries==0:
        url = "http://api.wolframalpha.com/v1/conversation.jsp"
        params = {
            "appid": app_id, 
            "i": question
            }
        response = requests.get(url, params=params).text
        print(response)
        response = json.loads(response)
        tries = 1

    else:   # a continuação da conversa ocorre em outra url
        host = response["host"]
        url = "http://"+host+"/api/v1/conversation.jsp"
        if "s" in response: # raros casos que response possui a key 's'
            params = {
                "appid": app_id, 
                "i": question, 
                "conv_id": response["conversationID"], 
                "s": response["s"]
                }                
        else:
            params = {
                "appid": app_id, 
                "i": question, 
                "conv_id": response["conversationID"]
                }
        response = json.loads(requests.get(url, params=params).text)
    
    if "error" in response:
        response['result'] = "Eu não entendi consegui te entender!"
        tries = False


    return tries, response


