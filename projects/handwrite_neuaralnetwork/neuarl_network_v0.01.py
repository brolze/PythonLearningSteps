# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 16:22:37 2017

@author: potato

v0.01 #只包含run方法111111
"""

import numpy as np

class Perceptron(object):
    '''
    感知机类
    '''
    def __init__(self):
        pass

    def sigmoid(self,z):
        """
        sigmoid 函数实现
        """
        return 1.0/(1.0+np.exp(-z))
    
    def activate(self,wx,bias):
        return self.sigmoid(wx-bias)

class Layer(object):
    '''
    层类
    '''
    def __init__(self,node_num,feature_num):
        self.weight = np.random.random((node_num,feature_num)) #初始化 权
        self.layer_nodes = Perceptron()
        
        
    def run(self,input_):
        cal_result = np.dot(self.weight,input_)
        activate_fuction_v = np.vectorize(self.layer_nodes.sigmoid) # 把sigmoid函数 vector化
        activate_result = activate_fuction_v(cal_result)
        return activate_result
        
        
    def update(self):
        pass
    

class Network(object):
    '''
    神经网络
    '''
    
    def __init__(self,X,y,hidden=[10]):
        '''
        @hidden : 列表。 [5,3] 代表2个隐藏层，第一个5个节点，第二个3个节点
            hidden 暂时不可用，先写死在代码里了
        
        '''
        self.X = X
        self.y = y
        Xshape = X.shape
        yshape = y.shape
        
        self.layer1 = Layer(node_num=5,feature_num=Xshape[0])
        self.layer2 = Layer(node_num=y.shape[0],feature_num=5) #假设只有1个隐藏层
        
    def run(self):
        self.l1_result = self.layer1.run(self.X)
        self.l2_result = self.layer2.run(self.l1_result)
        return self.l2_result




if __name__ == "__main__":
#    X = np.array([
#            [1.0,1.5],
#            [2.0,2.5],
#            [3.0,3.5],
#            [4.0,4.5],
#            [5.0,5.5],
#            ])
    X = np.array([1.0,1.5])
    X = X.T
    
    # y先假设是分类问题，每个y相当于被分为0类和1类
#    y = np.array([
#            [1.0,0.0],
#            [1.0,0.0],
#            [0.0,1.0],
#            [0.0,1.0],
#            [0.0,1.0],
#            ])
    y = np.array([1.0,0.0])
    y = y.T
    
    nn = Network(X,y)
    result = nn.run()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    