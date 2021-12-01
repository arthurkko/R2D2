import spacy
import json
from spacy.util import minibatch
from spacy.training.example import Example
import random

def train(data):
    try:
        nlp = spacy.load("./mia_model")
        return nlp

    except:

        # Create an empty model
        nlp = spacy.blank("pt")

        # Add the TextCategorizer to the empty model
        textcat = nlp.add_pipe("textcat")

    

        print("Categorias:\n")
        # Add labels to text classifier
        for i in data["intents"]:
            textcat.add_label(i["tag"])
            print(i['tag'])
        print("\n")

        list_patterns = [i["patterns"] for i in data["intents"]]
        train_texts = [i for s in list_patterns for i in s]
        tuple_label = [(i['tag'], len(i['patterns'])) for i in data['intents']]
        labels =[]
        for t in tuple_label:
            l = []
            l = [t[0]]*t[1]
            labels += l
        train_labels = [{'cats': {'greeting': label == 'greeting',
                                'goobye': label == 'goodbye',
                                'thanks': label == 'thanks',
                                'name': label == 'name',
                                'location': label == 'location'}} 
                        for label in labels]
        train_data = list(zip(train_texts, train_labels))

        random.seed(1)
        spacy.util.fix_random_seed(1)
        optimizer = nlp.begin_training()

        losses = {}
        for epoch in range(5):
            random.shuffle(train_data)
            # Create the batch generator with batch size = n
            batches = minibatch(train_data, size=30)
            # Iterate through minibatches
            for batch in batches:
                for text, labels in batch:
                    doc = nlp.make_doc(text)
                    example = Example.from_dict(doc, labels)
                    nlp.update([example], sgd=optimizer, losses=losses)
            print(losses)

        nlp.to_disk("./mia_model")

        return nlp

def chat(text, response):
    with open("intents.json") as file:
        data = json.load(file)
        nlp = train(data)

    docs = [nlp.tokenizer(text)]
        
    # Use textcat to get the scores for each doc
    textcat = nlp.get_pipe('textcat')
    scores = textcat.predict(docs)
    # print(scores)

    # From the scores, find the label with the highest score/probability
    predicted_label = scores.argmax(axis=1)
    # print(predicted_label)
    predict = textcat.labels[predicted_label[0]]
    # print(predict)

    if scores[0][predicted_label[0]] >= 0.9:
        for list in data["intents"]:
            if list['tag'] == predict:
                r = list['responses']
                response['result'] = random.choice(r)
                flag = 1
                return flag, response
    else:
        flag = 0
        return flag, response
    
