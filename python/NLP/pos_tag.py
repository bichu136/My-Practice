import re 
import numpy as np
from model import predict    
        

# from nltk.tag.hmm import HiddenMarkovModelTrainer as HMM_Trainer
# trainer = HMM_Trainer()
# tagger = trainer.train_supervised(data)


##getting input for hmm ###
# print(_word_to_index)
symbols=input()
predict(symbols)

# print(tokens)
