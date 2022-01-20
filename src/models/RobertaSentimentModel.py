from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
from scipy.special import softmax

import os


class RobertaSentimentModel: 

    MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
    labels = ["negative", "neutral", "positive"]


    
    def init_model(self):

        if not "cardiffnlp" in os.listdir():
            self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL)
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL, local_files_only=True)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.MODEL, local_files_only=True   )

        self.tokenizer.save_pretrained(self.MODEL)
        self.model.save_pretrained(self.MODEL)



    def preprocess(self, textInput: str):

        new_text = []
     
        for t in textInput.split(" "):
            t = '@user' if t.startswith('@') and len(t) > 1 else t
            t = 'http' if t.startswith('http') else t
            new_text.append(t)
        return " ".join(new_text)

   

    def predict(self, textInput: str):

        text = self.preprocess(textInput)
        encoded_input = self.tokenizer(text, return_tensors='pt')
        output = self.model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        
        final_score = -1*scores[0] + 1*scores[2]

        return final_score


