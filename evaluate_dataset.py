# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 08:03:30 2019

"""
# local imports
import move 
import scale
import helperFunc as helper
import plot

# system imports
import os
import json 
import os.path
import math
from matplotlib import pyplot as plt

label = 'ب'
label = label.strip()

folders = []
files = []
fileNames=[]

Dir = 'temp_old_dataset\\'+label

files,fileNames,folders = helper.json_files(Dir)
            
parent = (os.path.dirname(files[1])).split('\\')
#print(parent[0]+"\\"+parent[1]+"\\"+parent[2])            
count=0
    
for file in files:
    js = json.loads(open(files[count]).read())
        
    parent = (os.path.dirname(files[count])).split('\\')
        
    parentName = "'"+parent[len(parent)-2]+"'"
        
    
    for items in js['people']:
        handRight = items["hand_right_keypoints_2d"]
    
    handPoints = helper.removePoints(handRight)
    p1 = [handPoints[0], handPoints[1]]
    p2 = [handPoints[18], handPoints[19]]
    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
    
    Result,Points = scale.dummy_scalePoints(handPoints,distance)
   
    handRightResults,handRightPoints = move.dummy_centerPoints(Result)            
            
            
    frame = plot.plot_dataset(handRightPoints,'black') 
    
    
    for x in range(len(frame)):
        # change the figure size
        fig2 = plt.figure(figsize = (20,20)) # create a 5 x 5 figure 
        ax3 = fig2.add_subplot(111)
        ax3.imshow(frame[x], interpolation='none')
        ax3.set_title(files[count])
        
        plt.show()
        
           
    count+=1    
   












      
            
            
            
            
            
            
            
            
            
            
            