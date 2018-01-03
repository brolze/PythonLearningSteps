# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 17:24:22 2017

@author: potato

基于教程
http://outofmemory.cn/code-snippet/2267/Python-duojincheng-multiprocessing-usage-example

v0.03:
    增加了守护进程
    守护进程就是不阻挡主程序退出，自己干自己的 mutilprocess.setDaemon(True)
    等待守护进程退出，要加上join,join可以传入浮点数值，等待n久就不等了

"""
import multiprocessing
import time

def daemon():
    name = multiprocessing.current_process().name
    print('Starting:', name)
    time.sleep(2)
    print('Exiting :', name)

def non_daemon():
    name = multiprocessing.current_process().name
    print('Starting:', name)
    time.sleep(2)
    print('Exiting :', name)

if __name__ == '__main__':
    d = multiprocessing.Process(name='daemon',
                                target=daemon)
    d.daemon = True #给d进程定义存在守护进程

    n = multiprocessing.Process(name='non-daemon',
                                target=non_daemon)
    n.daemon = False

    d.start()
    n.start()

    print('d.is_alive()', d.is_alive())
    print('n.is_alive()', n.is_alive())
    d.join(1)
    print('d.is_alive()', d.is_alive())
    print('n.is_alive()', n.is_alive())
    n.join()