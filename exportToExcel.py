#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 09:45:38 2020

@author: elvyyang
"""


import xlsxwriter
import os, os.path
import ast

workbook = xlsxwriter.Workbook('Oxford_Book_List.xlsx')
worksheet = workbook.add_worksheet()

dirName = "./book_data"
files = []
Files = os.listdir(dirName)
for filename in Files:
    if filename.endswith(".json"):
        files.append(os.path.join(dirName, filename))

row = 1

for book_data in files:
    with open(book_data,'r') as reader:
       contents = reader.read()
       fileDict = ast.literal_eval(contents)
    
    header = ["Title", "Author", "Publication", "Date"]
    col = 0
    for i in header:
        worksheet.write(0,col,i)
        col+=1
        
    for title in fileDict:
        col = 0
        worksheet.write(row,col,title)
        for i in fileDict[title]:
            for x in i:
                worksheet.write(row,col+1,x)
                col+=1
        row+=1
workbook.close()
