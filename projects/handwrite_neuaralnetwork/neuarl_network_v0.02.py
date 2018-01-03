# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 16:22:37 2017

@author: potato

v0.02   #实现loss fuction
        #实现基于loss function 的前反馈机制
        #已完成简单的收敛过程
        
误差函数的输入是权w，输出是误差E，优化就是对这个函数求导。

注： 符号系统使用 西瓜书 的


"""

import numpy as np


'''
#随便走一条路试试
tmpx = np.random.random((5,1)) #随机x ， 5个随机数
tmpw = np.random.random((2,5)) #随机w ，映射到2个y，
tmpy = np.array([[0.0,1.0]]).T #假设正确的是应该预测为 1

ypred = np.dot(tmpw,tmpx)
error = ypred - tmpy

# 假设是找 w_jh 的权变化量， 其中 j=1,h=3 ,对应的变应该是 Sig(w_jh * x_h) = y_j 
j = 1 ; h = 3
theta_whj_betaj = tmpx[h] # w_hj 对 beta_j 求导数，得到的就是 x相应节点的值。
theta_hatyj_betaj = ypred[j]*(1-ypred[j]) # beta_j 对 haty_j 求导数，根据sigmod函数是这个值
theta_Ek_hatyj = error[j] # Error 对 haty_j 求导，求导后就是相应的Error值
delta_whj = theta_whj_betaj*theta_hatyj_betaj*theta_Ek_hatyj

'''


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
        self.bias = np.ones((node_num,1))
        self.layer_nodes = Perceptron() #暂时只用到了激活函数，所有只声明了一个节点，调用下方法
        
        
    def run(self,input_):
        self.cal_result = np.dot(self.weight,input_)
        self.cal_result = self.cal_result.reshape((len(self.cal_result),1))
        activate_fuction_v = np.vectorize(self.layer_nodes.sigmoid) # 把sigmoid函数 vector化
        input_of_sigmoid = self.cal_result+self.bias
        activate_result = activate_fuction_v(input_of_sigmoid)
        activate_result = activate_result.reshape((len(activate_result),1))
        return activate_result
        
        
    

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
        self.learning_rate = 0.2
        
        self.layer1 = Layer(node_num=5,feature_num=X.shape[0])
        self.layer2 = Layer(node_num=y.shape[0],feature_num=5) #假设只有1个隐藏层
       
    def loss(self):
        loss = ((self.l2_result - self.y)**2).sum()
        return loss


    def _partial_E_yhat(self):
        p1 = y_hat - y 

    def optimizer(self):
        #优化器，即对损失函数求导
        pass

    def run(self):
        self.l1_result = self.layer1.run(self.X)
        self.l2_result = self.layer2.run(self.l1_result)
        loss = self.loss()
        return self.l2_result,loss
    
    def train(self):
        for i in range(100):
            y_hat,loss = self.run() # 求输出 \hat{y}
            print("%i rount,now loss is %.2f"%(i,loss))
            
            gj = y_hat*(1-y_hat)*(self.y - y_hat) # gj 其实是指第j个元素的某种误差
            eh = np.dot(self.layer2.weight.T,gj)* self.l1_result*(1-self.l1_result)
            
            # 更新 layer2 的 weight
            delta_w = np.dot(gj,self.l1_result.T)
            self.layer2.weight = self.layer2.weight + self.learning_rate*delta_w
            
            # 更新 layer2 的 bias
            self.layer2.bias = self.layer2.bias - self.learning_rate*gj
            
            # 更新 layer1 的 weight
            self.layer1.weight = self.layer1.weight + self.learning_rate*np.dot(eh,self.X.T)

            # 更新 layer1 的 bias
            self.layer1.bias = self.layer1.bias - self.learning_rate*eh
            

if __name__ == "__main__":
#    X = np.array([
#            [1.0,1.5],
#            [2.0,2.5],
#            [3.0,3.5],
#            [4.0,4.5],
#            [5.0,5.5],
#            ])
    X = np.array([1.0,1.5]).reshape((1,2))
    X = X.T
    
    # y先假设是分类问题，每个y相当于被分为0类和1类
#    y = np.array([
#            [1.0,0.0],
#            [1.0,0.0],
#            [0.0,1.0],
#            [0.0,1.0],
#            [0.0,1.0],
#            ])
    y = np.array([1.0,0.0]).reshape(2,1)
    
    nn = Network(X,y)
    y_hat,loss = nn.run()
#    nn.train()
    nn.train()

    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    