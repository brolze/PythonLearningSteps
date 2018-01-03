# -*- coding: utf-8 -*-
"""
Created on Wed Dec 06 16:32:25 2017

@author: potato
"""

import numpy as np
import pandas as pd
import time
import tkinter as tk
import sys
import os
sys.path.append(os.path.dirname(__file__))
from player import *

class Environment_2d():
    def __init__(self):
        # init reward map matrix
        self.map_2d_element = pd.DataFrame(np.zeros([6,6]))
        self.map_2d_element.iloc[3,3] = 1
        self.map_2d_element.iloc[3,2] = -1
        self.map_2d_element.iloc[2,3] = -1
        self.map_2d_element.iloc[4,3] = -1
             
        self.map_shape = self.map_2d_element.shape
        self.actions = {"right":(1,0),"left":(-1,0),"up":(0,-1),"down":(0,1)}
        self.action_num = len(self.actions.keys())
        self.player = None
        
        # draw a background canvas
        self.window = tk.Tk()
        self.window.geometry("500x500")
        self.window.wm_attributes('-topmost',1)
        self.canvas = tk.Canvas(self.window,bg="white",height=200,width=200)
        self.x_split_distance = (200 - 20)/self.map_shape[0] # x distance between cages  
        self.y_split_distance = (200 - 20)/self.map_shape[1] # y distance between cages
        for start_point in [10+x*self.x_split_distance \
                            for x in range(0,self.map_shape[0]+1)]: 
            line = self.canvas.create_line(start_point,10,start_point,190)
        for start_point in [10+y*self.y_split_distance \
                            for y in range(0,self.map_shape[1]+1)]: 
            line = self.canvas.create_line(10,start_point,190,start_point)
       
        self.squaresize = (self.x_split_distance-6,self.y_split_distance-6)
        for x,row in self.map_2d_element.iterrows():
            for y,item in row.iteritems():
                if item == 1:
                    treasure = self.canvas.create_rectangle(
                            10+self.x_split_distance*x+3,
                            10+self.y_split_distance*y+3,
                            10+self.x_split_distance*x+3+self.squaresize[0],
                            10+self.y_split_distance*y+3+self.squaresize[1],
                            fill="yellow"
                            )
                elif item == -1:
                    hole = self.canvas.create_rectangle(
                            10+self.x_split_distance*x+3,
                            10+self.y_split_distance*y+3,
                            10+self.x_split_distance*x+3+self.squaresize[0],
                            10+self.y_split_distance*y+3+self.squaresize[1],
                            fill="black"
                            )
                else:
                    pass
                
        self.player_image = None # init player's image
        
        self.canvas.pack()
    
    

    def _displaytool_action_to_distance(self,action):
        if action in self.actions.keys():
            action_value = self.actions[action]
            x_move_distance = self.x_split_distance*action_value[0]
            y_move_distance = self.y_split_distance*action_value[1]
            return x_move_distance,y_move_distance
        else:
            raise ValueError("Environment have no such action!")

    def display_moveplayer_by_action(self,action):
        if action == "reset":
            if self.player_image: # if have player's image, delete player's image
                self.canvas.delete(self.player_image)

            p_position = self.player.position_now
            self.playersize = (self.x_split_distance-10,self.y_split_distance-10)
            self.player_image = self.canvas.create_oval(
                    10 + self.x_split_distance*p_position[0] + 5,
                    10 + self.y_split_distance*p_position[1] + 5,
                    10 + self.y_split_distance*p_position[0] + 5 + self.playersize[0],
                    10 + self.y_split_distance*p_position[1] + 5 + self.playersize[1],
                    fill="blue")
        elif not action:
            x,y=0,0
            self.canvas.move(self.player_image,x,y)
        else:
            x,y = self._displaytool_action_to_distance(action)
            self.canvas.move(self.player_image,x,y)
        self.player.actual_action = None # reset player's actual action
        
    
    def _tool_add(self,a,b):
        # (new_x,new_y) = (x,y) + (_x,_y)
        new_x = a[0] + b[0]
        new_y = a[1] + b[1]
        return (new_x,new_y)
        
    def feedback(self,position,action):
        # check the action's consequence, maybe dead? hit the wall? or other
        #   r_or_p means rewards or punishments
        #   possible means this action can be done or not
        #   game end means whether the game is end
        #   actual_action means if player really do this action, it actually will how to performed.
        #       actual_action only use to display

        new_position = self._tool_add(position,self.actions[action])
        if new_position[0] < 0 or new_position[1] < 0 or \
            new_position[0] > self.map_shape[0]-1 or \
            new_position[1] > self.map_shape[1]-1: 
            # if hit the wall
            game_end = False
            actual_action = None
        elif self.map_2d_element.iloc[new_position] != 0:
            if self.map_2d_element.iloc[new_position] == -1:
                print("dead!")
            elif self.map_2d_element.iloc[new_position] == 1:
                print("win!")
            game_end = True
            actual_action = action
            position = new_position
        else:
            game_end = False
            position = new_position
            actual_action = action 
        r_or_p = self.map_2d_element.iloc[position]
        
        return position,r_or_p,game_end,actual_action
        
        
    def make_action(self,action):
        pass


    def reset_player(self):
        self.player.position_now = (0,0)

    def main_test(self):
        # init test environment
        operator_frame_1 = tk.Frame()
        operator_frame_1.pack()
        b_up = tk.Button(operator_frame_1,text="up",
                           command=lambda:self.player.behave("up",do=True))
        b_up.pack()
        operator_frame_2 = tk.Frame()
        operator_frame_2.pack()
        b_left = tk.Button(operator_frame_2,text="left",
                           command=lambda:self.player.behave("left",do=True))
        b_left.pack(side="left")
        b_right = tk.Button(operator_frame_2,text="right",
                           command=lambda:self.player.behave("right",do=True))
        b_right.pack(side="right")
        operator_frame_3 = tk.Frame()
        operator_frame_3.pack()
        b_down = tk.Button(operator_frame_3,text="down",
                           command=lambda:self.player.behave("down",do=True))
        b_down.pack()
        
        
    def main_behavior(self):
        # this is like main function
        while(True):
            time.sleep(1)
            steps = 0
            global best_action
            best_action = None # if start,then set to None
            while(True):
                time.sleep(0.01)
#                state = self.player.play_one_step_qlearning()
#                state,best_action = self.player.play_one_step_sarsa(best_action)
                state,best_action = self.player.play_one_step_sarsa_lambda(best_action)
                steps += 1
                self.window.update()
                if state != 0:
                    print("total steps (%i)."%steps)
                    self.reset_player()
                    break
            
    def environment_show(self,test=False):
        # main environment entrance
        if not self.player:
            print("Didn't init player!")
            return
        self.display_moveplayer_by_action("reset") # first time need to initialize player's image

        if test:
            self.window.after(100, self.main_test)
        else:
            self.window.after(100, self.main_behavior) # after 100ms run this function

        self.window.mainloop()
    


        
if __name__ == "__main__":
    env2d = Environment_2d()
    player = Player_2d(env2d)
    env2d.environment_show(test=False)
    
