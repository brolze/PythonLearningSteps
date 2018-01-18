#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 15:37:30 2018

@author: xujq
"""

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import time

def add_layer(inputs,in_size,out_size,activation_function=None):
    Weights = tf.Variable(tf.random_normal([in_size,out_size]))
    biases = tf.Variable(tf.zeros([1,out_size])+0.1)
    Wx_plus_b = tf.matmul(inputs,Weights)+biases
    if activation_function is None:
        outputs = Wx_plus_b
    else:
        outputs = activation_function(Wx_plus_b)
    return outputs

x_data = np.linspace(-1,1,300)[:,np.newaxis] # add a new dimension
noise = np.random.normal(0,0.05,x_data.shape)
y_data = np.square(x_data) - 0.5 + noise

xs = tf.placeholder(tf.float32,[None,1]) # None means any number of length is ok
ys = tf.placeholder(tf.float32,[None,1])

l1 = add_layer(xs,1,10,tf.nn.relu)
prediction = add_layer(l1,10,1,None)

loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction),
                     reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.scatter(x_data,y_data)
plt.ion()

for i in range(1000):
    sess.run(train_step,feed_dict={xs:x_data,ys:y_data})
    if i%100 == 0:
        try:
            ax.lines.remove(lines[0]) # remove the first line
        except Exception:
            pass   
        print(sess.run(loss,feed_dict={xs:x_data,ys:y_data}))
        prediction_value = sess.run(prediction,feed_dict={xs:x_data,ys:y_data})
        lines = ax.plot(x_data,prediction_value,'r-',lw=5)
        plt.pause(0.1)
        
plt.ioff()
plt.show()


