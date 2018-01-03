# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 14:46:47 2017

@author: potato
"""

import scipy as sp
import numpy as np
import pandas as pd
import tensorflow as tf
import sys,os
sys.path.append(os.path.dirname(__file__))


class DeepNet(object):
    def __init__(self,batch_size):
        '''
        初始化神经网络
            @batch_size: 每次分批处理的数据条数
        '''
        self.batch_size = batch_size
        
        # 初始化
        self.graph = tf.Graph()
        self.define_graph()
        self.session = tf.Session(graph=self.graph)
        self.writer = tf.summary.FileWriter('./board',self.graph)
        

    def _define_model(self):
        '''
        定义模型
        '''
        with tf.name_scope('model'):
            self.W = tf.Variable([.3], dtype=tf.float32,name="W")
            self.b = tf.Variable([-.3], dtype=tf.float32,name="b")
            self.linear_model = self.W*self.x + self.b
        
    def _define_loss_fuction(self):
        '''
        定义损失函数
        '''
        with tf.name_scope('loss'):
            squared_deltas = tf.square(self.linear_model - self.y)
            self.loss = tf.reduce_sum(squared_deltas)
            
    def _define_optimizer(self):
        '''
        定义优化器，其中最简单的就是 梯度下降
        '''
        with tf.name_scope('train'):
            optimizer = tf.train.GradientDescentOptimizer(0.01)
            self.train = optimizer.minimize(self.loss)
        

    def define_graph(self):
        '''
        定义神经网络
        '''
        with self.graph.as_default():
            # define variable
            self.x = tf.placeholder(tf.float32,name="x")
            self.y = tf.placeholder(tf.float32,name="y")
            
            self._define_model()
            
            self._define_loss_fuction()
            
            self._define_optimizer()
            

    
    def test(self):
        '''
        测试神经网络
        '''
        with self.session as sess:
            tf.global_variables_initializer().run() # init constant variables
            for i in range(1000):
                result = sess.run([self.train],feed_dict = {
                        self.x:[1,2,3,4],
                        self.y:[5,3,2,1]
                                  })
            curr_W, curr_b, curr_loss = sess.run([self.W, self.b, self.loss],
                                feed_dict = {
                                        self.x: [1,2,3,4], 
                                        self.y: [5,3,2,1],
                                        })
            print("W: %s b: %s loss: %s"%(curr_W, curr_b, curr_loss))


    



if __name__ == "__main__":


    dn = DeepNet(batch_size = 1000)
    dn.define_graph()
    dn.test()
