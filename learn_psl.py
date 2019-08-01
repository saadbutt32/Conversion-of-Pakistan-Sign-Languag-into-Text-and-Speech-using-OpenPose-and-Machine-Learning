# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 03:44:00 2019

"""
import PSL.alphabet_recognition.alphabet_recognition as alphabet
import PSL.helper.helperFunc as helper


from matplotlib import pyplot as plt
import cv2

import os
import subprocess
from tkinter import Label
import tkinter
import cv2
import PIL.Image, PIL.ImageTk

# for error handling
import errno, stat, shutil
import sys, signal

import json
import eel
import time


"""
Handling Errors While removing temp folders
"""     
def signal_handler(signal, frame):
    # Removing Keypoints Folder
    shutil.rmtree("Keypoints", ignore_errors=True, onerror=handleRemoveReadonly)
    shutil.rmtree("gui\\Learn_images", ignore_errors=True, onerror=handleRemoveReadonly)
    os.system("taskkill /f /im  OpenPoseDemo.exe")
    print( 'All done')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# if folder is read only raise exception
def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise Exception

# Remove temporary folder if exists
shutil.rmtree("gui\\Learn_images", ignore_errors=True, onerror=handleRemoveReadonly)
shutil.rmtree("Keypoints", ignore_errors=True, onerror=handleRemoveReadonly)


"""
labels and image files
"""
labels = ['ا','ب','پ','ت‬','ٹ‬','ث‬','ج‬','چ‬','ح‬','خ‬','د‬','ڈ‬','ذ‬','ر‬','ڑ‬','ز‬','ژ‬','س‬','ش‬','ص‬','ض‬','ط‬','ظ‬','ع‬','غ‬','ف‬','ق‬','ک‬','گ‬','ل‬','م‬','و‬','ء‬','ہ‬','ی‬','ے‬']

fileNames=[]
Dir = 'data\\learn'
for entry in os.scandir(Dir):
    if entry.is_file():
            fileNames.append(entry.path)


@eel.expose
def skip_Sign():
    global skip_sign
    skip_sign=True
    print("skip_sign")


@eel.expose
def openposelearn():
    """
    Starting OpenPoseDemo.exe
    and storing json files to temporary folder [Keypoints]
    """
    print('Starting OpenPose')
    os.chdir('bin\\openpose')
    subprocess.Popen('bin\\OpenPoseDemo.exe --hand  --write_json ..\\..\\Keypoints  --net_resolution 128x128  --number_people_max 1', shell=True)
    os.chdir('..\\..')
    
    

try:
    # Create target Directory
    os.mkdir("gui\\Learn_images")
except FileExistsError:
    print("Directory  already exists")



#POSE_PAIRS = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 5], [5, 6], [6, 7], [7, 8], [0, 9], [9, 10],
#              [10, 11], [11, 12], [0, 13], [13, 14], [14, 15], [15, 16], [0, 17], [17, 18],
#              [18, 19], [19, 20]]
#
#colors = [[0, 0, 130], [0, 0, 175], [0, 0, 210], [0, 0, 250],
#          [0, 200, 160], [0, 180, 150], [0, 230, 186], [0, 255, 255],
#          [82, 201, 8], [82, 204, 0], [92, 230, 0], [102, 252, 6],
#          [197, 88, 17], [204, 82, 0], [179, 71, 0], [227, 94, 5],
#          [204, 0, 163], [200, 0, 163], [196, 0, 163], [230, 0, 184]]

# read background image
#frame = cv2.imread("PSL\\BLACK_background.jpg")



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
    
    

    
    
    background = "PSL\\BLACK_background.jpg"
        
    frame = cv2.imread(background)
    
    count=0
    # Draw Skeleton
    for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]
    
        if posePoints[partA] and posePoints[partB] and posePoints[partA][0]!=0 and posePoints[partA][1]!=0 and posePoints[partB][0]!=0 and posePoints[partB][1]!=0 :
            cv2.line(frame, posePoints[partA], posePoints[partB], colors[count], 10)
            cv2.circle(frame, posePoints[partA], 5, (0, 0, 255), thickness=10, lineType=cv2.FILLED)
            cv2.circle(frame, posePoints[partB], 5, (255, 255, 255), thickness=15, lineType=cv2.FILLED)
        count+=1

    count=0
    for pair in HAND_PAIRS:
        partA = pair[0]
        partB = pair[1]
    
        if handRightPoints[partA] and handRightPoints[partB]:
            cv2.line(frame, handRightPoints[partA], handRightPoints[partB], colors[count], 10)
            cv2.circle(frame, handRightPoints[partA], 5, (0, 0, 255), thickness=3, lineType=cv2.FILLED)
            cv2.circle(frame, handRightPoints[partB], 5, (255, 255, 255), thickness=4, lineType=cv2.FILLED)
        count+=1
            
    
    count=0
    for pair in HAND_PAIRS:
        partA = pair[0]
        partB = pair[1]
    
        if handLeftPoints[partA] and handLeftPoints[partB]:
            cv2.line(frame, handLeftPoints[partA], handLeftPoints[partB], colors[count], 10)
            cv2.circle(frame, handLeftPoints[partA], 5, (0, 0, 255), thickness=3, lineType=cv2.FILLED)
            cv2.circle(frame, handLeftPoints[partB], 5, (255, 255, 255), thickness=4, lineType=cv2.FILLED)
        count+=1
    
    
#    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    return frame
    
@eel.expose
def learning():
    global skip_sign
    
    """
    storing json files to temporary folder [Keypoints]
    Creating temp folder and initializing with zero padded json file
    """
    
    dirName = 'Keypoints'
    fileName = 'PSL\\000000000000_keypoints.json'
    
    try:
        # Create target Directory
        os.mkdir(dirName)
        shutil.copy(fileName, dirName)
        print("Directory ", dirName, " Created ")
    except FileExistsError:
        print("Directory ", dirName, " already exists")

    label=''
    for x in range(len(fileNames)):


        skip_sign=False
        eel.get_Alphabet(x+1)

        while label!=labels[x]:
            
            for entry in os.scandir('Keypoints'):
                if entry.is_file():
                    if os.path.splitext(entry)[1] == ".json":
                        filePlotName = entry.name
            
            try:
                js = json.loads(open('Keypoints\\' + filePlotName).read())
            except ValueError:
                print ('Decoding JSON has failed')
                pass
                
            # extract 'hand_right_keypoints_2d' from json file
            for items in js['people']:
                pose = items["pose_keypoints_2d"]
                handRight = items["hand_right_keypoints_2d"]
                handLeft = items["hand_left_keypoints_2d"]
            
            pose_points = helper.removePoints(pose)
            posePoints = helper.join_points(pose_points)
            
            #  function to remove confidence points
            hand_right_Points = helper.removePoints(handRight)
            handRightPoints = helper.join_points(hand_right_Points)
            
            hand_left_points = helper.removePoints(handLeft)
            handLeftPoints = helper.join_points(hand_left_points)
            
            
            frame = plotPose(posePoints,handRightPoints,handLeftPoints)
            
            
            if hand_right_Points[0] != 0:
                cv2.imwrite('gui\\Learn_images\\'+filePlotName+'.jpg',frame)
                #reset image
                frame = cv2.imread("PSL\\BLACK_background.jpg")
                eel.get_fileName(filePlotName)
            
            eel.sleep(0.05)
                        
            if skip_sign == True:
                break
            try:

                for entry in os.scandir('Keypoints'):
                    if entry.is_file():
                        if os.path.splitext(entry)[1] == ".json":
                            fileName = entry.name

                try:
                    label = alphabet.match_ann('Keypoints\\'+fileName)
                except:
                    pass

                

            except UnboundLocalError:
                print("UnboundLocalError")

        eel.get_status()
        print("end while")

    return True
    
