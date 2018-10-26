#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 10:51:27 2018

@author: ElAwbery
"""
'''
Write a function, stdDevOfLengths(L) that takes in a list of strings, L, and outputs the standard deviation 
of the lengths of the strings. 
Return float('NaN') if L is empty.
'''

def stdDevOfLengths(L):
    """
    L is a list of strings
    Computes and returns the SD of the lengths of the strings in L
    """
    
    if L == []:
        return float('NaN')
   
    else:
        total = 0
        for el in L:
            total += len(el)
        mean = total/len(L)
        
        sum_of_squares = 0
        for el in L:
            square_of_distance = (len(el) - mean)**2
            sum_of_squares += square_of_distance
        
        standard_deviation = (sum_of_squares/len(L))**0.5
     
    return standard_deviation

print(stdDevOfLengths([]))

# Test cases:
empty = []
stdDevOfLengths(empty)
 
L = ['a', 'z', 'p'] 
print(stdDevOfLengths(L)) # 0

L2 = ['apples', 'oranges', 'kiwis', 'pineapples'] 
print(stdDevOfLengths(L2)) # 1.8708

L3 = ['', 'abc', 'a', 'abcdefghijklmnopqrstuvwxyz', '', '']
print(stdDevOfLengths(L3))

L4 = ['...', '....', '.....']
print(stdDevOfLengths(L4))

L5 = ['..........', '....', '............', '...............', '....................', '.....']
print(stdDevOfLengths(L5))
