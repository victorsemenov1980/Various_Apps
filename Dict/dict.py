#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 15:14:39 2020

@author: user
"""

import json
import difflib
from difflib import SequenceMatcher
from difflib import get_close_matches

def dict(data,keyword):
    try:
        data[keyword] 
    except:
        KeyError()
        try:
            i=keyword.title()
            return data[i]
            
        except:
            KeyError()
            try:
                j=keyword.upper()
                return data[j]
            except:
                KeyError()
                try:
                    x=get_close_matches(keyword, data.keys())
                    y=input( f'Did you mean {x[0]} instead? y/n ')
                    y1=y.lower()
                    if y1 in ['y','yes']:
                        return data[x[0]]
                    else:
                        return 'Sorry'
            
                except:
                    x=None
                    return'Word not found'
   
    return data[keyword]
data=json.load(open('data.json'))
keyword=input('Enter your dictionary search: ')
x=keyword.lower()
print('The definition for the word',x,'is the following:')
print(dict(data, x))