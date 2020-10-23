import tensorflow as tf
import numpy as np
model = tf.keras.Sequential()
def read_data(filename):
    r = []
    with open(filename) as file:
        line =file.readline() 
        while(line!=""):
            r.append([float(i) for i in line.split(",")])
            line = file.readline()
    return np.array(r)
def scale_range (input, min, max):
    input += -(np.min(input))
    input /= np.max(input) / (max - min)
    input += min
    return input
def scale_range (input, min, max):
    input += -(np.min(input))
    input /= np.max(input) / (max - min)
    input += min
    return input
x =read_data('input.csv')
y =read_data('y_pred.csv')
scale_range(x,0,1)
scale_range(y,0,1)
model.add(tf.keras.layers.Dense(1,use_bias=True,input_shape=(5,)))
model.compile(loss='mse',optimizer='adam')
log_dir = "logs/fit/"
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

model.fit(x,y,epochs=1000,batch_size=75,callbacks=[tensorboard_callback])
print(model.get_weights())

