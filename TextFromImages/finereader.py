#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 16:32:09 2020

@author: user
"""
import pandas as pd
import re

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text

string=ocr_core('test3.png')
with open('text.txt','w') as file:
    file.write(string)
row={}
lines=[]
with open('text.txt','r') as file:
    
    input_ = file.read()
x=re.split(r'Get directions',input_)
# print(x)
row['name']=[]
row['Address']=[]
for i in range(len(x)-1):
    
    y=re.split(r'\n\n \n\n',x[i])
    
    
    
    row['name'].append(y[0])
    
    
    row['Address'].append(y[1])
# print(row)
df=pd.DataFrame(row)
print(df)

df.to_csv('output.csv',index=True)


                    