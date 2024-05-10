import torch
import torch.nn as nn
from transformers import BertTokenizer,BertModel

bert = BertModel.from_pretrained('bert-base-uncased')
class conv_layer(nn.Module):
    def __init__(self):
        super(conv_layer,self).__init__()
        self.conv1=nn.Conv1d(in_channels=70,out_channels=70,kernel_size=3)
        self.relu=nn.ReLU()
        self.pool1=nn.MaxPool1d(2,stride=2)
        
    def forward(self,x):
        x=self.conv1(x)
        x=self.relu(x)
        x=self.pool1(x)
        
        return x
class NewsBERT_LSTM(nn.Module):
    def __init__(self):
        super(NewsBERT_LSTM,self).__init__()
        self.bert=bert
        

        self.conv=conv_layer()
        
        self.LSTM=nn.LSTM(input_size=383,hidden_size=64,batch_first=True,bidirectional=True,num_layers=1)
        self.layernorm=nn.LayerNorm(64*2)

        self.fc1=nn.Linear(64*2,64)
        self.fc2=nn.Linear(64,32)
        self.fc3=nn.Linear(32,1)


    def forward(self,x,y):
        x,y=x.int(),y.int()
        x=self.bert(x,y)
        x=x.last_hidden_state
        
        x=self.conv(x)
        
        
        x,(hn,cn)=self.LSTM(x)
        x=self.layernorm(x)
        x=x[:,-1,:]
        
        x=self.fc1(x)
        x=nn.ReLU()(x)
        x=self.fc2(x)
        x=nn.ReLU()(x)
        x=self.fc3(x)
        x=nn.Sigmoid()(x)
        return x