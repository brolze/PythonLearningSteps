# -*- coding: utf-8 -*-
"""
Created on Thu Dec 07 17:16:50 2017

@author: potato
"""
import pandas as pd
import numpy as np



class Brain():
    def __init__(self,possible_actions):
        print("Hello")
        pass
        
    def _check_action(self,step):
        pass
            
    def choose_action(self,step):
        pass
    
    def update(self,prestep,nextstep,action,r_or_p):
        pass


class Qbrain(Brain):
    def __init__(self,possible_actions):
        self.possible_actions = possible_actions
        self.len_possible_actions = len(possible_actions)
        self.q_table = pd.DataFrame([],columns=possible_actions)
        
        self.lambda_ = 0.5 # discount factor
        self.alpha = 0.1 # learning rate
        self.epsilon = 0.8 # greedy police
        
    def _check_action(self,step):
        step = str(step)
        if step not in self.q_table.index:
            self.q_table.loc[step] = np.random.random(self.len_possible_actions)
            
    def choose_action(self,step):
        self._check_action(step)
        if np.random.uniform() > self.epsilon:
            best_action = np.random.choice(self.possible_actions)
        else:
            best_action = self.q_table.loc[str(step),:].idxmax()
        return best_action
    
    def update(self,prestep,nextstep,action,r_or_p):
        self._check_action(nextstep)

        self.q_table.loc[str(prestep),action] = \
            self.q_table.loc[str(prestep),action] + self.alpha* \
                (r_or_p + self.lambda_*(self.q_table.loc[str(nextstep),:].max() - \
                 self.q_table.loc[str(prestep),action]))





if __name__ == "__main__":
    qbrain = Qbrain(["left"])