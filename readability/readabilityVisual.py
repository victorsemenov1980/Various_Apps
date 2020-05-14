#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 16:10:16 2020

@author: user
"""
class readability(object):
    def __init__(self,text):
        self.text=text
    def evaluate(self):
        alphabeth=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        x=self.text.split()
        letters=int()
        sentences=int()
        for char in self.text:
            if char in alphabeth:
                letters+=1
            else:
                letters+=0
        for char in text:
            if char=='.' or char=='!' or char=='?':
                sentences+=1
            else:
                sentences+=0
        L=letters*100/len(x)
        S=sentences*100/len(x)  
        index=int()
        index=0.0588 * L - 0.296 * S - 15.8
        # print('')
        # print('Number of words: ',len(x))
        # print('')
        # print('Number of letters in text: ',letters)
        # print('')
        # print('Number of sentences: ',sentences)
        # print('')
        if index<1:
            p='Before Grade 1'
        elif index>16:
            p='Grade 16+'
        else:
            p='Grade: '+str(round(index))
        return p

# text='I love you!'
# test=readability(text)
# print(test.evaluate())

import PySimpleGUI as sg

sg.theme('BluePurple')

layout = [[sg.Text('Coleman-Liau index. Index = 0.0588 * L - 0.296 * S - 15.8.'), sg.Text(size=(15,1), key='-OUTPUT-')],
          [sg.Input(key='-IN-')],
          [sg.Button('Show'), sg.Button('Exit')]]

window = sg.Window('Pattern 2B', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event in  (None, 'Exit'):
        break
    if event == 'Show':
        text=values['-IN-']
        test=readability(text)
        p=test.evaluate()
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].update(p)

window.close()










