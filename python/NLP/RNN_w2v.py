import tensorflow as tf 
import tensorflow.keras as keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from nltk.corpus import treebank 
from sklearn.model_selection import train_test_split
word_tokenizer = Tokenizer() 

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
print(Y.shape)
# embedding = 
NUM_CLASSES = Y.shape[2]
# model = keras.Sequential()
EMBEDDING_SIZE  = 300  
VOCABULARY_SIZE = len(word_tokenizer.word_index) + 1
# create architecture
def create_model():
    rnn_model = keras.Sequential()

    # create embedding layer - usually the first layer in text problems
    rnn_model.add(keras.layers.Embedding(input_dim     =  VOCABULARY_SIZE,         # vocabulary size - number of unique words in data
                            output_dim    =  EMBEDDING_SIZE,          # length of vector with which each word is represented
                            input_length  =  MAX_SEQ_LENGTH,          # length of input sequence
                            trainable     =  False                    # False - don't update the embeddings
    ))

    # add an RNN layer which contains 64 RNN cells
    rnn_model.add(keras.layers.SimpleRNN(64, 
                return_sequences=True  # True - return whole sequence; False - return single output of the end of the sequence
    ))

    # add time distributed (output at each sequence) layer
    rnn_model.add(keras.layers.TimeDistributed(keras.layers.Dense(NUM_CLASSES, activation='softmax')))
    # model.fit(X_padded,Y_padded, batch_size=128, epochs=10, validation_data=None)
    rnn_model.compile(loss      =  'categorical_crossentropy',
                    optimizer =  'adam',
                    metrics   =  ['acc'])
    return rnn_model

rnn_model = create_model()
def train_model(model):
# Create a callback that saves the model's weights
    cp_callback = keras.callbacks.ModelCheckpoint(filepath='./exp',
                                                    save_weights_only=True,
                                                    verbose=1)

    rnn_training = model.fit(X_train, Y_train, batch_size=128, epochs=1000,validation_data=(X_test,Y_test),callbacks=[cp_callback])
# train_model(rnn_model)
