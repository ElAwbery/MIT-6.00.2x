#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 17:18:49 2018

@author: Charlie
"""
import pylab as plt


mySamples = []
myLinear = []
myQuadratic = []
myCubic = []
myExponential = []

for i in range (0, 30):
    mySamples.append(i)
    myLinear.append(i)
    myQuadratic.append(i**2)
    myCubic.append(i**3)
    myExponential.append(1.5**i)


# first trial     
plt.plot(mySamples, myLinear)
plt.plot(mySamples, myQuadratic)
plt.plot(mySamples, myCubic)
plt.plot(mySamples, myExponential)


plt.figure('linear comparisons')  # figure creates a separate window frame with this name, then plt calls what to put in it. 
plt.clf()
plt.title("Cubic & quadratic cf. linear, from 6.00.2x")
plt.subplot(211)
plt.plot(mySamples, myQuadratic, 'r--', label = 'quadratic')
plt.plot(mySamples, myLinear, 'k-', label = 'linear')
plt.xlabel('sample points')
plt.ylabel('functions')
plt.legend(loc = 'upper left')

plt.subplot(212)
plt.plot(mySamples, myCubic, 'g--', label = 'cubic')
plt.plot(mySamples, myLinear, 'k-', label = 'linear')
plt.xlabel('sample points')
plt.ylabel('functions')
plt.ylim(0, 800)
plt.legend(loc = 'upper left')


plt.clf () # will clear a frame before you use it with the same name again. 


plt.figure('myExpo')
plt.plot(mySamples, myExponential)


def display_retire(monthlies, rate, terms):
    """
    Assumes monthlies is a list of numbers, representing amount paid per month
    rate is floating point representing percentage rate
    terms is number of years (usually something like 20 * 12)
    """
    plt.figure('retirement plot, 2nd scenario')
    plt.clf()
    for monthly in monthlies:
        xvals, yvals = retire(monthly, rate, terms) # helper function
        plt.plot(xvals, yvals, label = "monthly" + str(monthly))
        plt.legend(loc = 'upper left')
        
def retire(monthly, rate, terms):
    """
    Helper function for display_retire
    input monthly = an int, rate = a floating point representing percent roi, terms = number of months
    """
    savings = [0]
    base = [0]
    mRate = rate/12
    
    for i in range(terms):
        base += [i]
        savings += [savings[-1] * (1+mRate) + monthly]
    
    return base, savings
        
        
display_retire([50, 100, 250, 500, 1000], .05, 20*12)


















































    
    