#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 12:27:49 2018

@author: ElAwbery
"""

# Hi, for info this is my original solution to the power set problem. 

def BigPowerSet(items):
    
    N = len(items)
      
    for i in range (3**N):
        
        list1 = []
        list2 = []
        combo = (list1, list2)
        ternary = base_three(i, N)
        
        # yields one result from N times round the inner for loop, like with the example generator
        # uses ternary string indexing to access the bag number (0, 1, or 2)  
        
        for j in range(N):
            
            if int(ternary[j]) == 1:  
                
                list1.append(items[j])
             
            if int(ternary[j]) == 2: 
                list2.append(items[j])
     
        combo = (list1, list2)
        
        yield combo # gives one of all possible combinations, each time round the outer for loop
        
def base_three(num, digits):
    if digits == 0:
        return ''
    else:
        return base_three(num//3, digits - 1) + str(num%3)


  
# Using ideas from from the net using itertools, this the shortest length code I could get it down to:   
    
import itertools

# solution no. 1
bag = ['a', 'b', 'c']

def cool_powerset(bag):
    
    powerset = [x for length in range(len(bag)+1) for x in itertools.combinations(bag, length)]
    
    return powerset

print(cool_powerset(bag))


 
    