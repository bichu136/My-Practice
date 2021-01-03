import re 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
f = open('message.txt', encoding='utf-8').readlines()
data = []
for sent in f:
    l = []
    tokens = sent.split()
    for token in tokens:
        t = token.split('\\')
        l.append([t[0], t[1]])
    data.append(l)
# print(data)
# print all the things
symbols_set = []
tags_set = []
for sent in data:
    for token in sent:
        symbols_set.append(token[0])
        tags_set.append(token[1])

t = list(np.unique(np.array(tags_set))) +["<S>","<E>"]
_tag_to_index = {t[i]:i for i in range(len(t)) }
_index_to_tag = {i:t[i] for i in range(len(t)) }
t = list(np.unique(np.array(symbols_set))) +["<S>","<E>"]
_word_to_index = {t[i]:i for i in range(len(t)) }
_index_to_word = {i:t[i] for i in range(len(t)) }
observation_matrix = np.ones((len(_word_to_index),len(_tag_to_index)))/100
change_state_matrix = np.ones((len(_tag_to_index),len(_tag_to_index)))/100

for sents in data:
    t = [('<S>','<S>')]+sents + [('<E>','<E>')]
    for i in range(len(t)-1):
        observation_matrix[_word_to_index[t[i][0]]][_tag_to_index[t[i][1]]] +=1
        change_state_matrix[_tag_to_index[t[i][1]]][_tag_to_index[t[i+1][1]]] +=1
observation_matrix =  (observation_matrix.T/observation_matrix.sum(axis=1)).T
change_state_matrix = (change_state_matrix.T/change_state_matrix.sum(axis=1)).T
# print(change_state_matrix[_tag_to_index["<S>"]])


change_state_matrix[_tag_to_index["<E>"]] = np.zeros(change_state_matrix[_tag_to_index["<E>"]].shape)
observation_matrix[_word_to_index["<S>"]] = np.zeros(observation_matrix[_word_to_index["<S>"]].shape)
observation_matrix[_word_to_index["<S>"]][_tag_to_index["<S>"]] = 1.0

##our model
def calc_prop_1st(current_tag,next_observe):
    r = observation_matrix[_word_to_index[next_observe]] * change_state_matrix[_tag_to_index[current_tag]]
    return r
def calc_prop(next_word,current_prop):
    prop_for_word = observation_matrix[_word_to_index[next_word]]
    w = np.dot(prop_for_word.reshape(-1,1),np.transpose(current_prop).reshape(1,len(current_prop)))
    prop_for_all_tag = np.max(w*change_state_matrix,axis=1)
    previous_tags = np.argmax(w*change_state_matrix,axis=1)
    previous_tags = [_index_to_tag[i] for i in previous_tags]
    return prop_for_all_tag,previous_tags


def calc_prop_last(current_prop):
    return current_prop * change_state_matrix[:,_tag_to_index["<E>"]].T,[_index_to_tag[i] for i in range(len(_index_to_tag))]

def predict(x):
    
    tokens = ["<S>"] +x + ["<E>"]
    i = 0
    step = []
    prop = [observation_matrix[_word_to_index['<S>']]]
    while i<len(tokens)-2:
        prop_for_all_tags,previous_tags = calc_prop(tokens[i+1],prop[-1])
        step.append(previous_tags)
        prop.append(prop_for_all_tags)
        i+=1
    prop.pop(0)
    r = []
    i = len(prop)-1
    r = [_index_to_tag[np.argmax(prop[i])]]
    while(i>0):
        k= step[i][_tag_to_index[r[0]]]
        r = [k]+r
        i-=1
    return r

print(symbols_set)
def tokenize(str):
    tokens=[]
    for matches in re.findall(r'(\.|\,|"|"|…|\?|\:|\!|\;|\ |)*(\w*)(\.|\,|"|"|…|\?|\:|\!|\;|\ |)',symbols):
        for token in matches:  
            if token not in ['',' ']:
                tokens.append(token)
    return tokens



## validation on data train ## 
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

symbols='tôi lao ra khỏi lớp và đi thẳng đến thư_viện.'
x = tokenize(symbols)
confuse = np.zeros((len(_index_to_tag),len(_index_to_tag)))
c=0
total = 0
for i in range(len(Xs)):
    print(Xs[i])
    pred_ys = predict(Xs[i])
    for j in range(len(Xs[i])):
        confuse[_tag_to_index[pred_ys[j]]][_tag_to_index[Ys[i][j]]]+=1
        if _tag_to_index[pred_ys[j]]==_tag_to_index[Ys[i][j]]:
            c+=1
        total+=1
    print("---------------------------------")
print(confuse.shape)
df = pd.DataFrame(confuse)
# columns=list(_tag_to_index.keys()),index=list(_tag_to_index.keys())
sn.heatmap(df)
plt.show()
print(confuse)
A = sum([confuse[i][i] for i in range(28)])/total
print(A,c/total)