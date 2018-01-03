#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 14:24:29 2017

@author: potato


"""

import numpy as np
import pandas as pd
import time
import tkinter as tk

class Environment():
    def __init__(self):
                
        self.map_2d_element = [-1,0,0,0,0,0,0,0,1]
        self.map_2d = range(len(self.map_2d_element))        
        self.map_shape = [len(self.map_2d)]
        self.action = {"forward":1,"backward":-1}
        self.action_num = len(self.action.keys())
        
        # draw a background canvas
        self.window = tk.Tk()
        self.window.geometry("300x300")
        self.window.wm_attributes('-topmost',1)
        canvas_width = 200
        self.canvas = tk.Canvas(self.window,bg="white",height=50,width=canvas_width)
        self.line_split_distance = (canvas_width - 20)/len(self.map_2d_element)
        for start_point in [10+x*self.line_split_distance \
                            for x in range(1,len(self.map_2d_element))]: 
            line = self.canvas.create_line(start_point,0,start_point,50)
        endpoint_position = 1+(len(self.map_2d_element))*self.line_split_distance
        endflag = self.canvas.create_oval(endpoint_position,15,endpoint_position+20,35,fill="red")
    
        self.canvas.pack()
        
        #draw other component
        self.labeltextvar = tk.StringVar()
        self.labeltextvar.set("Hello")
        self.l_instruction_desk = tk.Label(textvariable=self.labeltextvar,bg="yellow",width = canvas_width,
                              height=1)
        self.l_instruction_desk.pack()
        
    def _action_to_distance(self,action):
        if action in self.action.keys():
            action_value = self.action[action]
            x_move_distance = self.line_split_distance*action_value
            return x_move_distance,0
        else:
            raise ValueError("Environment have no such action!")

    
    def feedback(self,position,action):
        # check the action's consequence
        #   r_or_p means rewards or punishments
        #   possible means this action can be done or not
        #   game end means whether the game is end
        #   actual_action means if player really do this action, it actually will how to performed.
        r_or_p = self.map_2d_element[position]
        new_position = position + self.action[action]
        if new_position < 0:
            possible = False
            actual_action = None
        else:
            possible = True
            position = new_position
            actual_action = action
        
        game_end = False
        return position,possible,r_or_p,game_end,actual_action
    

    def environment_show(self,player):
        # main environment entrance
        self.player = player
        location = 10+player.position_now*self.line_split_distance + self.line_split_distance/3
        self.player_image = self.canvas.create_rectangle(
            location,20,location+10,30,fill="blue")
        self.window.after(100, self.main_behavior)
        self.window.mainloop()

    def display_moveplayer_by_action(self):
        action = self.player.actual_action
        if not action:
            x,y=0,0
        else:
            x,y = self._action_to_distance(action)
        self.canvas.move(self.player_image,x,y)
        self.player.actual_action = None # reset player's actual action
        
    def reset_player(self):
        self.player.position_now = 1
        self.canvas.delete(self.player_image)
        location = 10+self.player.position_now*self.line_split_distance + self.line_split_distance/3
        self.player_image = self.canvas.create_rectangle(
            location,20,location+10,30,fill="blue")
        
    def main_behavior(self):
        # this is like main function
        while(True):
            time.sleep(1)
            steps = 0
            while(True):
                time.sleep(0.01)
                state = self.player.play_one_step()
                steps += 1
                self.window.update()
                if state == 1:
                    self.reset_player()
                    break
            print(steps)



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
        position,possible,r_or_p,game_end,actual_action = \
            self.env.feedback(self.position_now,action)
        if do:
            self.position_now = position
            self.actual_action = actual_action
            self.env.display_moveplayer_by_action() # tell player did to environment
           
        return r_or_p,position
    
        
    def play_one_step(self):
        #each step of movement of the player in an environment
        best_action = self.choose_action()
        response,next_position = self.behave(best_action)
        q_predict = self.q_table.ix[self.position_now,best_action]
        if response != 1:
            q_target = response + self.lambda_ * self.q_table.loc[next_position,:].max()
        else:
            q_target = 1
        q_table_ori = self.q_table.ix[self.position_now,best_action]
        self.q_table.ix[self.position_now,best_action] += self.alpha * (q_target - q_predict)
        print("q_table (%s,%s) change from %s to %s"%(self.position_now,best_action,q_table_ori,
              self.q_table.ix[self.position_now,best_action]))
        
        self.behave(best_action,do=True)
        return response       
    

        
        
if __name__ == "__main__":
    env = Environment()
    player = Player(env)
    env.environment_show(player)
            
            

        
        
        

