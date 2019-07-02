# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 21:29:21 2019

"""
import os

def json_files(Dir):

    folders = []
    files = []
    fileNames=[]
    
    for entry in os.scandir(Dir):
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
                files.append(entry.path)
                fileNames.append(entry.name)
    return files,fileNames,folders

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



    
    








