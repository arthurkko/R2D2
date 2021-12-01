from libre import translate
from wolf import respond
from spacy_bow import chat


question = ""
tries = 0
response = {}
question = input("Question: ").lower()
while(question!="sair"):
    flag, response = chat(question, response)
    if flag==False:
        tries, response = respond(tries, question, response)
        translate(response["result"])
    else:
        print(response["result"])
        tries = 0

    question = input("Question: ")