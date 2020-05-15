#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 15 16:39:57 2020

@author: user
"""
import tkinter
from tkinter import*

window=Tk()

window.wm_title('Current balance')#Title for the window

class account:
    def __init__(self,file):
        self.file=file
        with open(file,'r') as file:
            self.balance=int(file.read())#file read is always a string
    
    def withdraw(self,amount):
        self.amount=amount
        self.balance=self.balance-amount
        return self.balance
    
    def deposit(self,amount):
        self.amount=amount
        self.balance=self.balance+amount
        return self.balance
    
    def save(self):
        with open(self.file,'w') as file:
            file.write(str(self.balance))

def view():
    t1.insert(END,str(current.balance)+'\n')
    current.save()
    
def withdraw():
    current.withdraw(int(e1_value.get()))
    t1.insert(END,'After withdrawal of '+e1_value.get()+' the leftover is '+str(current.balance)+'\n')
    current.save()
def deposit():
    current.deposit(int(e1_value.get()))
    t1.insert(END,'After deposit of '+e1_value.get()+' the available balance is '+str(current.balance)+'\n')
    current.save()
current=account('balance.txt')

'''INPUT boxes'''

e1=Label(window,text="Enter amount")
e1.grid(row=0,column=0)
e1_value=StringVar()
e1=Entry(window,textvariable=e1_value)
e1.grid(row=0,column=1)



'''OUTput box'''
t1=Text(window,height=20,width=60)
t1.grid(row=2,column=0,columnspan=6)


'''Buttons'''
b1=Button(window,text='View current balance',command=view)
b1.grid(row=3,column=0,rowspan=1)
b2=Button(window,text='Withdraw amount',command=withdraw)
b2.grid(row=3,column=1,rowspan=1)
b3=Button(window,text='Deposit amount',command=deposit)
b3.grid(row=3,column=2,rowspan=1)


window.mainloop()