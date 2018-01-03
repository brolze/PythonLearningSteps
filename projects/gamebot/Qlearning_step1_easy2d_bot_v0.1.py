#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 14:24:29 2017

@author: potato


"""

import numpy as np
import pandas as pd
import time


class Environment():
    def __init__(self):
        self.map_2d_element = [0,0,0,0,0,0,0,1]
        self.map_2d = range(len(self.map_2d_element))        
        self.map_shape = [len(self.map_2d)]
        self.action = {"forward":1,"backward":-1}
        self.action_num = len(self.action.keys())
        
    def environment_show(self,players):
        show_str = ""
        for bit in self.map_2d_element:
            if bit == 0:
                show_str += "_"
            elif bit == 1:
                show_str += "T"

        player = players[0] # only one player
        p = player.position_now
        show_str = show_str[:p] + player.name + show_str[p+1:]
        print(show_str)            
         
        return show_str
    
    def check_reward(self,position):
        return self.map_2d_element[position]

class Player():
    def __init__(self,env):
        self.env = env
        self.position_now = 1  
        self.name = "o"
        self.lambda_ = 0.5 # discount factor
        self.alpha = 0.1 # learning rate
        self.epsilon = 0.9 # greedy police
        self.possible_actions = list(env.action.keys())
        
        q_table_d = env.map_shape + [env.action_num] 
        self.q_table = np.random.random(q_table_d)
        self.q_table = pd.DataFrame(self.q_table,\
            index=env.map_2d,columns=env.action.keys())
        
    def behave(self,action,do=False):
        position  = self.position_now + self.env.action[action]
        if position < 0:
            position = 0
        if do:
            self.position_now = position
        
        reward = self.env.check_reward(position)
        return reward,position
    
    def choose_action(self):
        if np.random.uniform() > self.epsilon:
            best_action = np.random.choice(self.possible_actions)
        else:
            best_action = self.q_table.loc[self.position_now,:].idxmax()
        return best_action
        
    def play_one_round(self):
        action = self.choose_action()
        response,next_position = player.behave(action)
        q_predict = self.q_table.ix[self.position_now,action]
        if response == 0:
            q_target = response + self.lambda_ * self.q_table.loc[next_position,:].max()
        else:
            q_target = 1
        self.q_table.ix[self.position_now,action] += self.alpha * (q_target - q_predict)
        self.behave(action,do=True)
        
        return response
        
        
if __name__ == "__main__":
    env = Environment()
    player = Player(env)
    
    action = player.choose_action()
    player.behave(action)
    while(True):
        steps = 0
        while(True):
            state = player.play_one_round()
            steps += 1
            env.environment_show([player])
            time.sleep(0.05)
            if state == 1:
                player.position_now=1
                break
        print(steps)
            
            

        
        
        

