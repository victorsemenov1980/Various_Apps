import tkinterfrom tkinter import*import sqlite3window=Tk()def cube():    g=round(float(e1_value.get())*1000,2)    p=round(float(e1_value.get())*2.20462,2)    o=round(float(e1_value.get())*35.274,2)    # t1.insert(END,e1_value.get())    t1.insert(END,str(g)+' grams')    t2.insert(END,str(p)+' pounds')    t3.insert(END,str(o)+' ounces')b1=Button(window,text='Convert',command=cube)"""Button needs command parameter to work"""b1.grid(row=0,column=2,rowspan=5)#position, span for size in rows"""Entry for inputText for output"""e1=Label(window,text="Enter kilograms")e1.grid(row=0,column=0)e1_value=StringVar()e1=Entry(window,textvariable=e1_value)e1.grid(row=0,column=1)t1=Text(window,height=2,width=20)t1.grid(row=1,column=0)t2=Text(window,height=2,width=20)t2.grid(row=2,column=0)t3=Text(window,height=2,width=20)t3.grid(row=3,column=0)window.mainloop()