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

'''
Backend part
'''
class Database:
    def __init__(self,db):
        self.db=db
        self.conn=sqlite3.connect(db)
        self.cur=self.conn.cursor()
        
        
    def view_all(self):
        self.cur.execute('SELECT * FROM book')
        return self.cur.fetchall()
        
        
    def search(self,title="",author="",year="",isbn=""):#default empty in case user will not  enter all the values
        self.cur.execute('SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?',(title,author,year,isbn))
        return self.cur.fetchall()
        
    def add(self,title,author,year,isbn):
        self.cur.execute('INSERT INTO book VALUES (NULL,?,?,?,?)',(title,author,year,isbn))
        self.conn.commit()
        
        
    def update(self,title,author,year,isbn,id):
        self.cur.execute('UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?',(title,author,year,isbn,id))
        self.conn.commit()
       
        
    def delete(self,id):
        self.cur.execute('DELETE FROM book WHERE id=?',(id,))
        self.conn.commit()
        
    def __del__(self):
        self.conn.close()#closing database before exiting the programm
       
database=Database('books.db')
'''
Frontend part
'''
class Window:
    def __init__(self,window):
        self.window = window
 
        self.window.wm_title("Books")
        '''INPUT boxes'''

        self.e1=Label(window,text="Book title")
        self.e1.grid(row=0,column=0)
        self.e1_value=StringVar()
        self.e1=Entry(window,textvariable=self.e1_value)
        self.e1.grid(row=0,column=1)
        self.e2=Label(window,text="Book author")
        self.e2.grid(row=0,column=2)
        self.e2_value=StringVar()
        self.e2=Entry(window,textvariable=self.e2_value)
        self.e2.grid(row=0,column=3)
        self.e3=Label(window,text="Year of publication")
        self.e3.grid(row=1,column=0)
        self.e3_value=StringVar()
        self.e3=Entry(window,textvariable=self.e3_value)
        self.e3.grid(row=1,column=1)
        self.e4=Label(window,text="ISBN")
        self.e4.grid(row=1,column=2)
        self.e4_value=StringVar()
        self.e4=Entry(window,textvariable=self.e4_value)
        self.e4.grid(row=1,column=3)
        
        '''OUTput box'''
        self.t1=Listbox(window,height=20,width=60)
        self.t1.grid(row=2,column=0,columnspan=6)
        sb1=Scrollbar(window)
        sb1.grid(row=2,column=4)
        self.t1.configure(yscrollcommand=sb1.set)
        sb1.configure(command=self.t1.yview)
        
        '''BIND is the function allowing to get the info from the list item '''
        self.t1.bind('<<ListboxSelect>>',self.get_selected_row)
        
        '''Buttons'''
        b1=Button(window,text='Search',command=self.search1)
        b1.grid(row=3,column=0,rowspan=1)
        b2=Button(window,text='View All',command=self.view)
        b2.grid(row=3,column=1,rowspan=1)
        b3=Button(window,text='Add new entry',command=self.add1)
        b3.grid(row=3,column=2,rowspan=1)
        b4=Button(window,text='Update this entry',command=self.update1)
        b4.grid(row=4,column=0,rowspan=1)
        b5=Button(window,text='Delete this entry',command=self.delete1)
        b5.grid(row=4,column=1,rowspan=1)
    def view(self):
        self.t1.delete(0,END)#clear the outputbox
        x=database.view_all()
        for i in x:
            self.t1.insert(END,i)
        
    def search1(self):
        self.t1.delete(0,END)#clear the outputbox
        
        x=database.search(self.e1_value.get(),self.e2_value.get(),self.e3_value.get(),self.e4_value.get())
        for i in x:
            self.t1.insert(END,i)
    def add1(self):
        self.t1.delete(0,END)#clear the outputbox
        database.add(self.e1_value.get(),self.e2_value.get(),self.e3_value.get(),self.e4_value.get())
        self.t1.insert(END,self.e1_value.get(),self.e2_value.get(),self.e3_value.get(),self.e4_value.get())
    def update1(self):
        self.t1.delete(0,END)#clear the outputbox
        database.update(self.e1_value.get(),self.e2_value.get(),self.e3_value.get(),self.e4_value.get(),selected_tuple[0])
        '''We need to pass the index as it is, but the values got to be original, not from the Selected tuple,
        otherwise we will be sending to database unchanged record'''
        x=search(selected_tuple[1],selected_tuple[2],selected_tuple[3],selected_tuple[4])
        self.t1.insert(END,x)
    def delete1(self):
        database.delete(selected_tuple[0])  
        view_all()
        '''We just pass the index from the list item'''
    
    '''
    Get selected row is my function to get values from the selected item in list
    '''
    def get_selected_row(self,event):
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



window=Tk()
Window(window)
window.mainloop()