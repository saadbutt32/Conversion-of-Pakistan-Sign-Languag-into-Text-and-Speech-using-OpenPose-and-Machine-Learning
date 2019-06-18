# -*- coding: utf-8 -*-
"""
Created on Sat Dec 15 04:37:04 2018

"""
import sqlite3 
import cv2
import json
import math
import move
import scale
import helperFunc as helper
from matplotlib import pyplot as plt

POSE_PAIRS = [ [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20] ]

def plot_skeleton(fileName,background,isMove,isScale):
    js = json.loads(open(fileName).read())
    for items in js['people']:
        handRight = items["hand_right_keypoints_2d"]
    
    handCoord = helper.getCoordPoints(handRight)
    handPoints = helper.removePoints(handRight)
    
    p1 = [handPoints[0], handPoints[1]]
    p2 = [handPoints[18], handPoints[19]]
    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
    
    
    if isScale:
       handRightResult,handRightPoints = scale.scalePoints(handPoints,distance)
    else:
        handRightResult = handPoints
        handRightPoints = handCoord  
    
    if isMove:
        handRightResult,handRightPoints = move.centerPoints(handRightResult)
     
    
    p1 = [handRightResult[0], handRightResult[1]]
    p2 = [handRightResult[18], handRightResult[19]]
    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
    
#    print(distance)
#    print(handPoints)
#    print(handRightPoints)
   
    
#    print(handRightResult)   
#    p1 = [handRightResult[0], handRightResult[1]]
#    p2 = [handRightResult[17], handRightResult[18]]
#    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
#    
#    print(distance,handRightResult[0],handRightResult[1],handRightResult[17],handRightResult[18])
#    
#    
#    
#    
#    print(handRightResult)
#    
#    p1 = [handRightResult[0], handRightResult[1]]
#    p2 = [handRightResult[17], handRightResult[18]]
#    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
#    
#    print(distance)
    
    
#    p1 = [Result[0], Result[1]]
#    p2 = [Result[17], Result[18]]
#    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
#    
#    print(distance)
#    print("\n\n")
#    print(handRightPoints)
    
    
    frame = cv2.imread('C:\\123Drive\\Python\\Sign_Language_Interpreter\\' + background)
#    frame2 = frame
    
    ## for croping image
    #maxX = int(max(handrightX))+20
    #maxY = int(max(handrightY))+20
    
    #print(maxX)
    #print(maxY)
    #
    #crop = frame[0:78,0:52]
    #
    
    # Draw Skeleton
    for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]
    
        if handRightPoints[partA] and handRightPoints[partB]:
            cv2.line(frame, handRightPoints[partA], handRightPoints[partB], (0, 255, 255), 2)
            cv2.circle(frame, handRightPoints[partA], 5, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
            cv2.circle(frame, handRightPoints[partB], 5, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
    
#    # Draw line
#    
#    cv2.line(frame2, handRightPoints[0], handRightPoints[8], (0, 255, 255), 2)
#    cv2.circle(frame2, handRightPoints[0], 5, (255, 255, 255), thickness=-1, lineType=cv2.FILLED)
#    cv2.circle(frame2, handRightPoints[9], 5, (255, 255, 255), thickness=-1, lineType=cv2.FILLED)
#    
    #cv2.imwrite('test_test.jpg',frame)
    return frame


def plot_points(points,background):
    
    handRight = points
    handRightPoints = []
    handRightX = []
    handRightY = []
    for x in range(0,len(handRight),2): 
        handRightX.append(handRight[x])
    for x in range(1,len(handRight),2): 
        handRightY.append(handRight[x])
    
    for x in range(len(handRightX)): 
        handRightPoints.append((int(handRightX[x]) , int(handRightY[x]))) 
    
    frame = cv2.imread('C:\\123Drive\\Python\\Sign_Language_Interpreter\\' + background)
#    frame2 = frame
    
    ## for croping image
    #maxX = int(max(handrightX))+20
    #maxY = int(max(handrightY))+20
    
    #print(maxX)
    #print(maxY)
    #
    #crop = frame[0:78,0:52]
    #
    
    # Draw Skeleton
    for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]
    
        if handRightPoints[partA] and handRightPoints[partB]:
            cv2.line(frame, handRightPoints[partA], handRightPoints[partB], (0, 255, 255), 2)
            cv2.circle(frame, handRightPoints[partA], 5, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
#            cv2.circle(frame, handRightPoints[partB], 5, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
#    # Draw line
#    
#    cv2.line(frame2, handRightPoints[0], handRightPoints[8], (0, 255, 255), 2)
#    cv2.circle(frame2, handRightPoints[0], 5, (255, 255, 255), thickness=-1, lineType=cv2.FILLED)
#    cv2.circle(frame2, handRightPoints[9], 5, (255, 255, 255), thickness=-1, lineType=cv2.FILLED)
            
    
    #cv2.imwrite('test_test.jpg',frame)
    return frame



def plot_db():
    
    ret_frame = []
    POSE_PAIRS = [ [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20] ]
    background = 'big_background.png'
    connection = sqlite3.connect("db\\main_dataset.db") 
    crsr = connection.cursor()
    
    sql = 'SELECT x1,y1'
    for x in range(2,22):
        sql = sql + ',x'+str(x)+',y'+str(x)
    sql = sql + ' FROM rightHandDataset WHERE 1'
    
    crsr.execute(sql)
    feature_res = crsr.fetchall()
    
    for x in range(len(feature_res)):
        points = feature_res[x]
        
        handRight = points
        handRightPoints = []
        handRightX = []
        handRightY = []
        for x in range(0,len(handRight),2): 
            handRightX.append(handRight[x])
        for x in range(1,len(handRight),2): 
            handRightY.append(handRight[x])
        
        for x in range(len(handRightX)): 
            handRightPoints.append((int(handRightX[x]) , int(handRightY[x]))) 
        
        frame = cv2.imread(background)
        
        # Draw Skeleton
        for pair in POSE_PAIRS:
            partA = pair[0]
            partB = pair[1]
        
            if handRightPoints[partA] and handRightPoints[partB]:
                cv2.line(frame, handRightPoints[partA], handRightPoints[partB], (0, 255, 255), 2)
                cv2.circle(frame, handRightPoints[partA], 5, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
                cv2.circle(frame, handRightPoints[partB], 5, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
                
        # adjust cv2 colors        
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        # plot lines on backdround
#        plt.imshow(frame)
#        plt.show()
        
        ret_frame.append(frame)
        
        # reset background
        frame = cv2.imread(background)
        
        
    return ret_frame






































































