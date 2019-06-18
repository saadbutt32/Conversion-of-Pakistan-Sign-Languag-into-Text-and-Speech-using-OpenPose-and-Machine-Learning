# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 21:29:21 2019

"""

def removePoints(handRight):
    
    handRightResults = []
    handRightX = []
    handRightY = []
    
    for x in range(0,len(handRight),3): 
        handRightX.append(handRight[x])
    for x in range(1,len(handRight),3): 
        handRightY.append(handRight[x])
    
    for x in range(len(handRightX)): 
        handRightResults.append(handRightX[x])
        handRightResults.append(handRightY[x])

    return handRightResults


def getCoordPoints(handRight):
    
    handRightPoints = []
    handRightX = []
    handRightY = []
    
    for x in range(0,len(handRight),3): 
        handRightX.append(handRight[x])
    for x in range(1,len(handRight),3): 
        handRightY.append(handRight[x])
    
    for x in range(len(handRightX)): 
       handRightPoints.append((int(handRightX[x]) , int(handRightY[x]))) 

    return handRightPoints

def confidencePoints(handRight):
    handRightC= []
    for x in range(2,len(handRight),3): 
        handRightC.append(handRight[x])
    
    return handRightC

def confidence(handRight):
    sum = handRight[0]
    for x in range(1,len(handRight)): 
        sum += handRight[x]
    
    return sum



    
    








