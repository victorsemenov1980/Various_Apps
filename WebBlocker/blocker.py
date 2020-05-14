#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 15:18:03 2020

@author: user
"""
import time
from datetime import datetime as dt

hosts_path='hosts'
redirect='127.0.0.1'
websites=['www.rbc.ru','www.exler.ru']
while True:
    if dt(dt.now().year,dt.now().month,dt.now().day,8)<dt.now()<dt(dt.now().year,dt.now().month,dt.now().day,16):
        with open(hosts_path,'r+') as file:
            content=file.read()
            for website in websites:
                if website in content:
                    pass
                else:
                    file.write(redirect+' '+website+'\n')
    else:
        with open(hosts_path,'r+') as file:
            content=file.readlines()#will make a list of line instead of a string
            file.seek(0)#putting cursor at the beginning of the file
            for line in content:
                if not any(website in line for website in websites):
                    file.write(line)
            file.truncate()#cuts everything after the last correct line written
            
    time.sleep(60)