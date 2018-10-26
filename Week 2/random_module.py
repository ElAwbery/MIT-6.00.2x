#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 13:26:50 2018

@author: Charlie
"""
'''
import random


# random generator of even numbers

def genEven():

    return random.randrange(10, 21, 2)

    
# deterministic generator of even numbers

def determinist():
    
    for even in range(10, 21, 2):
    
        return even
    
print(determinist())
'''    
'''
import random

mylist = []

# The following i will be a different integer each time, because there is an unknown seed
for i in range(random.randint(1, 10)):
    print("i", i)
    random.seed(0)
    # The following number is always going to be 7, because the seed is re-set, and randint follows a prescribed order (it isn't random from seed 0)
    if random.randint(1, 10) > 3: 
        number = random.randint(1, 10)
        mylist.append(number)
        
print(mylist)
'''
'''
import random

# Code Sample A
mylist = []

for i in range(random.randint(1, 10)):
    random.seed(0)
    if random.randint(1, 10) > 3:
        number = random.randint(1, 10)
        if number not in mylist:
            mylist.append(number)
print(mylist)
'''
import random


mylist = []

random.seed(0)
for i in range(random.randint(1, 10)): # for i in range 7
    if random.randint(1, 10) > 3: # second time randint is called, it will be 7, then 4th time...
        number = random.randint(1, 10) # third time randint is called, this will be 1
        mylist.append(number)
    print(mylist)
    





































