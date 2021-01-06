from model import HMM_model
from nltk.corpus import treebank 
import re
import numpy as np
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
def tokenize(str):
    tokens=[]
    for matches in re.findall(r'(\.|\,|"|"|…|\?|\:|\!|\;|\ |)*(\w*)(\.|\,|"|"|…|\?|\:|\!|\;|\ |)',symbols):
        for token in matches:  
            if token not in ['',' ']:
                tokens.append(token)
    return tokens


f = open('message.txt', encoding='utf-8').readlines()
data = []
for sent in f:
    l = []
    tokens = sent.split()
    for token in tokens:
        t = token.split('\\')
        l.append([t[0], t[1]])
    data.append(l)

symbols='tôi lao ra khỏi lớp và đi thẳng đến thư_viện.'
x = tokenize(symbols)

# using my model
# data = treebank.tagged_sents()
HMM = HMM_model(data)
confuse = np.zeros((len(HMM._tag_to_index),len(HMM._tag_to_index)))
Xs = []
Ys = []
for sents in data:
    token_sequence =[]
    tag_sequence =[]
    for token in sents:
        token_sequence.append(token[0])
        tag_sequence.append(token[1])
    Xs.append(token_sequence)
    Ys.append(tag_sequence)




c=0
total = 0
for i in range(len(Xs)):
    pred_ys = [k[1] for k in HMM.predict(Xs[i])]
    for j in range(len(Xs[i])):
        try:
            confuse[HMM._tag_to_index[pred_ys[j]]][HMM._tag_to_index[Ys[i][j]]]+=1
        except:
            print(i,j)
        if HMM._tag_to_index[pred_ys[j]] == HMM._tag_to_index[Ys[i][j]]:
            c+=1
        total+=1

# print(confuse.shape)
# df = pd.DataFrame(confuse)
# # columns=list(self._tag_to_index.keys()),index=list(self._tag_to_index.keys())
# sn.heatmap(df)
# plt.show()
# print(confuse)
A = sum([confuse[i][i] for i in range(len(HMM._index_to_tag))])/total
from nltk.tag.hmm import HiddenMarkovModelTrainer

trainer = HiddenMarkovModelTrainer()
tagger = trainer.train_supervised(data)

c=0
total = 0
# print(len(tagger._symbols))
# print(len(HMM._index_to_word))
# print(len(tagger._states))
# print(len(HMM._index_to_tag))
print([k[1] for k in HMM.predict(Xs[27])])
print([k[1] for k in tagger.tag(Xs[27])])
print(Ys[27])
for i in range(len(Xs)):
    pred_ys = [k[1] for k in tagger.tag(Xs[i])]
    for j in range(len(Xs[i])):
        # confuse[tagger._tag_to_index[pred_ys[j]]][tagger._tag_to_index[Ys[i][j]]]+=1
        if pred_ys[j]==Ys[i][j]:
            c+=1
        total+=1
# print(confuse.shape)
# df = pd.DataFrame(confuse)
# # columns=list(self._tag_to_index.keys()),index=list(self._tag_to_index.keys())
# sn.heatmap(df)
# plt.show()
# print(confuse)
print(A,c/total)