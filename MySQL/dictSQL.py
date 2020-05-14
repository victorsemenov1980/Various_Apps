#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:29:11 2020

@author: user
"""


import mysql.connector

con=mysql.connector.connect(
    user='ardit700_student',
    password='ardit700_student',
    host='108.167.140.122',
    database='ardit700_pm1database'
    )

word=input('Enter the word ')

cursor=con.cursor()
query=cursor.execute("SELECT * FROM Dictionary WHERE Expression = '%s'"%word)
result=cursor.fetchall()
print(result)

"""
Here are some more examples of SQL queries that you can try out from within your Python script just like we did previously:

Get all rows where the value of the column Expression starts with r:

"SELECT * FROM Dictionary WHERE Expression  LIKE 'r%'"
Get all rows where the value of the column Expression starts with rain:

"SELECT * FROM Dictionary WHERE Expression  LIKE 'rain%'"
All rows where the length of the value of the column Expression is less than four characters:

"SELECT * FROM Dictionary WHERE length(Expression) < 4"
All rows where the length of the value of the column Expression is four characters:

"SELECT * FROM Dictionary WHERE length(Expression) = 4"
All rows where the length of the value of the column Expression is greater than 1 but less than 4 characters:

"SELECT * FROM Dictionary WHERE length(Expression) > 1 AND length(Expression) < 4"
All rows of column Definition where the value of the column Expression starts with r:

"SELECT Definition FROM Dictionary WHERE Expression  LIKE 'r%

"""