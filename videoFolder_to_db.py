# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 03:35:28 2019

"""

# local imports
import db_helper as dbh

# system imports
import sqlite3 
import os
import json 
import os.path
import os


dbh.create_table

folders = []
files = []
fileNames=[]

for entry in os.scandir('video_dataset_processed_2fr'):
    if entry.is_dir():
        folders.append(entry.path)
        for entry1 in os.scandir(entry.path):
            if entry1.is_dir():
                folders.append(entry1.path)
                for entry2 in os.scandir(entry1.path):
                    if entry2.is_dir():
                        folders.append(entry2.path)
                    elif entry2.is_file():
                        if os.path.splitext(entry2)[1] == ".json":
                            files.append(entry2.path)
                            fileNames.append(entry2.name)
            elif entry1.is_file():
                if os.path.splitext(entry1)[1] == ".json":
                    files.append(entry1.path)
                    fileNames.append(entry1.name)
    elif entry.is_file():
        if os.path.splitext(entry)[1] == ".json":
            fileNames.append(entry1.name)
            
            
            


"""
Delete all records from database
"""
connection = sqlite3.connect("db\\main_dataset.db") 
crsr = connection.cursor() 
sql_command = "DELETE FROM videoDataset;"
crsr.execute(sql_command)
connection.commit()  
connection.close()

            
# connecting to the database  
connection = sqlite3.connect("db\\main_dataset.db") 
# cursor  
crsr = connection.cursor()             
count=0
for file in files:
    js = json.loads(open(files[count]).read())
        
    parent = (os.path.dirname(files[count])).split('\\')
    parentName = "'"+parent[len(parent)-2]+"'"
    
    
    sql_command = "INSERT INTO videoDataset VALUES (NULL, '"+ str(files[count]) + "',"+parentName+");"
    crsr.execute(sql_command)  
    count+=1           
            
connection.commit()  
connection.close() 

















