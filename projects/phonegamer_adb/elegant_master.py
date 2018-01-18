# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 08:12:49 2018

@author: xujianqiao
"""

import os
import re
import time
result = os.popen("adb shell getevent -p").read()
width = float(re.findall(".*0035.*value.*max (\d*).*",result)[0])
height = float(re.findall(".*0036.*value.*max (\d*).*",result)[0])

rateW = 1080/width
rateH = 1920/height


#result = os.popen("adb shell getevent").read()

def click(loc_x,loc_y):
    click = (int(loc_x,16),int(loc_y,16))
    screen_location = (click[0]*rateW,click[1]*rateH)
    os.popen("adb shell input tap %i %i"% \
            (int(screen_location[0]),int(screen_location[1])))

while True:
    os.popen("adb shell input keyevent 26")
    time.sleep(1)
    os.popen("adb shell input swipe 500 500 1500 1500 500")
    time.sleep(1)
    click('000000d7','00000400')
    time.sleep(0.3)
    click('000000d7','00000400')
    time.sleep(0.3)
    click('00000226','00000408')
    time.sleep(0.3) 
    click('0000021f','0000062a')
    time.sleep(1)      
    
    click('0000037d','00000273')
    time.sleep(2)
    for i in range(4):
        click('0000037d','00000273')
        time.sleep(0.3)
    for i in range(5):
        click('0000037b','0000045c')
        time.sleep(0.3)
    for i in range(5):
        click('0000031b','00000639')
        time.sleep(0.3)
    time.sleep(1)
    os.popen("adb shell input keyevent 26")
    for i in range(30):
        print("sleeping %i"%(i*20))
        time.sleep(20)



#import subprocess
#
#p1 = subprocess.Popen("adb shell geteven")



   