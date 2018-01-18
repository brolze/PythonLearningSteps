#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 19:13:11 2018

@author: xujq
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

'''
read a image and show and save
'''
if False:

    img = cv2.imread("girl1.jpeg",cv2.IMREAD_GRAYSCALE) # also use 0 is ok
        # also count be cv2.IMREAD.COLOR (also is 1) , cv2.IMREAD_UNCHANGED (-1)
    cv2.imshow('image',img)
    cv2.waitKey(0) # wait any key
    cv2.destroyAllWindows()
    
    plt.imshow(img,cmap="gray",interpolation='bicubic')
    plt.plot([50,100],[80,100],'c',linewidth=5) # could also write other things
    plt.show()
    
    # save image
    cv2.imwrite("save.png",img)
    
'''
read a video and show and save
'''
if False:
    cap = cv2.VideoCapture(0) # camera of your computer, if replace 0 to vedio name then load from file
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))
    while True:
        ret,frame = cap.read()
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        out.write(frame)
        cv2.imshow('frame',frame)
        cv2.imshow('gray',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'): # wait for key 'q'
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    

'''
draw some shapes
'''            
if False:
    img = cv2.imread("girl1.jpeg",cv2.IMREAD_COLOR)
    
    cv2.line(img,(0,0),(150,150),(255,0,0),15) # blue green red
    cv2.rectangle(img,(15,25),(200,150),(0,255,0),5) # last one parm is line width
    cv2.circle(img,(100,63),55,(0,0,255),-1) # -1 means fill in the circle
    
    pts = np.array([[10,5],[20,30],[40,10],[30,30]],np.int32)
    pts.reshape((-1,1,2))
    cv2.polylines(img,[pts],True,(125,125,255),3) # ploylines is a line connect all plots
    
    
    
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
#    plt.imshow(cv2,interpolation='bicubic')
        
    
    




