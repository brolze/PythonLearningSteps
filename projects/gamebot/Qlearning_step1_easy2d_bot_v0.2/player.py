# -*- coding: utf-8 -*-
"""
Created on Wed Dec 06 17:18:54 2017

@author: potato
"""
import numpy as np
import pandas as pd
import time
import tkinter as tk
import sys
import os
sys.path.append(os.path.dirname(__file__))

from brain import Qbrain


#class Player_1d():
#    def __init__(self,env):
#        self.env = env
#        self.env.player = self
#        self.position_now = 1  
#        self.lambda_ = 0.5 # discount factor
#        self.alpha = 0.1 # learning rate
#        self.epsilon = 0.9 # greedy police
#        self.possible_actions = list(env.action.keys())
#        self.game_end = False
#        
#        q_table_d = env.map_shape + [env.action_num] 
#        self.q_table = np.random.random(q_table_d)
#        self.q_table = pd.DataFrame(self.q_table,\
#            index=env.map_2d,columns=env.action.keys())
#    
#    def choose_action(self):
#        # choose action base on q_table or random
#        if np.random.uniform() > self.epsilon:
#            best_action = np.random.choice(self.possible_actions)
#        else:
#            best_action = self.q_table.loc[self.position_now,:].idxmax()
#        return best_action
#
#    
#    def behave(self,action,do=False):
#        # base on action, choose to do the action or not.
#        #   action result will be feedback by the environment
#        
#        if self.game_end: # if game already end, reset the game 
#            self.env.reset_player()
#            actual_action = "reset"
#            self.env.display_moveplayer_by_action(actual_action) # tell player did to environment
#            self.game_end = False
#            return None
#        
#        position,possible,r_or_p,game_end,actual_action = \
#            self.env.feedback(self.position_now,action)
#        if do:
#            self.position_now = position
#            self.env.display_moveplayer_by_action(actual_action) # tell player did to environment
#            self.game_end = game_end
#
#        return r_or_p,position
#    
#        
#    def play_one_step(self):
#        #each step of movement of the player in an environment
#        if self.game_end:
#            self.behave(None)
#        else:
#            best_action = self.choose_action()
#            response,next_position = self.behave(best_action)
#            q_predict = self.q_table.ix[self.position_now,best_action]
#            q_target = response + self.lambda_ * self.q_table.loc[next_position,:].max()
#            q_table_ori = self.q_table.ix[self.position_now,best_action]
#            self.q_table.ix[self.position_now,best_action] += self.alpha * (q_target - q_predict)
#            print("q_table (%s,%s) change from %s to %s"%(self.position_now,best_action,q_table_ori,
#                  self.q_table.ix[self.position_now,best_action]))
#        
#            self.behave(best_action,do=True)
#            return response
        
        
class Player_2d():
    def __init__(self,env):
        self.env = env
        self.env.player = self
        self.position_now = (0,0) 
        self.possible_actions = list(env.actions.keys())
        self.game_end = False
        self.brain = Qbrain(self.possible_actions)
        

    
    def choose_action(self):
        # choose action base on q_table or random
        if np.random.uniform() > self.epsilon:
            best_action = np.random.choice(self.possible_actions)
        else:
            best_action = self.q_table.loc[self.position_now,:].idxmax()
        return best_action

    
    def behave(self,action,do=False):
        # base on action, choose to do the action or not.
        #   action result will be feedback by the environment
        
        if self.game_end: # if game already end, reset the game 
            self.env.reset_player()
            actual_action = "reset"
            self.env.display_moveplayer_by_action(actual_action) # tell player did to environment
            self.game_end = False
            return None
        
        position,r_or_p,game_end,actual_action = \
            self.env.feedback(self.position_now,action)
        if do:
            self.position_now = position
            self.env.display_moveplayer_by_action(actual_action) # tell player did to environment
            self.game_end = game_end

        return r_or_p,position
    
        
    def play_one_step(self):
        #each step of movement of the player in an environment
        if self.game_end:
            self.behave(None)
        else:
            best_action = self.brain.choose_action(self.position_now)
            response,next_position = self.behave(best_action)
            self.brain.update(
                    self.position_now,next_position,best_action,response)
            self.behave(best_action,do=True)
            return response