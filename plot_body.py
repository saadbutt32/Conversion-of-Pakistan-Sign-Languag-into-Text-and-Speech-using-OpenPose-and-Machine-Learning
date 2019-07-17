# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 19:02:38 2019

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

from matplotlib import pyplot as plt


#POSE_PAIRS = [ [1,0],[1,2],[1,5],[2,3],[3,4],[5,6],[6,7],
#              [1,8],[8,9],[9,10],[1,11],[11,12],[12,13],
#              [0,14],[0,15],[14,16],[15,17]]





#folders = []
#files = []
#fileNames=[]
#
#Dir = 'dataset'
#
#files,fileNames,folders = helper.json_files(Dir)
#
#js = json.loads(open("test_images\\output\\346_keypoints.json").read())
#for items in js['people']:
#    pose = items["pose_keypoints_2d"]
#    handRight = items["hand_right_keypoints_2d"]
#    handLeft = items["hand_left_keypoints_2d"]
#
#pose_points = helper.removePoints(pose)
##posePoints = helper.join_points(pose_points)
#p1 = [pose_points[0], pose_points[1]]
#p2 = [pose_points[45], pose_points[46]]
#distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
#scaled_results,scaled_points = norm.scaleBody(pose_points,distance)
#poseResults,posePoints = norm.moveBody(scaled_results)
#
#
#hand_right_points = helper.removePoints(handRight)
##handRightPoints = helper.join_points(hand_right_points)
#p1 = [hand_right_points[0], hand_right_points[1]]
#p2 = [hand_right_points[18], hand_right_points[19]]
#distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
#RightResult,Points = scale.scalePoints(hand_right_points,distance)
#handRightResults,handRightPoints = norm.move_to_wrist(RightResult,poseResults[8],poseResults[9])
#
#hand_left_points = helper.removePoints(handLeft)
##handLeftPoints = helper.join_points(hand_left_points)
#p1 = [hand_left_points[0], hand_left_points[1]]
#p2 = [hand_left_points[18], hand_left_points[19]]
#distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
#LeftResult,Points = scale.scalePoints(hand_left_points,distance)
#handLeftResults,handLeftPoints = norm.move_to_wrist(LeftResult,poseResults[14],poseResults[15])

def plotPose(posePoints,handRightPoints,handLeftPoints):
    POSE_PAIRS = [ [1,0],[1,2],[1,5],[2,3],[3,4],[5,6],[6,7],
              [1,8],[0,15],[15,17],[0,16],[16,18]]

    HAND_PAIRS = [ [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],
                  [10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],
                  [18,19],[19,20] ]
    
    colors = [ [0, 0, 130], [0, 0, 175],[0,0, 210],[0, 0, 250] , 
              [0,200,160], [0,180,150],[0,230,186],[0,255,255],
                 [82,201,8], [82,204,0], [92,230,0], [102,252,6], 
                 [197,88,17], [204,82,0],[179,71,0],[227,94,5],
                 [204,0,163], [200,0,163], [196,0,163], [230,0,184]]
    
    

    color="black"
    color = color.capitalize()
    
    background = color+'_background.jpg'
        
    frame = cv2.imread(background)
    
    count=0
    # Draw Skeleton
    for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]
    
        if posePoints[partA] and posePoints[partB] and posePoints[partA][0]!=0 and posePoints[partA][1]!=0 and posePoints[partB][0]!=0 and posePoints[partB][1]!=0 :
            
            if color == 'White':
                cv2.line(frame, posePoints[partA], posePoints[partB], colors[count], 10)
                cv2.circle(frame, posePoints[partA], 5, colors[count], thickness=10, lineType=cv2.FILLED)
                cv2.circle(frame, posePoints[partB], 15, (0,0,0), thickness=5, lineType=-1)
                
            else:
                cv2.line(frame, posePoints[partA], posePoints[partB], colors[count], 10)
                cv2.circle(frame, posePoints[partA], 5, (0, 0, 255), thickness=10, lineType=cv2.FILLED)
                cv2.circle(frame, posePoints[partB], 5, (255, 255, 255), thickness=15, lineType=cv2.FILLED)
            count+=1
    
    count=0
    for pair in HAND_PAIRS:
        partA = pair[0]
        partB = pair[1]
    
        if handRightPoints[partA] and handRightPoints[partB]:
            
            if color == 'White':
                cv2.line(frame, handRightPoints[partA], handRightPoints[partB], colors[count], 10)
                cv2.circle(frame, handRightPoints[partA], 5, colors[count], thickness=10, lineType=cv2.FILLED)
                cv2.circle(frame, handRightPoints[partB], 15, (0,0,0), thickness=5, lineType=-1)
                
            else:
                cv2.line(frame, handRightPoints[partA], handRightPoints[partB], colors[count], 10)
                cv2.circle(frame, handRightPoints[partA], 5, (0, 0, 255), thickness=3, lineType=cv2.FILLED)
                cv2.circle(frame, handRightPoints[partB], 5, (255, 255, 255), thickness=4, lineType=cv2.FILLED)
            count+=1
            
    
    count=0
    for pair in HAND_PAIRS:
        partA = pair[0]
        partB = pair[1]
    
        if handLeftPoints[partA] and handLeftPoints[partB]:
            
            if color == 'White':
                cv2.line(frame, handLeftPoints[partA], handLeftPoints[partB], colors[count], 10)
                cv2.circle(frame, handLeftPoints[partA], 5, colors[count], thickness=10, lineType=cv2.FILLED)
                cv2.circle(frame, handLeftPoints[partB], 15, (0,0,0), thickness=5, lineType=-1)
                
            else:
                cv2.line(frame, handLeftPoints[partA], handLeftPoints[partB], colors[count], 10)
                cv2.circle(frame, handLeftPoints[partA], 5, (0, 0, 255), thickness=3, lineType=cv2.FILLED)
                cv2.circle(frame, handLeftPoints[partB], 5, (255, 255, 255), thickness=4, lineType=cv2.FILLED)
            count+=1
    
    
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    return frame


#frame = plotPose(pose_points,handRightPoints,handLeftPoints)
#
#fig2 = plt.figure(figsize = (30,30)) # create a 20 x 20 figure 
#ax3 = fig2.add_subplot(111)
#ax3.imshow(frame, interpolation='none')
#
#plt.imshow(frame)
#plt.show()



















