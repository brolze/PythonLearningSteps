# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 17:17:39 2017

@author: potato

基于教程
http://outofmemory.cn/code-snippet/2267/Python-duojincheng-multiprocessing-usage-example
v0.01:
    先来一个最简单的多进程
"""

import multiprocessing
import time

def worker(num):
    """thread worker function"""
    print('Worker:', num)
    return

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()



