# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 01:01:56 2019

"""

import sqlite3 
import cv2
import json
import math
import move
import scale
import helperFunc as helper
import os
import normalize as norm
import inverse_kinematics as ik
import rotate
import db_helper as dbh

from matplotlib import pyplot as plt


dbh.populate_words()

noLeftHand = False


folders = []
files = []
fileNames=[]

Dir = 'words_dataset'

files,fileNames,folders = helper.json_files(Dir)
# connecting to the database  
connection = sqlite3.connect("db\\main_dataset.db") 
# cursor  
crsr = connection.cursor() 

for x in range(len(files)):
    parent = ((files[x])).split('\\')
    parentName = "'"+parent[len(parent)-3]+"'"
    js = json.loads(open(files[x]).read())
    for items in js['people']:
        pose = items["pose_keypoints_2d"]
        handRight = items["hand_right_keypoints_2d"]
        handLeft = items["hand_left_keypoints_2d"]
    
    pose_points = helper.removePoints(pose)
    #posePoints = helper.join_points(pose_points)
    p1 = [pose_points[0], pose_points[1]]
    p2 = [pose_points[45], pose_points[46]]
    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
    scaled_results,scaled_points = norm.scaleBody(pose_points,distance)
    poseResults,posePoints = norm.moveBody(scaled_results)
    
    hand_right_points = helper.removePoints(handRight)
    p1 = [hand_right_points[0], hand_right_points[1]]
    p2 = [hand_right_points[18], hand_right_points[19]]
    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
    RightResult,Points = scale.scalePoints(hand_right_points,distance)
    handRightResults,handRightPoints = norm.move_to_wrist(RightResult,poseResults[8],poseResults[9])
    
    # extract confidence points
    RightConfPoints = helper.confidencePoints(handRight)
    LeftConfPoints = helper.confidencePoints(handLeft)
    # add all confidence points
    RightConfidence = helper.confidence(RightConfPoints)
    LeftConfidence = helper.confidence(LeftConfPoints)  
        
    if LeftConfidence > 3:
        hand_left_points = helper.removePoints(handLeft)
        p1 = [hand_left_points[0], hand_left_points[1]]
        p2 = [hand_left_points[18], hand_left_points[19]]
        distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
        if distance != 0: 
            LeftResult,Points = scale.scalePoints(hand_left_points,distance)
            handLeftResults,handLeftPoints = norm.move_to_wrist(LeftResult,poseResults[14],poseResults[15])
        else: 
            handLeftResults,handLeftPoints = norm.move_to_wrist(hand_left_points,poseResults[14],poseResults[15])
    
    else:
        noLeftHand = True
        handLeftPoints = [(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0)]
        handLeftResults = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,]
    
    addX = 0
    addY = 0
    for x in range(6):
        populate = True
        
        if x==0:
            addX = -80
            addY = 0
        if x==1:
            addX = 80
            addY = 0
        if x==2:
            addX = 0
            addY = -80
        if x==3:
            addX = 0
            addY = 80
        if x==4:
            addX = 80
            addY = 80
        if x==5:
            addX = -80
            addY = -80
        
        
        
        if noLeftHand == False:
            handRightResults,handRightPoints = move.movePoints(handRightResults,addX,addY)
        elif noLeftHand == True:
            handRightResults,handRightPoints,handLeftResults,handLeftPoints = move.moveBothHands(handRightResults,handLeftResults,addX,addY)
        
        """
        inverse Kinematics rightArm
        """
        
        p4 = poseResults[4]
        p5 = poseResults[5]
        
        p6 = poseResults[6]
        p7 = poseResults[7]
        
        p8 = poseResults[8]
        p9 = poseResults[9]
        
        p1 = [p4, p5]
        p2 = [0, 0]
        distanceX = p1[0]-p2[0]
        distanceY = p1[1]-p2[1]
        
        p4 -= distanceX
        p5 -= distanceY
        
        p6 -= distanceX
        p7 -= distanceY
        
        p8 -= distanceX
        p9 -= distanceY
        
        
        p1 = [p4, p5]
        p2 = [p6, p7]
        d1 = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
        
        p1 = [p6, p7]
        p2 = [p8, p9]
        d2 = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
        
        
        a1 = d1  # length of link a1
        a2 = d2 # length of link a2 
        
        
        
        # Desired Position of End effector
        x = handRightResults[0]
        x -= distanceX
        y = handRightResults[1]
        y -= distanceY
        
        
        angle = ik.get_angle(x,y,a1,a2)
        
        
        posePoints[3] = (int(posePoints[2][0]+a1),int(posePoints[2][1]))
        poseResults[6] = posePoints[2][0]+a1
        poseResults[7] = posePoints[2][1]
        
        posePoints[4] = (int(posePoints[3][0]+a2),int(posePoints[3][1]))
        poseResults[8] = posePoints[3][0]+a2
        poseResults[9] = posePoints[3][1]
        
        
        point4 = rotate.rotate(posePoints[4],angle[1],posePoints[3])
        posePoints[4] = (int(point4[0]),int(point4[1]))
        poseResults[8] = point4[0]
        poseResults[9] = point4[1]
        
        point3 = rotate.rotate(posePoints[3],angle[0],posePoints[2])
        point4 = rotate.rotate(posePoints[4],angle[0],posePoints[2])
        
        posePoints[3] = (int(point3[0]),int(point3[1]))
        poseResults[6] = point3[0]
        poseResults[7] = point3[1]
        
        posePoints[4] = (int(point4[0]),int(point4[1]))
        poseResults[8] = point4[0]
        poseResults[9] = point4[1]
        
        
        a = a1
        b = a2 
        p1 = [pose_points[4], pose_points[5]]
        p2 = [pose_points[8], pose_points[9]]
        c = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
        
        try:
            angleC = math.degrees( math.acos( (a**2 + b**2 - c**2)/(2*a*b) ) )
            
            if (posePoints[3][0] > posePoints[2][0]-200) and posePoints[3][1] > 300 and posePoints[3][1] < 600:
                point3 = rotate.rotate(posePoints[3],180-angleC,posePoints[2])
                
                posePoints[3] = (int(point3[0]),int(point3[1]))
                poseResults[6] = point3[0]
                poseResults[7] = point3[1]  
                
                print("in condition 1")
                
            if posePoints[3][1] < 300 and posePoints[3][0] < posePoints[1][0]:
                point3 = rotate.rotate(posePoints[3],270-angleC,posePoints[2])
                
                posePoints[3] = (int(point3[0]),int(point3[1]))
                poseResults[6] = point3[0]
                poseResults[7] = point3[1]
                
                print("in condition 2")    
            
            if posePoints[3][0] > posePoints[1][0]:
                point3 = rotate.rotate(posePoints[3],90-angleC,posePoints[2])
                
                posePoints[3] = (int(point3[0]),int(point3[1]))
                poseResults[6] = point3[0]
                poseResults[7] = point3[1]
                
                print("in condition 3")
        except:
            populate=False
            pass
         
        
        if noLeftHand == True:
            """
            inverse Kinematics leftArm
            """
            
            p4 = poseResults[10]
            p5 = poseResults[11]
            
            p6 = poseResults[12]
            p7 = poseResults[13]
            
            p8 = poseResults[14]
            p9 = poseResults[15]
            
            p1 = [p4, p5]
            p2 = [0, 0]
            distanceX = p1[0]-p2[0]
            distanceY = p1[1]-p2[1]
            
            p4 -= distanceX
            p5 -= distanceY
            
            p6 -= distanceX
            p7 -= distanceY
            
            p8 -= distanceX
            p9 -= distanceY
            
            
            p1 = [p4, p5]
            p2 = [p6, p7]
            d1 = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
            
            p1 = [p6, p7]
            p2 = [p8, p9]
            d2 = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
            
            
            a1 = d1  # length of link a1
            a2 = d2 # length of link a2 
            
            
            
            # Desired Position of End effector
            x = handLeftResults[0]
            x -= distanceX
            y = handLeftResults[1]
            y -= distanceY
            
            
            angle = ik.get_angle(x,y,a1,a2)
            
            
            
            
            posePoints[6] = (int(posePoints[5][0]+a1),int(posePoints[5][1]))
            poseResults[12] = posePoints[5][0]+a1
            poseResults[13] = posePoints[5][1]
            
            posePoints[7] = (int(posePoints[6][0]+a2),int(posePoints[6][1]))
            poseResults[14] = posePoints[6][0]+a2
            poseResults[15] = posePoints[6][1]
            
            
            point4 = rotate.rotate(posePoints[7],angle[1],posePoints[6])
            posePoints[7] = (int(point4[0]),int(point4[1]))
            poseResults[14] = point4[0]
            poseResults[15] = point4[1]
            
            point3 = rotate.rotate(posePoints[6],angle[0],posePoints[5])
            point4 = rotate.rotate(posePoints[7],angle[0],posePoints[5])
            
            posePoints[6] = (int(point3[0]),int(point3[1]))
            poseResults[12] = point3[0]
            poseResults[13] = point3[1]
            
            posePoints[7] = (int(point4[0]),int(point4[1]))
            poseResults[14] = point4[0]
            poseResults[15] = point4[1]
            
            
            a = a1
            b = a2 
            p1 = [pose_points[10], pose_points[11]]
            p2 = [pose_points[14], pose_points[15]]
            c = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
            
            
            #angleC = math.degrees( math.acos( (a**2 + b**2 - c**2)/(2*a*b) ) )
            
            #if (posePoints[3][0] > posePoints[2][0]-200) and posePoints[3][1] > 300:
            #    point3 = rotate.rotate(posePoints[3],180-angleC,posePoints[2])
            #    posePoints[3] = (int(point3[0]),int(point3[1]))
            #    print("in condition 1")
            #    
            #if posePoints[3][1] < 300 and posePoints[3][0] < posePoints[1][0]:
            #    point3 = rotate.rotate(posePoints[3],270-angleC,posePoints[2])
            #    posePoints[3] = (int(point3[0]),int(point3[1]))
            #    print("in condition 2")    
            #
            #if posePoints[3][0] > posePoints[1][0]:
            #    point3 = rotate.rotate(posePoints[3],90-angleC,posePoints[2])
            #    posePoints[3] = (int(point3[0]),int(point3[1]))
            #    print("in condition 3")    
        
            
        if populate== True:
            # SQL command to insert the data in the table 
            sql_command = "INSERT INTO poseDataset VALUES (NULL, "+ str(handRightResults[0]) + ", "+ str(handRightResults[1]) + ","+ str(handRightResults[2]) + ","+ str(handRightResults[3]) + ","+ str(handRightResults[4]) + ","+ str(handRightResults[5]) + ","+ str(handRightResults[6]) + ","+ str(handRightResults[7]) + ","+ str(handRightResults[8]) + ","+ str(handRightResults[9]) + ","+ str(handRightResults[10]) + ","+ str(handRightResults[11]) + ","+ str(handRightResults[12]) + ","+ str(handRightResults[13]) + ","+ str(handRightResults[14]) + ","+ str(handRightResults[15]) + ","+ str(handRightResults[16]) + ","+ str(handRightResults[17]) + ","+ str(handRightResults[18]) + ","+ str(handRightResults[19]) + ","+ str(handRightResults[20]) + ","+ str(handRightResults[21]) + ","+ str(handRightResults[22]) + ","+ str(handRightResults[23]) + ","+ str(handRightResults[24]) + ","+ str(handRightResults[25]) + ","+ str(handRightResults[26]) + ","+ str(handRightResults[27]) + ","+ str(handRightResults[28]) + ","+ str(handRightResults[29]) + ","+ str(handRightResults[30]) + ","+ str(handRightResults[31]) + ","+ str(handRightResults[32]) + ","+ str(handRightResults[33]) + ","+ str(handRightResults[34]) + ","+ str(handRightResults[35]) + ","+ str(handRightResults[36]) + ","+ str(handRightResults[37]) + ","+ str(handRightResults[38]) + ","+ str(handRightResults[39]) + ","+ str(handRightResults[40]) + ","+ str(handRightResults[41]) + ","+str(handLeftResults[0]) + ", "+ str(handLeftResults[1]) + ","+ str(handLeftResults[2]) + ","+ str(handLeftResults[3]) + ","+ str(handLeftResults[4]) + ","+ str(handLeftResults[5]) + ","+ str(handLeftResults[6]) + ","+ str(handLeftResults[7]) + ","+ str(handLeftResults[8]) + ","+ str(handLeftResults[9]) + ","+ str(handLeftResults[10]) + ","+ str(handLeftResults[11]) + ","+ str(handLeftResults[12]) + ","+ str(handLeftResults[13]) + ","+ str(handLeftResults[14]) + ","+ str(handLeftResults[15]) + ","+ str(handLeftResults[16]) + ","+ str(handLeftResults[17]) + ","+ str(handLeftResults[18]) + ","+ str(handLeftResults[19]) + ","+ str(handLeftResults[20]) + ","+ str(handLeftResults[21]) + ","+ str(handLeftResults[22]) + ","+ str(handLeftResults[23]) + ","+ str(handLeftResults[24]) + ","+ str(handLeftResults[25]) + ","+ str(handLeftResults[26]) + ","+ str(handLeftResults[27]) + ","+ str(handLeftResults[28]) + ","+ str(handLeftResults[29]) + ","+ str(handLeftResults[30]) + ","+ str(handLeftResults[31]) + ","+ str(handLeftResults[32]) + ","+ str(handLeftResults[33]) + ","+ str(handLeftResults[34]) + ","+ str(handLeftResults[35]) + ","+ str(handLeftResults[36]) + ","+ str(handLeftResults[37]) + ","+ str(handLeftResults[38]) + ","+ str(handLeftResults[39]) + ","+ str(handLeftResults[40]) + ","+ str(handLeftResults[41]) + ","+str(poseResults[0]) + ", "+ str(poseResults[1]) + ","+ str(poseResults[2]) + ","+ str(poseResults[3]) + ","+ str(poseResults[4]) + ","+ str(poseResults[5]) + ","+ str(poseResults[6]) + ","+ str(poseResults[7]) + ","+ str(poseResults[8]) + ","+ str(poseResults[9]) + ","+ str(poseResults[10]) + ","+ str(poseResults[11]) + ","+ str(poseResults[12]) + ","+ str(poseResults[13]) + ","+ str(poseResults[14]) + ","+ str(poseResults[15]) + ","+ str(poseResults[16]) + ","+ str(poseResults[17]) + ","+ str(poseResults[30]) + ","+ str(poseResults[31]) + ","+ str(poseResults[32]) + ","+ str(poseResults[33]) + ","+ str(poseResults[34]) + ","+ str(poseResults[35]) + ","+ str(poseResults[36]) + ","+ str(poseResults[37])  + ","+parentName+");"
            crsr.execute(sql_command)  


connection.commit()  
connection.close() 
























































