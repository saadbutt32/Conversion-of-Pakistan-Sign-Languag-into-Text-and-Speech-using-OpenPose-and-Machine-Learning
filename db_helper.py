# -*- coding: utf-8 -*-

# local imports
import move 
import scale
import helperFunc as helper

# system imports
import sqlite3 
import os
import json 
import os.path
import math
  

def populate_db():
    
    """
    Delete all records from database
    """
    connection = sqlite3.connect("db\\main_dataset.db") 
    crsr = connection.cursor() 
    sql_command = "DELETE FROM rightHandDataset;"
    crsr.execute(sql_command)
    connection.commit()  
    connection.close()
    
    
    
    folders = []
    files = []
    fileNames=[]
    
    for entry in os.scandir('dataset'):
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
         
    # connecting to the database  
    connection = sqlite3.connect("db\\main_dataset.db") 
    # cursor  
    crsr = connection.cursor() 
     
        
    count=0
    
    for file in files:
        js = json.loads(open(files[count]).read())
            
        parent = (os.path.dirname(files[count])).split('\\')
            
        parentName = "'"+parent[len(parent)-2]+"'"
            
        count+=1
        for items in js['people']:
            handRight = items["hand_right_keypoints_2d"]
        
        handPoints = helper.removePoints(handRight)
        p1 = [handPoints[0], handPoints[1]]
        p2 = [handPoints[18], handPoints[19]]
        distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
        
        Result,Points = scale.scalePoints(handPoints,distance)
       
        handRightResults,handRightPoints = move.centerPoints(Result)
        
#        p1 = [Result[0], Result[1]]
#        p2 = [Result[17], Result[18]]
#        distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
#    
#    
#        handRightResults,handRightPoints = scale.scalePoints(Result,distance)
#        print(handRightResults)
#        p1 = [handRightResults[0], handRightResults[1]]
#        p2 = [handRightResults[17], handRightResults[18]]
#        distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
            
      
       
        # SQL command to insert the data in the table 
        sql_command = "INSERT INTO rightHandDataset VALUES (NULL, "+ str(handRightResults[0]) + ", "+ str(handRightResults[1]) + ","+ str(handRightResults[2]) + ","+ str(handRightResults[3]) + ","+ str(handRightResults[4]) + ","+ str(handRightResults[5]) + ","+ str(handRightResults[6]) + ","+ str(handRightResults[7]) + ","+ str(handRightResults[8]) + ","+ str(handRightResults[9]) + ","+ str(handRightResults[10]) + ","+ str(handRightResults[11]) + ","+ str(handRightResults[12]) + ","+ str(handRightResults[13]) + ","+ str(handRightResults[14]) + ","+ str(handRightResults[15]) + ","+ str(handRightResults[16]) + ","+ str(handRightResults[17]) + ","+ str(handRightResults[18]) + ","+ str(handRightResults[19]) + ","+ str(handRightResults[20]) + ","+ str(handRightResults[21]) + ","+ str(handRightResults[22]) + ","+ str(handRightResults[23]) + ","+ str(handRightResults[24]) + ","+ str(handRightResults[25]) + ","+ str(handRightResults[26]) + ","+ str(handRightResults[27]) + ","+ str(handRightResults[28]) + ","+ str(handRightResults[29]) + ","+ str(handRightResults[30]) + ","+ str(handRightResults[31]) + ","+ str(handRightResults[32]) + ","+ str(handRightResults[33]) + ","+ str(handRightResults[34]) + ","+ str(handRightResults[35]) + ","+ str(handRightResults[36]) + ","+ str(handRightResults[37]) + ","+ str(handRightResults[38]) + ","+ str(handRightResults[39]) + ","+ str(handRightResults[40]) + ","+ str(handRightResults[41]) + ","+parentName+");"
        crsr.execute(sql_command)     
                
        
    connection.commit()  
    connection.close()

def create_video_table():
    connection = sqlite3.connect("db\\main_dataset.db")  
    crsr = connection.cursor() 
    
    sql_command1 = """CREATE TABLE IF NOT EXISTS videoDataset (  
     id INTEGER PRIMARY KEY,  
     video VARCHAR(90),
     label VARCHAR(30)  
     );"""
    
    crsr.execute(sql_command1) 
    
    connection.commit()  
    connection.close()
    
def create_table():
    connection = sqlite3.connect("db\\main_dataset.db")  
    crsr = connection.cursor() 
    
    
    
    sql_command1 = """CREATE TABLE IF NOT EXISTS rightHandDataset (  
     id INTEGER PRIMARY KEY,  
     x1 DOUBLE,
     y1 DOUBLE,
     x2 DOUBLE,
     y2 DOUBLE,  
     x3 DOUBLE,
     y3 DOUBLE,
     x4 DOUBLE,
     y4 DOUBLE,
     x5 DOUBLE,
     y5 DOUBLE,
     x6 DOUBLE,
     y6 DOUBLE,
     x7 DOUBLE,
     y7 DOUBLE,
     x8 DOUBLE,
     y8 DOUBLE,
     x9 DOUBLE,
     y9 DOUBLE,
     x10 DOUBLE,
     y10 DOUBLE,
     x11 DOUBLE,
     y11 DOUBLE,
     x12 DOUBLE,
     y12 DOUBLE,
     x13 DOUBLE,
     y13 DOUBLE,
     x14 DOUBLE,
     y14 DOUBLE,
     x15 DOUBLE,
     y15 DOUBLE,
     x16 DOUBLE,
     y16 DOUBLE,
     x17 DOUBLE,
     y17 DOUBLE,
     x18 DOUBLE,
     y18 DOUBLE,
     x19 DOUBLE,
     y19 DOUBLE,
     x20 DOUBLE,
     y20 DOUBLE,
     x21 DOUBLE,
     y21 DOUBLE,
    
     label VARCHAR(30)  
     );"""
    
    
    #crsr.execute("DELETE FROM rHand")
    
    # execute the statement 
    crsr.execute(sql_command1)
    
    connection.commit()  
    connection.close()
    
    
 
    
    
    
    
    

            
            
            
            
            
            
            
            
            
    
    
    
    
    
    