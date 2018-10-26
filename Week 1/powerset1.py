#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 11:52:49 2018

@author: ElAwbery
"""

# generate all combinations of N items
def powerSet(items):
    N = len(items)
    # enumerate the 2**N possible combinations
    for i in range(2**N): # the number of possible combinations
        
        combo = []
        
        for j in range(N):  # for each item (indexed)
            # make up a combination from this algorithm
            
            if (i >> j) % 2 == 1:
                combo.append(items[j])
                print ("adding to combo when i =", i, "and j = ", j)
               
        yield combo # gives one of the possible combinations, each time round the outer for loop
        # now i increments and we go another time round the inner for loop
        # we have a different value for i, and work again through the j index
'''
As above, suppose we have a generator that returns every combination of objects in one bag. 
We can represent this as a list of 1s and 0s denoting whether each item is in the bag or not.

Write a generator that returns every arrangement of items such that each is in one or none of two 
different bags. Each combination should be given as a tuple of two lists, the first being the items 
in bag1, and the second being the items in bag2.
'''

items1 = ['string', 'bool', 'tuple', 'list', 'dic', 'range', 'class', 'integer']
items2 = ['a', 'b', 'c']

# My first solution to the power set problem. 

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


 
    
    
    
    
    
