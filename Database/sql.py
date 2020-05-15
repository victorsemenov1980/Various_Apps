#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 19:19:24 2020

@author: user
"""


import tkinter
from tkinter import*
import sqlite3
from tkinter.ttk import*

import sys



window=Tk()

window.wm_title('Book Database')#Title for the window



def view_all():
    t1.delete(0,END)#clear the outputbox
    conn=sqlite3.connect('books.db')
    cur=conn.cursor()
    cur.execute('SELECT * FROM book')
    x=cur.fetchall()
    conn.close()
    for i in x:
        t1.insert(END,i)
    
def search(title="",author="",year="",isbn=""):#default empty in case user will not  enter all the values
    conn=sqlite3.connect('books.db')
    cur=conn.cursor()
    cur.execute('SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?',(title,author,year,isbn))
    x=cur.fetchall()
    conn.close()
    for i in x:
        t1.insert(END,i)
def add(title,author,year,isbn):
    conn=sqlite3.connect('books.db')
    cur=conn.cursor()
    cur.execute('INSERT INTO book VALUES (NULL,?,?,?,?)',(title,author,year,isbn))
    conn.commit()
    conn.close()
def update(title,author,year,isbn,id):
    conn=sqlite3.connect('books.db')
    cur=conn.cursor()
    cur.execute('UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?',(title,author,year,isbn,id))
    conn.commit()
    conn.close()
def delete(id):
    conn=sqlite3.connect('books.db')
    cur=conn.cursor()
    cur.execute('DELETE FROM book WHERE id=?',(id,))
    conn.commit()
    conn.close()    
    
def search1():
    t1.delete(0,END)#clear the outputbox
    x=search(e1_value.get(),e2_value.get(),e3_value.get(),e4_value.get())
    for i in x:
        t1.insert(END,i)
def add1():
    t1.delete(0,END)#clear the outputbox
    x=add(e1_value.get(),e2_value.get(),e3_value.get(),e4_value.get())
    t1.insert(END,e1_value.get(),e2_value.get(),e3_value.get(),e4_value.get())
def update1():
    t1.delete(0,END)#clear the outputbox
    update(e1_value.get(),e2_value.get(),e3_value.get(),e4_value.get(),selected_tuple[0])
    '''We need to pass the index as it is, but the values got to be original, not from the Selected tuple,
    otherwise we will be sending to database unchanged record'''
    x=search(selected_tuple[1],selected_tuple[2],selected_tuple[3],selected_tuple[4])
    t1.insert(END,x)
def delete1():
    x=delete(selected_tuple[0])  
    view_all()
    '''We just pass the index from the list item'''
    
'''
Get selected row is my function to get values from the selected item in list
'''
def get_selected_row(event):
    '''Global is needed to ease the use of variable that doesn't exist outside the function'''
    global selected_tuple
    id=t1.curselection()[0]
    selected_tuple=t1.get(id)
    e1.delete(0,END)
    e1.insert(END,selected_tuple[1])
    e2.delete(0,END)
    e2.insert(END,selected_tuple[2])
    e3.delete(0,END)
    e3.insert(END,selected_tuple[3])
    e4.delete(0,END)
    e4.insert(END,selected_tuple[4])
    return(selected_tuple)

'''INPUT boxes'''

e1=Label(window,text="Book title")
e1.grid(row=0,column=0)
e1_value=StringVar()
e1=Entry(window,textvariable=e1_value)
e1.grid(row=0,column=1)
e2=Label(window,text="Book author")
e2.grid(row=0,column=2)
e2_value=StringVar()
e2=Entry(window,textvariable=e2_value)
e2.grid(row=0,column=3)
e3=Label(window,text="Year of publication")
e3.grid(row=1,column=0)
e3_value=StringVar()
e3=Entry(window,textvariable=e3_value)
e3.grid(row=1,column=1)
e4=Label(window,text="ISBN")
e4.grid(row=1,column=2)
e4_value=StringVar()
e4=Entry(window,textvariable=e4_value)
e4.grid(row=1,column=3)

'''OUTput box'''
t1=Listbox(window,height=20,width=60)
t1.grid(row=2,column=0,columnspan=6)
sb1=Scrollbar(window)
sb1.grid(row=2,column=4)
t1.configure(yscrollcommand=sb1.set)
sb1.configure(command=t1.yview)

'''BIND is the function allowing to get the info from the list item '''
t1.bind('<<ListboxSelect>>',get_selected_row)

'''Buttons'''
b1=Button(window,text='Search',command=search1)
b1.grid(row=3,column=0,rowspan=1)
b2=Button(window,text='View All',command=view_all)
b2.grid(row=3,column=1,rowspan=1)
b3=Button(window,text='Add new entry',command=add1)
b3.grid(row=3,column=2,rowspan=1)
b4=Button(window,text='Update this entry',command=update1)
b4.grid(row=4,column=0,rowspan=1)
b5=Button(window,text='Delete this entry',command=delete1)
b5.grid(row=4,column=1,rowspan=1)

window.mainloop()