# -*- coding: utf-8 -*-
"""
Created on Thu Dec 07 17:16:50 2017

@author: potato
"""
import pandas as pd
import numpy as np



class Brain(object):
    def __init__(self,possible_actions):
        self.gamma = 0.9 # discount factor
        self.alpha = 0.2# learning rate
        self.epsilon = 0.9 # greedy police
        
        self.possible_actions = possible_actions
        self.len_possible_actions = len(possible_actions)
        self.q_table = pd.DataFrame([],columns=possible_actions)
        
    def _check_action(self,step):
        step = str(step)
        if step not in self.q_table.index:
            self.q_table.loc[step] = np.zeros(self.len_possible_actions)
            
    def choose_action(self,step):
        self._check_action(step)
        if np.random.uniform() > self.epsilon:
            best_action = np.random.choice(self.possible_actions)
        else:
            best_action = self.q_table.loc[str(step),:].idxmax()
        return best_action
    
    def update(self,prestep,nextstep,action,r_or_p):
        print("update fuction not set!")
    


class Qbrain(Brain):
    def update(self,prestep,nextstep,action,r_or_p):
        self._check_action(nextstep)
        self.q_table.loc[str(prestep),action] = \
            self.q_table.loc[str(prestep),action] + self.alpha* \
                (r_or_p + self.gamma*(self.q_table.loc[str(nextstep),:].max()) - \
                 self.q_table.loc[str(prestep),action])
                

class SarsaBrain(Brain):
    def update(self,prestep,nextstep,action,next_action,r_or_p):
        self._check_action(nextstep)
        self.q_table.loc[str(prestep),action] = \
            self.q_table.loc[str(prestep),action] + self.alpha* \
                (r_or_p + self.gamma*(self.q_table.loc[str(nextstep),next_action]) - \
                 self.q_table.loc[str(prestep),action])



class SarsaLambdaBrain(Brain):
    def __init__(self,possible_actions):
        super(SarsaLambdaBrain,self).__init__(possible_actions)
        self.e_table = pd.DataFrame([],columns=possible_actions) # eligibility trace table
        self.lambda_ = 0.8
        
    def _check_action(self,step):
        super(SarsaLambdaBrain,self)._check_action(step)
        step = str(step)
        if step not in self.e_table.index:
            self.e_table.loc[step] = np.zeros(self.len_possible_actions)
    
    def update(self,prestep,nextstep,action,next_action,r_or_p):
        self._check_action(nextstep)
        error = r_or_p + self.gamma*(self.q_table.loc[str(nextstep),next_action]) - \
             self.q_table.loc[str(prestep),action]
        # about eligibility trace
        self.e_table.loc[str(prestep),action] += 1
        self.q_table = self.q_table + self.alpha*self.e_table*error
        self.e_table = self.gamma*self.lambda_*self.e_table
        
    

if __name__ == "__main__":
    qbrain = Qbrain(["left"])
    
    
    
    
    
    
    