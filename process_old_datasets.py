# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 00:22:51 2019

"""

# local imports
import db_helper as dbh
import helperFunc as helper
import move
import scale
import plot

# system imports
import cv2
import math
import os
import subprocess
import json
from matplotlib import pyplot as plt
import time
from datetime import datetime

# for error handling
import errno, stat, shutil
from distutils.dir_util import copy_tree
import sys, signal




"""
Remove files with confidence less then threshold
"""
conf_thershold = 13
folders = []
files = []
fileNames=[]

Dir = 'dataset_old'

for entry in os.scandir(Dir):
    if entry.is_dir():
        folders.append(entry.path)
        for entry1 in os.scandir(entry.path):
            if entry1.is_dir():
                folders.append(entry1.path)
            elif entry1.is_file():
                if os.path.splitext(entry1)[1] == ".json":
                    files.append(entry1.path)
                    fileNames.append(entry1.name)
    elif entry.is_file():
        if os.path.splitext(entry)[1] == ".json":
            files.append(entry.path)
            fileNames.append(entry.name)

count=0            
# traverse fileNames[]
for x in range(len(files)):
    # load each file from fileName[]
    js = json.loads(open(files[x]).read())
    # extract 'hand_right_keypoints_2d' from json file
    for items in js['people']:
        handRight = items["hand_right_keypoints_2d"]
    
    # extract confidence points
    confPoints = helper.confidencePoints(handRight)
    # add all confidence points
    confidence = helper.confidence(confPoints)
    
    # remove file if confidence is less than threshold
    if confidence < conf_thershold:
        os.remove(files[x])
        print(confidence)
        count+=1


print(str(count) + " files removed")



"""
plot remaining files
and delete if user inputs "N"  
"""   
# points to draw lines between
POSE_PAIRS = [ [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20] ]
background = 'big_background.png'
folders = []
files = []
fileNames=[]
#scan temporary folder
for entry in os.scandir(Dir):
    if entry.is_dir():
        folders.append(entry.path)
        for entry1 in os.scandir(entry.path):
            if entry1.is_dir():
                folders.append(entry1.path)
            elif entry1.is_file():
                if os.path.splitext(entry1)[1] == ".json":
                    files.append(entry1.path)
                    fileNames.append(entry1.name)
    elif entry.is_file():
        if os.path.splitext(entry)[1] == ".json":
            files.append(entry.path)
            fileNames.append(entry.name)
            

count=0
# read background image
frame = cv2.imread(background)
for x in range(len(files)):
    # load each file from fileName[]
    js = json.loads(open(files[x]).read())
    # extract 'hand_right_keypoints_2d' from json file
    for items in js['people']:
        handRight = items["hand_right_keypoints_2d"]
    
    #  function to remove confidence points
    handPoints = helper.removePoints(handRight)
     
    p1 = [handPoints[0], handPoints[1]]
    p2 = [handPoints[18], handPoints[19]]
    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
    
    Result,Points = scale.dummy_scalePoints(handPoints,distance)
   
    handRightResults,handRightPoints = move.dummy_centerPoints(Result)  

    split = (os.path.dirname(files[x])).split('\\')
    
    name = split[1]+'_'+fileNames[x]
    
    frame = plot.save_old_dataset(handRightPoints,'black',name) 
    count+=1













