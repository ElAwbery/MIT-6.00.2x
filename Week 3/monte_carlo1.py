#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 13:17:55 2018

@author: Charlie
"""
import random

def noReplacementSimulation(numTrials):
    '''
    Runs numTrials trials of a Monte Carlo simulation
    of drawing 3 balls out of a bucket containing
    3 red and 3 green balls. Balls are not replaced once
    drawn. Returns a decimal - the fraction of times 3 
    balls of the same color were drawn.
    '''
    success_count_red = 0
    success_count_green = 0
    
    current_trials = 0
    
    while current_trials < numTrials:
        
        first_selection = random.random()
        second_selection = random.random()
        third_selection = random.random()
            
        # all balls are red: (because 0.5 all balls are red 0.4 balls remaining balls for second pick are red
        # and 0.25 balls remaining for final pick are red 
        
        if first_selection < 0.5 and second_selection < 0.4 and third_selection < 0.25:  
            success_count_red += 1
                                  
        # all balls are green:    
        elif first_selection >= 0.5 and second_selection >= 0.6 and third_selection >= 0.75:  
            success_count_green += 1
        
        current_trials += 1 
    
    return (success_count_red + success_count_green)/numTrials # the ratio of success to numTrials

# test:
# a reasonable result would be around 1/20*2 (red success + green success) = roughly 0.1 success ratio 
  
trial_numbers_to_test = [10, 100, 1000, 10000, 100000, 1000000, 10000000]

for trial in trial_numbers_to_test:
    print(noReplacementSimulation(trial))
    
    
    
    
