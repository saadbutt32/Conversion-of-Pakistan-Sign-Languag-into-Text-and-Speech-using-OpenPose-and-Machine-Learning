# -*- coding: utf-8 -*-

# local imports
import move 
import scale
import helperFunc as helper
import normalize as norm

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
    
    
def populate_words():
    
    """
    Delete all records from database
    """
    connection = sqlite3.connect("db\\main_dataset.db") 
    crsr = connection.cursor() 
    sql_command = "DELETE FROM poseDataset;"
    crsr.execute(sql_command)
    connection.commit()  
    connection.close()
    
    print("records deleted, new records will be entered now")
    
    folders = []
    files = []
    fileNames=[]
    
    for entry in os.scandir('words_dataset'):
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
            pose = items["pose_keypoints_2d"]
            handRight = items["hand_right_keypoints_2d"]
            handLeft = items["hand_left_keypoints_2d"]
            
            
        # extract confidence points
        LeftConfPoints = helper.confidencePoints(handLeft)
        # add all confidence points
        LeftConfidence = helper.confidence(LeftConfPoints)    
            
        pose_points = helper.removePoints(pose)
        #posePoints = helper.join_points(pose_points)
        p1 = [pose_points[0], pose_points[1]]
        p2 = [pose_points[2], pose_points[3]]
        distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
        scaled_results,scaled_points = norm.scaleBody(pose_points,distance)
        poseResults,posePoints = norm.moveBody(scaled_results)
        
        
        hand_right_points = helper.removePoints(handRight)
        p1 = [hand_right_points[0], hand_right_points[1]]
        p2 = [hand_right_points[18], hand_right_points[19]]
        distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
        RightResult,Points = scale.scalePoints(hand_right_points,distance)
        handRightResults,handRightPoints = norm.move_to_wrist(RightResult,poseResults[8],poseResults[9])
        
        
        if LeftConfidence > 2:
            hand_left_points = helper.removePoints(handLeft)
            p1 = [hand_left_points[0], hand_left_points[1]]
            p2 = [hand_left_points[18], hand_left_points[19]]
            distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
            LeftResult,Points = scale.scalePoints(hand_left_points,distance)
            handLeftResults,handLeftPoints = norm.move_to_wrist(LeftResult,poseResults[14],poseResults[15])
        else:
            handLeftResults = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,]
    
        
      
       
        # SQL command to insert the data in the table 
        sql_command = "INSERT INTO poseDataset VALUES (NULL, "+ str(handRightResults[0]) + ", "+ str(handRightResults[1]) + ","+ str(handRightResults[2]) + ","+ str(handRightResults[3]) + ","+ str(handRightResults[4]) + ","+ str(handRightResults[5]) + ","+ str(handRightResults[6]) + ","+ str(handRightResults[7]) + ","+ str(handRightResults[8]) + ","+ str(handRightResults[9]) + ","+ str(handRightResults[10]) + ","+ str(handRightResults[11]) + ","+ str(handRightResults[12]) + ","+ str(handRightResults[13]) + ","+ str(handRightResults[14]) + ","+ str(handRightResults[15]) + ","+ str(handRightResults[16]) + ","+ str(handRightResults[17]) + ","+ str(handRightResults[18]) + ","+ str(handRightResults[19]) + ","+ str(handRightResults[20]) + ","+ str(handRightResults[21]) + ","+ str(handRightResults[22]) + ","+ str(handRightResults[23]) + ","+ str(handRightResults[24]) + ","+ str(handRightResults[25]) + ","+ str(handRightResults[26]) + ","+ str(handRightResults[27]) + ","+ str(handRightResults[28]) + ","+ str(handRightResults[29]) + ","+ str(handRightResults[30]) + ","+ str(handRightResults[31]) + ","+ str(handRightResults[32]) + ","+ str(handRightResults[33]) + ","+ str(handRightResults[34]) + ","+ str(handRightResults[35]) + ","+ str(handRightResults[36]) + ","+ str(handRightResults[37]) + ","+ str(handRightResults[38]) + ","+ str(handRightResults[39]) + ","+ str(handRightResults[40]) + ","+ str(handRightResults[41]) + ","+str(handLeftResults[0]) + ", "+ str(handLeftResults[1]) + ","+ str(handLeftResults[2]) + ","+ str(handLeftResults[3]) + ","+ str(handLeftResults[4]) + ","+ str(handLeftResults[5]) + ","+ str(handLeftResults[6]) + ","+ str(handLeftResults[7]) + ","+ str(handLeftResults[8]) + ","+ str(handLeftResults[9]) + ","+ str(handLeftResults[10]) + ","+ str(handLeftResults[11]) + ","+ str(handLeftResults[12]) + ","+ str(handLeftResults[13]) + ","+ str(handLeftResults[14]) + ","+ str(handLeftResults[15]) + ","+ str(handLeftResults[16]) + ","+ str(handLeftResults[17]) + ","+ str(handLeftResults[18]) + ","+ str(handLeftResults[19]) + ","+ str(handLeftResults[20]) + ","+ str(handLeftResults[21]) + ","+ str(handLeftResults[22]) + ","+ str(handLeftResults[23]) + ","+ str(handLeftResults[24]) + ","+ str(handLeftResults[25]) + ","+ str(handLeftResults[26]) + ","+ str(handLeftResults[27]) + ","+ str(handLeftResults[28]) + ","+ str(handLeftResults[29]) + ","+ str(handLeftResults[30]) + ","+ str(handLeftResults[31]) + ","+ str(handLeftResults[32]) + ","+ str(handLeftResults[33]) + ","+ str(handLeftResults[34]) + ","+ str(handLeftResults[35]) + ","+ str(handLeftResults[36]) + ","+ str(handLeftResults[37]) + ","+ str(handLeftResults[38]) + ","+ str(handLeftResults[39]) + ","+ str(handLeftResults[40]) + ","+ str(handLeftResults[41]) + ","+str(poseResults[0]) + ", "+ str(poseResults[1]) + ","+ str(poseResults[2]) + ","+ str(poseResults[3]) + ","+ str(poseResults[4]) + ","+ str(poseResults[5]) + ","+ str(poseResults[6]) + ","+ str(poseResults[7]) + ","+ str(poseResults[8]) + ","+ str(poseResults[9]) + ","+ str(poseResults[10]) + ","+ str(poseResults[11]) + ","+ str(poseResults[12]) + ","+ str(poseResults[13]) + ","+ str(poseResults[14]) + ","+ str(poseResults[15]) + ","+ str(poseResults[16]) + ","+ str(poseResults[17]) + ","+ str(poseResults[30]) + ","+ str(poseResults[31]) + ","+ str(poseResults[32]) + ","+ str(poseResults[33]) + ","+ str(poseResults[34]) + ","+ str(poseResults[35]) + ","+ str(poseResults[36]) + ","+ str(poseResults[37])  + ","+parentName+");"
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

