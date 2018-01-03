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

from brain import Qbrain,SarsaBrain,SarsaLambdaBrain
        
class Player_2d():
    def __init__(self,env):
        self.env = env
        self.env.player = self
        self.position_now = (0,0) 
        self.possible_actions = list(env.actions.keys())
        self.game_end = False
#        self.brain = Qbrain(self.possible_actions)
#        self.brain = SarsaBrain(self.possible_actions)
        self.brain = SarsaLambdaBrain(self.possible_actions)
        self.brain._check_action(self.position_now)
        
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
        
    def play_one_step_qlearning(self):
        #each step of movement of the player in an environment
        if self.game_end:
            self.behave(None)
            return 0
        else:
            best_action = self.brain.choose_action(self.position_now)
            response,next_position = self.behave(best_action)
            self.brain.update(
                    self.position_now,next_position,best_action,response)
            self.behave(best_action,do=True)
            return response
        
    def play_one_step_sarsa(self,action=None):
        #each step of movement of the player in an environment
        if self.game_end:
            self.behave(None)
            return 0,None
        else:
            if not action:
                best_action = self.brain.choose_action(self.position_now)
            else:
                best_action = action
            previous_position = self.position_now # remember position
            response,next_position = self.behave(best_action,do=True)
                # choose again after one step
            next_best_action = self.brain.choose_action(self.position_now)
            self.brain.update(previous_position,self.position_now,
                              best_action,next_best_action,response)
            return response,next_best_action
        
    def play_one_step_sarsa_lambda(self,action=None):
        #each step of movement of the player in an environment
        if self.game_end:
            self.behave(None)
            return 0,None
        else:
            if not action:
                best_action = self.brain.choose_action(self.position_now)
            else:
                best_action = action
            previous_position = self.position_now # remember position
            response,next_position = self.behave(best_action,do=True)
                # choose again after one step
            next_best_action = self.brain.choose_action(self.position_now)
            self.brain.update(previous_position,self.position_now,
                              best_action,next_best_action,response)
            
            return response,next_best_action
        
        