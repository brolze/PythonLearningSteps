# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 14:46:47 2017

@author: potato

V0.03:
    # 实现一个精确度的判别函数

"""

import scipy.io as spio
import numpy as np
import pandas as pd
import tensorflow as tf
import sys,os
sys.path.append(os.path.dirname(__file__))


class DeepNet(object):
    def __init__(self):
        '''
        初始化神经网络
        '''
        # 初始化
        self.graph = tf.Graph()
        self.define_graph() # 先定义graph (为了清晰只包括了运算流程中用的函数)
        self.define_other() # 定义其他工具函数
        self.session = tf.Session(graph=self.graph)
        self.writer = tf.summary.FileWriter('./board',self.graph) # 展示graph
        
    def _define_variable(self):
        '''
        定义变量
        '''
        self.x = tf.placeholder(tf.float32,name="x")
        self.y = tf.placeholder(tf.float32,name="y")
        
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
            self._define_variable() #定义变量           
            self._define_model() #定义模型            
            self._define_loss_fuction() #定义损失函数            
            self._define_optimizer() #定义优化器

    def _define_model_evaluation(self):
        '''
        定义模型评价函数,需要子类定义
        '''
        print('no model evaluation fuction been defined.')

    def define_other(self):
        '''
        定义其他函数
        '''
        with self.graph.as_default():
            self._define_model_evaluation() #定义模型评价函数


            
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


class DeepNetDigitalGraphLearn(DeepNet):
    def __init__(self,batch_size,hiddenlevel_nodecount,num_labels):
        self.batch_size = batch_size
        self.hiddenlevel_nodecount = hiddenlevel_nodecount
        self.num_labels = num_labels
        print("super initing...")
        super(DeepNetDigitalGraphLearn,self).__init__()
    
    @staticmethod
    def batch_load(imgdata,labels,batch_size,num_labels):
        '''
        切分数据集，切成 batch size 的迭代器
        '''
        if imgdata.shape[-1] != len(labels):
            raise Exception('Length of samples and labels must equal')
        start_step = 0
        i = 0 # batch number counter
        while start_step<len(labels):
            next_step = start_step + batch_size
            if next_step > len(labels):
                break
            # 返回编号，batch数据，batch labels
            yield i,imgdata[:,:,:,start_step:next_step],\
                DeepNetDigitalGraphLearn.y_encoder(labels[start_step:next_step],num_labels)
            i+=1
            start_step = next_step
            
    @staticmethod
    def y_encoder(labels,num_labels):
        encode_y = []
        for i in labels:
            i = i[0]%num_labels #由于数据因素，这里对10取余数
            new_element = np.zeros(num_labels)
            new_element[i]=1
            encode_y.append(new_element)
        encode_y = np.array(encode_y)
        return encode_y
            
    def _define_variable(self):
        '''
        重定义 定义变量函数 
        '''
        self.train_batch_x = tf.placeholder(tf.float32, #类型
            shape = (
                    32, #长
                    32, #款
                    3, #像素
                    self.batch_size #每组大小
                    ),name="x_train_batch")
        self.train_batch_y = tf.placeholder(tf.float32, #类型
            shape = (
                    self.batch_size, #每组大小
                    self.num_labels,
                    ),name="y_train_batch")
        
    def _define_model(self):
        '''
        重定义 定义函数
        '''
        with tf.name_scope('fc1'):
            fc1_weight = tf.Variable(
                tf.truncated_normal([32*32*3,self.hiddenlevel_nodecount], stddev=0.1),
                name = "fc1_weights")
            fc1_biases = tf.Variable(
                tf.constant(0.1, shape=[self.hiddenlevel_nodecount]),
                name = "fc1_biases")
        
        with tf.name_scope('fc2'):
            fc2_weight = tf.Variable(
                tf.truncated_normal([self.hiddenlevel_nodecount,self.num_labels], stddev=0.1),
                name = "fc2_weights")
            fc2_biases = tf.Variable(
                tf.constant(0.1, shape=[self.num_labels]),
                name = "fc2_biases")
        
        def model_calculation(data):
            reshape_data = tf.reshape(data,(32*32*3,self.batch_size))
            reshape_data = tf.transpose(reshape_data) #为了后面的矩阵运算进行转置
            # fully connected layer 1
            with tf.name_scope('fc1_model'):
                fc1_model = tf.matmul(reshape_data,fc1_weight) + fc1_biases
                hidden = tf.nn.relu(fc1_model)
           # fully connected layer 2
            with tf.name_scope('fc2_model'):
                return tf.matmul(hidden, fc2_weight) + fc2_biases
            
        self.model = model_calculation(self.train_batch_x)
        
    def _define_loss_fuction(self):
        '''
        重定义 损失函数
        '''
        with tf.name_scope('loss'):
            self.loss = tf.reduce_mean(
                tf.nn.softmax_cross_entropy_with_logits(logits=self.model,
                    labels=self.train_batch_y)
            )
            tf.summary.scalar('Loss', self.loss) #增加一个可视化的summary
            
    def _define_optimizer(self):
        '''
        重定义 优化器，其中最简单的就是 梯度下降
        '''
        with tf.name_scope('optimizer'):
            optimizer = tf.train.GradientDescentOptimizer(0.01)
            self.train = optimizer.minimize(self.loss) # 训练的过程就是用优化器最小误差

    def _define_model_evaluation(self):
        '''
        定义模型评价函数,需要子类定义
        '''
        # Predictions for the training, validation, and test data.
        with tf.name_scope('predictions'):
            self.prediction = tf.nn.softmax(self.model, name='prediction')
        
#        with tf.name_scope('model_evaluation'):
##            ypred = self.model
##            ytrue = self.train_batch_y
#            def accuracyfunc(ypred,ytrue):
#                y_matrix = ypred == ytrue
#                true_false = np.apply_along_axis(lambda x: np.all(x),1,y_matrix)
#                accuracy = np.asarray(np.unique(true_false,return_counts=True)).T
#                return accuracy
#            self.accuracy = accuracyfunc(self.model,self.train_batch_y)
            
    def test(self,imgdata,labels):
        '''
        重定义 测试函数
        '''
        print("test start!")
        with self.session as sess:
            tf.global_variables_initializer().run() # init constant variables
            for i,batch_imgdata,batch_label in self.batch_load(imgdata,labels,
                                            self.batch_size,self.num_labels):
                result = sess.run([
                            self.train,
                            self.loss,
                            self.prediction,
                        ],feed_dict={
                            self.train_batch_x : batch_imgdata,
                            self.train_batch_y : batch_label,
                        })
                print(result)
        return result
        
    
            


if __name__ == "__main__":

    train_raw = spio.loadmat("../../demo_withnote/tfgirls/data/train_32x32.mat")
#    test_raw = spio.loadmat("../../demo_withnote/tfgirls/data/test_32x32.mat")
#    extra_raw = spio.loadmat("../../demo_withnote/tfgirls/data/extra_32x32.mat")
    
    dn = DeepNetDigitalGraphLearn(batch_size = 1000,hiddenlevel_nodecount = 100,
                                  num_labels = 10)
    result_sample = dn.test(train_raw['X'],train_raw['y'])



#    dn = DeepNet()
#    dn.define_graph()
#    dn.test()
