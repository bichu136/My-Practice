import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
class ONotationPredictor:
    def __call__(self, x):
        # self.w_logn * tf.math.log(x) + 
        return (self.w_sqr_n * tf.square(x))+self.b+ (self.w_nlgn * (tf.math.log(x)*x))
        # self.w_n * x +self.b + self.w_sqrt_n * tf.math.sqrt(x) + 

    def __init__(self):
        self.w_logn = tf.Variable(11.0,trainable=True)
        self.w_sqrt_n = tf.Variable(11.0,trainable=True,name="w_sqrt_n")
        self.w_n = tf.Variable(11.0,trainable=True,name="w_n")
        self.w_nlgn = tf.Variable(11.0,trainable=True,name="w_nlgn")
        self.w_sqr_n = tf.Variable(11.0,trainable=True,name="w_sqr_n")
        self.w_cube_n = tf.Variable(11.0,trainable=True)
        self.b = tf.Variable(12.0,trainable=True,name="b")
def loss(y, pred):
    return tf.reduce_mean(tf.square(y - pred))

def train(linear_model,x,y,lr=0.00001):
    with tf.GradientTape() as t:
        current_loss = loss(y, linear_model(x))
    print(current_loss.numpy())
    # lr_weight, lr_bias,lr_w_nlgn,lr_w_sqrt_n,
    lr_w_sqr_n,lr_b,lr_w_nlgn = t.gradient(current_loss, [linear_model.w_sqr_n,linear_model.b,linear_model.w_nlgn])
    # linear_model.w_n, linear_model.b,linear_model.w_nlgn,linear_model.w_sqrt_n,
    print(lr_b.numpy(),lr_w_sqr_n.numpy(),lr_w_nlgn)
    # linear_model.w_n.assign_sub(lr * lr_weight)
    linear_model.b.assign_sub(lr * lr_b)
    # linear_model.w_nlgn.assign_sub(lr*lr_w_nlgn)
    # linear_model.w_sqrt_n.assign_sub(lr*lr_w_sqrt_n)
    linear_model.w_sqr_n.assign_sub(lr*lr_w_sqr_n)
def scale_range (input, min, max):
    input += -(np.min(input))
    input /= np.max(input) / (max - min)
    input += min
    return input

O_notation_predictor = ONotationPredictor()
x=np.array([int(i) for i in open('n.txt').read().split()],dtype=np.float32)
y=np.array([int(i) for i in open('y.txt').read().split()],dtype=np.float32)
x = scale_range(x,0,100)
y = scale_range(y,0,100)
plt.scatter(x,y)
plt.show()
# weights =[]
# biases = [] 
epoch = 80
learning_rate=0.12
for epoch_count in range(epoch):
    # weights.append({
    #                 "a": O_notation_predictor.w_logn.numpy(),
    #                 "b":O_notation_predictor.w_sqrt_n.numpy()
    #                 })
    # biases.append()
    real_loss =tf.reduce_mean(tf.square(y,O_notation_predictor(x)))
    train(O_notation_predictor,x,y,learning_rate)
    print(f"Epoch count {epoch_count}: Loss value: {real_loss.numpy()}")


