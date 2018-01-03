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
from player import Player

class Environment_1d():
    def __init__(self):
        self.map_2d_element = [-1,0,0,0,0,0,0,0,1]
        self.map_2d = range(len(self.map_2d_element))        
        self.map_shape = [len(self.map_2d)]
        self.action = {"forward":1,"backward":-1}
        self.action_num = len(self.action.keys())
        self.player = None
        
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
        new_position = position + self.action[action]
        if new_position <= 0:
            game_end = True
        elif new_position >= len(self.map_2d_element)-1:
            game_end = True
        else:
            game_end = False
        possible = True
        position = new_position
        actual_action = action 
        r_or_p = self.map_2d_element[position]     

        return position,possible,r_or_p,game_end,actual_action

    def make_action(self,action):
        if not action:
            x,y=0,0
        else:
            x,y = self._action_to_distance(action)
        self.canvas.move(self.player_image,x,y)
        
        
    def display_moveplayer_by_action(self,action):
        if action == "reset":
            self.canvas.delete(self.player_image)
            location = 10+self.player.position_now*self.line_split_distance + self.line_split_distance/3
            self.player_image = self.canvas.create_rectangle(
                location,20,location+10,30,fill="blue")
        elif not action:
            x,y=0,0
            self.canvas.move(self.player_image,x,y)
        else:
            x,y = self._action_to_distance(action)
            self.canvas.move(self.player_image,x,y)
        self.player.actual_action = None # reset player's actual action

    def reset_player(self):
        self.player.position_now = 1

    def main_test(self):
        self.operator_frame = tk.Frame(height = 100,width = 400)
        self.operator_frame.pack()
        b_left = tk.Button(self.operator_frame,text="left",
                           command=lambda:self.player.behave("backward",do=True))
        b_left.pack(side="left")
        b_right = tk.Button(self.operator_frame,text="right",
                           command=lambda:self.player.behave("forward",do=True))
        b_right.pack(side="right")

        
    def main_behavior(self):
        # this is like main function
        while(True):
            time.sleep(1)
            steps = 0
            while(True):
                time.sleep(0.1)
                state = self.player.play_one_step()
                steps += 1
                self.window.update()
                if state == 1:
                    self.reset_player()
                    break
            
    def environment_show(self,test=False):
        # main environment entrance
        if not self.player:
            print("Didn't init player!")
            return
        location = 10+player.position_now*self.line_split_distance + self.line_split_distance/3
        self.player_image = self.canvas.create_rectangle(
            location,20,location+10,30,fill="blue")
        if test:
            self.window.after(100, self.main_test)
        else:
            self.window.after(100, self.main_behavior)
        self.window.mainloop()
        

        
if __name__ == "__main__":
    env1d = Environment_1d()
    player = Player(env1d)
    env1d.environment_show(test=False)
    
