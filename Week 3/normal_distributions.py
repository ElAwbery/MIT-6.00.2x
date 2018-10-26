#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 12:51:33 2018

@author: ElAwbery
"""

import random
import pylab

dist = []

for i in range(10000):
    dist.append(random.gauss(0, 30))
    pylab.hist(dist, 30)    

def getMeanAndStandard(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    
    for x in X:
        tot += (x - mean)**2 # square the differences from the mean
        
    std = (tot/len(X))**0.5 # get the SD
    
    return mean, std

L = [1, 1, 1, 1, 2]
pylab.hist(L)

factor = pylab.array(len(L)*[1])/len(L)
print(factor)

pylab.figure()
pylab.hist(L, weights = factor)
   
pylab.show()

