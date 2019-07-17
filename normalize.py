# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 10:28:14 2019

"""
# wristX = pose[12],  wirstY = pose[13]
def move_to_wrist(handRight,wristX,wristY):
    refX = wristX
    refY= wristY
    
    handRightResults = []
    handRightPoints = []
    handRightX = []
    handRightY = []
    
    for x in range(0,len(handRight),2): 
        handRightX.append(handRight[x])
    for x in range(1,len(handRight),2): 
        handRightY.append(handRight[x])  
        
    p1 = [handRightX[0], handRightY[0]]
    p2 = [refX, refY]
    distanceX = p1[0]-p2[0]
    distanceY = p1[1]-p2[1]
    
    for x in range(len(handRightX)):
        handRightX[x] -= distanceX
     
    for x in range(len(handRightY)):
        handRightY[x] -= distanceY
    
    # storing computed keypoints
    for x in range(len(handRightX)): 
        handRightPoints.append((int(handRightX[x]) , int(handRightY[x]))) 
        handRightResults.append(handRightX[x])
        handRightResults.append(handRightY[x])

    return handRightResults,handRightPoints



def scaleBody(handRight,distance):
   
    ref = 200
    
    handRightResults = []
    handRightPoints = []
    handRightX = []
    handRightY = []
#    handRightC = []
#    threshold = 0
    for x in range(0,len(handRight),2): 
        handRightX.append(handRight[x])
    for x in range(1,len(handRight),2): 
        handRightY.append(handRight[x])
#    for x in range(2,len(handRight),3): 
#        handRightC.append(handRight[x]) 
    
    scale = ref/distance
    #print(scale)  
    
    for x in range(len(handRightX)):
        handRightX[x] *=scale
            
    for x in range(len(handRightY)):
        handRightY[x] *=scale
            
    
#    for x in range(len(handRightY)):
#        handRightX[x] *=2
#        handRightY[x] *=2
    
            
    # storing computed keypoints
    for x in range(len(handRightX)): 
        #if handRightC[x] > threshold:
            handRightPoints.append((int(handRightX[x]) , int(handRightY[x]))) 
            handRightResults.append(handRightX[x])
            handRightResults.append(handRightY[x])
#        else:
#            handRightResults.append(None) 
            
    return handRightResults,handRightPoints

def moveBody(handRight):
    
    refX = 1000
    refY=400
    
    handRightResults = []
    handRightPoints = []
    handRightX = []
    handRightY = []
    
    for x in range(0,len(handRight),2): 
        handRightX.append(handRight[x])
    for x in range(1,len(handRight),2): 
        handRightY.append(handRight[x])  
        
    p1 = [handRightX[1], handRightY[1]]
    p2 = [refX, refY]
    distanceX = p1[0]-p2[0]
    distanceY = p1[1]-p2[1]
    
    for x in range(len(handRightX)):
        if handRightX[x] != 0:
            handRightX[x] -= distanceX
     
    for x in range(len(handRightY)):
        if handRightY[x] != 0:
            handRightY[x] -= distanceY
    
    # storing computed keypoints
    for x in range(len(handRightX)): 
        handRightPoints.append((int(handRightX[x]) , int(handRightY[x]))) 
        handRightResults.append(handRightX[x])
        handRightResults.append(handRightY[x])

    return handRightResults,handRightPoints














