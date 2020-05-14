#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 20:08:23 2020

@author: user
"""
import random
# import PySimpleGUI as sg
print('Hello dear! Today you will need to decide how many tasks you will compute.')
print()
n=int(input('So, how many? '))
success=0
failure=0
for i in range(n):
    x=random.randint(10,20)
    y=random.randint(0,10)
    k=('+','-')
    z=random.choice(k)
    print()
    print('How much will it be ',x,z,y)
    if z=='+':
        i=x+y
    elif z=='-':
        i=x-y
    answer=int(input('Print you answer here: '))
    
    if answer==i:
        print()
        print('Great Job!')
        success+=1
    else:
        print()
        print('Sorry, that was a wrong answer, the correct answer is ',i)
        failure+=1

print()
print('Your results are: Correctly solved: ',success,' and total mistakes: ',failure)
    
