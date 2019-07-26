# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 12:09:53 2019

"""

# local imports
import db_helper as dbh
import helperFunc as helper
import move
import scale
import plot
import normalize as norm
import plot_body

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
Handling Errors While removing temp folders
"""     
def signal_handler(signal, frame):
    # Removing Keypoints Folder
    shutil.rmtree("Keypoints", ignore_errors=True, onerror=handleRemoveReadonly)
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


""" 
Remove 'Keypoints_temp' folder if exists
"""

shutil.rmtree("Keypoints_temp", ignore_errors=True, onerror=handleRemoveReadonly)

      
"""
Starting OpenPoseDemo.exe
and storing json files to temporary folder [Keypoints_temp] 
"""
sec = int(input('Enter Seconds OpenPose should run for : '))
os.chdir('openpose')
print('Starting OpenPose')
output = subprocess.Popen('build\\x64\\Release\\OpenPoseDemo.exe --hand  --write_json ..\\Keypoints_temp  --net_resolution 128x128  --number_people_max 1', shell=True)
os.chdir('..')


"""
Creating temp folder and initializing with zero padded json file
"""
dirName = 'Keypoints_temp'
init_file = '000000000000_keypoints.json'

try:
    # Create target Directory
    os.mkdir(dirName)
    # copy initializing file in directory
    shutil.copy(init_file, dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")
    
#  wait for openpose to start     
time.sleep(5) 
#  wait for user  
time.sleep(sec) 
#  Kill openpose
os.system("taskkill /f /im  OpenPoseDemo.exe")


"""
Remove files with confidence less then threshold
"""
conf_thershold = 10
fileNames = []
#scan temporary folder
for entry in os.scandir('Keypoints_temp'):
    # store the name if entry is file and file is of ext .json
    if entry.is_file():
        if os.path.splitext(entry)[1] == ".json":
            fileNames.append(entry.name)
            
# traverse fileNames[]
for x in range(len(fileNames)):
    # load each file from fileName[]
    js = json.loads(open('Keypoints_temp\\' + fileNames[x]).read())
    # extract 'hand_right_keypoints_2d' from json file
    for items in js['people']:
        handRight = items["hand_right_keypoints_2d"]
        handLeft = items["hand_left_keypoints_2d"]
    
    # extract confidence points
    RightConfPoints = helper.confidencePoints(handRight)
    LeftConfPoints = helper.confidencePoints(handLeft)
    # add all confidence points
    RightConfidence = helper.confidence(RightConfPoints)
    LeftConfidence = helper.confidence(LeftConfPoints)
    # remove file if confidence is less than threshold
    if RightConfidence < 10:
        os.remove('Keypoints_temp\\' + fileNames[x])
        
    elif LeftConfidence < conf_thershold and LeftConfidence > 2 :
        os.remove('Keypoints_temp\\' + fileNames[x])   

    

"""
plot remaining files
and delete if user inputs "N"  
"""   
# points to draw lines between
POSE_PAIRS = [ [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20] ]
background = 'big_background.png'
fileNames = []
#scan temporary folder
for entry in os.scandir('Keypoints_temp'):
    # store the name if entry is file and file is of ext .json
    if entry.is_file():
        if os.path.splitext(entry)[1] == ".json":
            fileNames.append(entry.name)
            

# read background image
frame = cv2.imread(background)
for x in range(len(fileNames)):
    # load each file from fileName[]
    js = json.loads(open('Keypoints_temp\\' + fileNames[x]).read())
    # extract 'hand_right_keypoints_2d' from json file
    for items in js['people']:
        pose = items["pose_keypoints_2d"]
        handRight = items["hand_right_keypoints_2d"]
        handLeft = items["hand_left_keypoints_2d"]
        
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
        handLeftPoints = [(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0)]
        handLeftResults = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,]
    

    
    
    frame = plot_body.plotPose(posePoints,handRightPoints,handLeftPoints) 
    
    
    fig2 = plt.figure(figsize = (15,15)) # create a 20 x 20 figure 
    ax3 = fig2.add_subplot(111)
    ax3.imshow(frame, interpolation='none')
    
    plt.imshow(frame)
    plt.show()
    
    
    
    # delete file if user rejects it
    choice = input('do you want to keep it? Y/N: ')
    if choice == 'N' or choice == 'n':
        os.remove('Keypoints_temp\\' + fileNames[x])
        print("File Removed")

# store label
label = input('Enter label for these files: ')
# remove whitespaces
label = label.strip()

choice = input('do you want to put label = '+label+' ? Y/N: ')
if choice == 'N' or choice == 'n':
    # store label
    label = input('Enter label for these files: ')
    # remove whitespaces
    label = label.strip()
elif choice == 'Y' or choice == 'y':
    """
    traverse 'dataset' folder ,
    find subfolder matching 'label' ,
    create folder with timestamp in  matched folder , 
    and copy everything from 'Keypoints_temp' to created folder
    """
    for entry in os.scandir('words_dataset'):
        if entry.name == label:
            # current date and time
            now = datetime.now()
            
            # create folder with timestamp
            timestamp =  str(datetime.timestamp(now))
            dir_name = "words_dataset\\" + entry.name +"\\"+ timestamp
            try:
                # Create target Directory
                os.mkdir(dir_name)
                print("Directory " , dir_name ,  " Created ") 
            except FileExistsError:
                print("Directory " , dir_name ,  " already exists")
                
            # copy everything from 'Keypoints_temp' to created folder    
            copy_tree("Keypoints_temp", "words_dataset\\" + entry.name + "\\" + timestamp )
    
    
    # create table if not exists
    dbh.create_pose_table()
    # add all records from 'dataset' to 'db\main_databse.db'
    dbh.populate_words()
    
    
    
""" 
Remove 'Keypoints_temp' folder 
"""

shutil.rmtree("Keypoints_temp", ignore_errors=True, onerror=handleRemoveReadonly)
print( 'Keypoints_temp folder removed')

        






