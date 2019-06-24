
# -*- coding: utf-8 -*-

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
    
    # extract confidence points
    confPoints = helper.confidencePoints(handRight)
    # add all confidence points
    confidence = helper.confidence(confPoints)
    print(confidence)
    # remove file if confidence is less than threshold
    if confidence < conf_thershold:
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
        handRight = items["hand_right_keypoints_2d"]
    
    #  function to remove confidence points
    handPoints = helper.removePoints(handRight)
     
    p1 = [handPoints[0], handPoints[1]]
    p2 = [handPoints[18], handPoints[19]]
    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
    
    Result,Points = scale.dummy_scalePoints(handPoints,distance)
   
    handRightResults,handRightPoints = move.dummy_centerPoints(Result)  

    
    
    frame = plot.plot_dataset(handRightPoints,'black') 
    
    
    for i in range(len(frame)):
        # change the figure size
        fig2 = plt.figure(figsize = (20,20)) # create a 5 x 5 figure 
        ax3 = fig2.add_subplot(111)
        ax3.imshow(frame[i], interpolation='none')
        ax3.set_title(fileNames[x])
        
        plt.show()
    
    '''
    Depreciated code
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    '''
    #print("input " + fileNames[x])
    # Draw lines
#    for pair in POSE_PAIRS:
#        partA = pair[0]
#        partB = pair[1]
#    
#        if handRightPoints[partA] and handRightPoints[partB]:
#            cv2.line(frame, handRightPoints[partA], handRightPoints[partB], (0, 255, 255), 7)
#            cv2.circle(frame, handRightPoints[partA], 5, (0, 0, 255), thickness=4, lineType=cv2.FILLED)
#            cv2.circle(frame, handRightPoints[partB], 5, (255, 255, 255), thickness=3, lineType=cv2.FILLED)
#    
#    # adjust cv2 colors        
#    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
#    # plot lines on backdround
#    plt.imshow(frame)
#    plt.show()
#    # reset background
#    frame = cv2.imread(background)
    '''
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    '''
    
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
    for entry in os.scandir('dataset'):
        if entry.name == label:
            # current date and time
            now = datetime.now()
            
            # create folder with timestamp
            timestamp =  str(datetime.timestamp(now))
            dir_name = "dataset\\" + entry.name +"\\"+ timestamp
            try:
                # Create target Directory
                os.mkdir(dir_name)
                print("Directory " , dir_name ,  " Created ") 
            except FileExistsError:
                print("Directory " , dir_name ,  " already exists")
                
            # copy everything from 'Keypoints_temp' to created folder    
            copy_tree("Keypoints_temp", "dataset\\" + entry.name + "\\" + timestamp )
    
    
    
    """ 
    Remove 'Keypoints_temp' folder 
    """
    
    shutil.rmtree("Keypoints_temp", ignore_errors=True, onerror=handleRemoveReadonly)
    print( 'Keypoints_temp folder removed')
    
    
    # create table if not exists
    dbh.create_table()
    # add all records from 'dataset' to 'db\main_databse.db'
    dbh.populate_db()





