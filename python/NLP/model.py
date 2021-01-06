import re 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

class HMM_model():
    def __init__(self,data):        
        self.symbols_set = []
        self.tags_set = []
        for sent in data:
            for token in sent:
                self.symbols_set.append(token[0])
                self.tags_set.append(token[1])

        t = list(np.unique(np.array(self.tags_set))) +["<S>","<E>"]
        self._tag_to_index = {t[i]:i for i in range(len(t)) }
        self._index_to_tag = {i:t[i] for i in range(len(t)) }
        t = list(np.unique(np.array(self.symbols_set))) +["<S>","<E>"]
        self._word_to_index = {t[i]:i for i in range(len(t)) }
        self._index_to_word = {i:t[i] for i in range(len(t)) }
        self.observation_matrix = np.ones((len(self._word_to_index),len(self._tag_to_index)))
        self.change_state_matrix = np.ones((len(self._tag_to_index),len(self._tag_to_index)))

        for sents in data:
            t = [('<S>','<S>')]+sents+[('<E>','<E>')]
            for i in range(len(t)-1):
                self.observation_matrix[self._word_to_index[t[i][0]]][self._tag_to_index[t[i][1]]] +=1
                self.change_state_matrix[self._tag_to_index[t[i][1]]][self._tag_to_index[t[i+1][1]]] +=1
        # self.observation_matrix = np.exp(self.observation_matrix/10000)
        self.observation_matrix =  (self.observation_matrix.T/self.observation_matrix.sum(axis=1)).T
        # self.change_state_matrix = np.exp(self.change_state_matrix/10000)
        self.change_state_matrix = (self.change_state_matrix.T/self.change_state_matrix.sum(axis=1)).T

        self.change_state_matrix[self._tag_to_index["<E>"]] = np.zeros(self.change_state_matrix[self._tag_to_index["<E>"]].shape)
        self.observation_matrix[self._word_to_index["<S>"]] = np.zeros(self.observation_matrix[self._word_to_index["<S>"]].shape)
        self.observation_matrix[self._word_to_index["<S>"]][self._tag_to_index["<S>"]] = 1.0


    def calc_prop(self,next_word,current_prop):
        prop_for_word = self.observation_matrix[self._word_to_index[next_word]]
        w = np.dot(prop_for_word.reshape(-1,1),np.transpose(current_prop).reshape(1,len(current_prop)))
        prop_for_all_tag = np.max(w*self.change_state_matrix,axis=1)
        previous_tags = np.argmax(w*self.change_state_matrix,axis=1)
        previous_tags = [self._index_to_tag[i] for i in previous_tags]
        return prop_for_all_tag,previous_tags


    def predict(self,x):
        
        tokens = ["<S>"] +x + ["<E>"]
        i = 0
        step = []
        prop = [self.observation_matrix[self._word_to_index['<S>']]]
        while i<len(tokens)-2:
            prop_for_all_tags,previous_tags = self.calc_prop(tokens[i+1],prop[-1])
            step.append(previous_tags)
            prop.append(prop_for_all_tags)
            i+=1
        prop.pop(0)
        r = []
        i = len(prop)-1

        r = [(x[i],self._index_to_tag[np.argmax(prop[i])])]
        while(i>0):
            k= step[i][self._tag_to_index[r[0][1]]]
            r = [(x[i-1],k)]+r
            for j in range(len(prop[i])):
                print(self._index_to_tag[j],prop[i][j],step[i][j])
            i-=1
        
        # r=[self._index_to_tag[np.argmax(i)] for i in prop]
        return r






## validation on data train ## 
##         mains            ##
