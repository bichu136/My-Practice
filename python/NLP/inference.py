import tensorflow as tf 
import tensorflow.keras as keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from nltk.corpus import treebank 
from sklearn.model_selection import train_test_split
from RNN_w2v import create_model
import numpy as np
model = create_model()
model.load_weights('./exp')


data = treebank.tagged_sents()
X = []
Y = []
for sents in data:
    token_sequence =[]
    tag_sequence =[]
    for token in sents:
        token_sequence.append(token[0])
        tag_sequence.append(token[1])
    X.append(token_sequence)
    Y.append(tag_sequence)

# encode X
word_tokenizer = Tokenizer()              # instantiate tokeniser
word_tokenizer.fit_on_texts(X)            # fit tokeniser on data
# use the tokeniser to encode input sequence
X_encoded = word_tokenizer.texts_to_sequences(X)  
# encode Y
tag_tokenizer = Tokenizer()
tag_tokenizer.fit_on_texts(Y)
Y_encoded = tag_tokenizer.texts_to_sequences(Y)


# sequences greater than 100 in length will be truncated
MAX_SEQ_LENGTH = 100
X_padded = pad_sequences(X_encoded, maxlen=MAX_SEQ_LENGTH, padding="pre", truncating="post")
Y_padded = pad_sequences(Y_encoded, maxlen=MAX_SEQ_LENGTH, padding="pre", truncating="post")
# print the first sequence
print(X_padded[0], "\n"*3)
print(Y_padded[0])
X, Y = X_padded, Y_padded

Y = to_categorical(Y)

TEST_SIZE = 0.10
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=TEST_SIZE, random_state=4)
# Re-evaluate the model
# loss, acc = model.evaluate(X_test,Y_test, verbose=2)

input = X_padded[0].reshape((1,100))



print(tag_tokenizer.sequences_to_texts(np.argmax(model.predict(input),axis=2)))
print(tag_tokenizer.sequences_to_texts(Y_padded)[0])