#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 20:46:52 2020

@author: user
"""

import random
import PySimpleGUI as sg  
n=10  

success=0
failure=0
x=random.randint(10,20)
y=random.randint(0,10)   
k=('+','-')
z=random.choice(k) 
out1='Great Job! You made'
out3='mistakes and won'
out5='Sorry, the correct answer is'
assignment=x,z,y

layout = [ [sg.Txt('If ready - press GO!')],
             
            [sg.Txt('', size=(20,10), key='output1')  ], 
            [sg.In(size=(50,20), key='answer')],      
            [sg.Txt('_'  * 40)],      
            [sg.Txt('', size=(20,10), key='output')  ],      
            [sg.Button('Check', bind_return_key=True)],
            [sg.Button('Go', bind_return_key=True)]]      

window = sg.Window('Math', layout)    
while True:  
    event, values = window.read()  
    if event == 'Go':
        window['output1'].update(assignment)  
    if event =='Check':      
        try:
            if z=='+':
                i=x+y
            elif z=='-':
                i=x-y
            answer=int(values['answer']) 
            if answer==i:
                success+=1
                failure+=0
                out2=failure
                out4=success
                output=out1,out2,out3,out4
            else:
                failure+=1
                success+=0
                out6=i
                output=out5,out6
               
        except:      
            output = 'Invalid'     

        window['output'].update(output)      
    else:      
        break      



