from dotenv import load_dotenv
import os
import requests
import json

'''
    A biblioteca 'wolframalpha' é limitada. Ela traz o conteúdo direto do site com filtro razo (results).

    Para a aplicação no robô, Wolfram|Alpha possui uma API específica, capaz de retornar em maior quantidade
    respostas curtas, tendo em vista esta aplicação como alvo. 

    Mais info: https://products.wolframalpha.com/conversational-api/documentation/
'''

# question = input('Question: ')
# app_id = os.environ.get("wolframalpha_key")
# client = wolframalpha.Client(app_id)

# res = client.query(question)
# answer = next(res.results).text
# # answer = res.pod

# print(answer)






def conversational_api(app_id):

    error =  ""
    question = "question"
    tries = 0

    while (question!=""):
        question = input("Question: ")
        question = question.replace(" ", "+")       # formatar a pergunta no formato da url

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
                error = ""

        if error!="":
            if ("No result is available" in error) and question!="": # 
                print("\nNão sei responder a pergunta :/")
        else:
            pass

    return error

app_id = os.environ.get("wolframalpha_key")

error = conversational_api(app_id)
if error == "No result is available":
    print ("Tchau\n")
