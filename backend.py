from bert import NewsBERT_LSTM,conv_layer
from transformers import BertTokenizer
import torch
from flask import Flask,request,jsonify
import re


device='cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model=torch.load("model2.pt",map_location=torch.device(device))
model.eval()

app=Flask(__name__)

def remove_punctuations(word):
    words = word.split()
    pattern=r'[^\w\s]'
    string=re.sub(pattern,'',word)
    return string.lower()

@app.route('/predict',methods=['POST'])
def predict():
    text=request.get_json()['news']
    news=remove_punctuations(text)
    tokenized_text=tokenizer.encode_plus(text,max_length=70,pad_to_max_length=True,truncation=True)
    input_ids,attn_mask=torch.tensor(tokenized_text['input_ids']),torch.tensor(tokenized_text['attention_mask'])
    input_ids=input_ids.to(device)
    attn_mask=attn_mask.to(device)
    with torch.no_grad():
        pred=model(input_ids.unsqueeze(0),attn_mask.unsqueeze(0))
        print(pred.item())
        if pred.item()>0.4:
            label='true'
            return jsonify({"news":text,
                            "label":label})
        else:
            label='fake'
            return jsonify({"news":text,
                            "label":label})
        
if __name__=="__main__":
    app.run(debug=True)