def create_pose_table():
    connection = sqlite3.connect("db\\main_dataset.db")  
    crsr = connection.cursor() 
    
    sql_command1 = """CREATE TABLE IF NOT EXISTS poseDataset (  
     id INTEGER PRIMARY KEY,  
     Rx1 DOUBLE,
     Ry1 DOUBLE,
     Rx2 DOUBLE,
     Ry2 DOUBLE,  
     Rx3 DOUBLE,
     Ry3 DOUBLE,
     Rx4 DOUBLE,
     Ry4 DOUBLE,
     Rx5 DOUBLE,
     Ry5 DOUBLE,
     Rx6 DOUBLE,
     Ry6 DOUBLE,
     Rx7 DOUBLE,
     Ry7 DOUBLE,
     Rx8 DOUBLE,
     Ry8 DOUBLE,
     Rx9 DOUBLE,
     Ry9 DOUBLE,
     Rx10 DOUBLE,
     Ry10 DOUBLE,
     Rx11 DOUBLE,
     Ry11 DOUBLE,
     Rx12 DOUBLE,
     Ry12 DOUBLE,
     Rx13 DOUBLE,
     Ry13 DOUBLE,
     Rx14 DOUBLE,
     Ry14 DOUBLE,
     Rx15 DOUBLE,
     Ry15 DOUBLE,
     Rx16 DOUBLE,
     Ry16 DOUBLE,
     Rx17 DOUBLE,
     Ry17 DOUBLE,
     Rx18 DOUBLE,
     Ry18 DOUBLE,
     Rx19 DOUBLE,
     Ry19 DOUBLE,
     Rx20 DOUBLE,
     Ry20 DOUBLE,
     Rx21 DOUBLE,
     Ry21 DOUBLE,
     Lx1 DOUBLE,
     Ly1 DOUBLE,
     Lx2 DOUBLE,
     Ly2 DOUBLE,  
     Lx3 DOUBLE,
     Ly3 DOUBLE,
     Lx4 DOUBLE,
     Ly4 DOUBLE,
     Lx5 DOUBLE,
     Ly5 DOUBLE,
     Lx6 DOUBLE,
     Ly6 DOUBLE,
     Lx7 DOUBLE,
     Ly7 DOUBLE,
     Lx8 DOUBLE,
     Ly8 DOUBLE,
     Lx9 DOUBLE,
     Ly9 DOUBLE,
     Lx10 DOUBLE,
     Ly10 DOUBLE,
     Lx11 DOUBLE,
     Ly11 DOUBLE,
     Lx12 DOUBLE,
     Ly12 DOUBLE,
     Lx13 DOUBLE,
     Ly13 DOUBLE,
     Lx14 DOUBLE,
     Ly14 DOUBLE,
     Lx15 DOUBLE,
     Ly15 DOUBLE,
     Lx16 DOUBLE,
     Ly16 DOUBLE,
     Lx17 DOUBLE,
     Ly17 DOUBLE,
     Lx18 DOUBLE,
     Ly18 DOUBLE,
     Lx19 DOUBLE,
     Ly19 DOUBLE,
     Lx20 DOUBLE,
     Ly20 DOUBLE,
     Lx21 DOUBLE,
     Ly21 DOUBLE,
     Px1 DOUBLE,
     Py1 DOUBLE,
     Px2 DOUBLE,
     Py2 DOUBLE,  
     Px3 DOUBLE,
     Py3 DOUBLE,
     Px4 DOUBLE,
     Py4 DOUBLE,
     Px5 DOUBLE,
     Py5 DOUBLE,
     Px6 DOUBLE,
     Py6 DOUBLE,
     Px7 DOUBLE,
     Py7 DOUBLE,
     Px8 DOUBLE,
     Py8 DOUBLE,
     Px9 DOUBLE,
     Py9 DOUBLE,
     Px10 DOUBLE,
     Py10 DOUBLE,
     Px11 DOUBLE,
     Py11 DOUBLE,
     Px12 DOUBLE,
     Py12 DOUBLE,
     Px13 DOUBLE,
     Py13 DOUBLE,
    
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
    
    
 
    
    
    
    
    

            
            
            
            
            
            
            
            
            
    
    
    
    
    
    