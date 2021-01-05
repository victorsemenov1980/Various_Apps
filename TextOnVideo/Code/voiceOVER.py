#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 14:45:01 2020

@author: user
"""


from gtts import gTTS
import os

with open('/Users/user/Desktop/Code/Experiments/TextOnVideo/txt/10waystogetfit.txt','r') as file:
    myText=file.read().replace("\n"," ")

language='en'

output=gTTS(text=myText,lang=language, slow=False)

output.save('voice.mp3')