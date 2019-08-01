
# -*- coding: utf-8 -*-

# local imports
import PSL.helper.db_helper as dbh
import PSL.helper.helperFunc as helper
import PSL.helper.move as move
import PSL.helper.scale as scale
import PSL.helper.plot as plot
import PSL.retrain as retrain

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

import eel


"""
Handling Errors While removing temp folders
"""     
def signal_handler(signal, frame):
    # Removing Keypoints Folder
    shutil.rmtree("Keypoints", ignore_errors=True, onerror=handleRemoveReadonly)
    shutil.rmtree("gui\\captured_images", ignore_errors=True, onerror=handleRemoveReadonly)
    shutil.rmtree("gui\\temp_images", ignore_errors=True, onerror=handleRemoveReadonly)
    
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



def plotPose(posePoints, handRightPoints, handLeftPoints):
    POSE_PAIRS = [[1, 0], [1, 2], [1, 5], [2, 3], [3, 4], [5, 6], [6, 7],
                  [1, 8], [0, 15], [15, 17], [0, 16], [16, 18]]

    HAND_PAIRS = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 5], [5, 6], [6, 7], [7, 8], [0, 9], [9, 10],
                  [10, 11], [11, 12], [0, 13], [13, 14], [14, 15], [15, 16], [0, 17], [17, 18],
                  [18, 19], [19, 20]]

    colors = [[0, 0, 130], [0, 0, 175], [0, 0, 210], [0, 0, 250],
              [0, 200, 160], [0, 180, 150], [0, 230, 186], [0, 255, 255],
              [82, 201, 8], [82, 204, 0], [92, 230, 0], [102, 252, 6],
              [197, 88, 17], [204, 82, 0], [179, 71, 0], [227, 94, 5],
              [204, 0, 163], [200, 0, 163], [196, 0, 163], [230, 0, 184]]

    background = "PSL\\BLACK_background.jpg"

    frame = cv2.imread(background)

    count = 0
    # Draw Skeleton
    for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]

        if posePoints[partA] and posePoints[partB] and posePoints[partA][0] != 0 and posePoints[partA][1] != 0 and \
                posePoints[partB][0] != 0 and posePoints[partB][1] != 0:
            cv2.line(frame, posePoints[partA], posePoints[partB], colors[count], 10)
            cv2.circle(frame, posePoints[partA], 5, (0, 0, 255), thickness=10, lineType=cv2.FILLED)
            cv2.circle(frame, posePoints[partB], 5, (255, 255, 255), thickness=15, lineType=cv2.FILLED)
        count += 1

    count = 0
    for pair in HAND_PAIRS:
        partA = pair[0]
        partB = pair[1]

        if handRightPoints[partA] and handRightPoints[partB]:
            cv2.line(frame, handRightPoints[partA], handRightPoints[partB], colors[count], 10)
            cv2.circle(frame, handRightPoints[partA], 5, (0, 0, 255), thickness=3, lineType=cv2.FILLED)
            cv2.circle(frame, handRightPoints[partB], 5, (255, 255, 255), thickness=4, lineType=cv2.FILLED)
        count += 1

    count = 0
    for pair in HAND_PAIRS:
        partA = pair[0]
        partB = pair[1]

        if handLeftPoints[partA] and handLeftPoints[partB]:
            cv2.line(frame, handLeftPoints[partA], handLeftPoints[partB], colors[count], 10)
            cv2.circle(frame, handLeftPoints[partA], 5, (0, 0, 255), thickness=3, lineType=cv2.FILLED)
            cv2.circle(frame, handLeftPoints[partB], 5, (255, 255, 255), thickness=4, lineType=cv2.FILLED)
        count += 1

    #    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    return frame


remfileNames = []

@eel.expose
def capture_alphabet_dataset(sec):
    
    global remfileNames
    
    """
    ----------------------Start OpenPoseDemo.exe----------------------
    --render_pose 0  --display 0
    """
    os.chdir('bin\\openpose')
    print('Starting OpenPose')
    subprocess.Popen('bin\\OpenPoseDemo.exe --hand  --write_json ..\\..\\Keypoints   --number_people_max 1', shell=True)
    os.chdir('..\\..')
    
    
    
    """
    ----------------------Creating temp folder----------------------
    """
    dirName = 'Keypoints'
    init_file = 'PSL\\000000000000_keypoints.json'
    
    try:
        # Create target Directory
        os.mkdir(dirName)
        os.mkdir("gui\\captured_images")
        os.mkdir("gui\\temp_images")
        
        # copy initializing file in directory
        shutil.copy(init_file, dirName)
        print("Directory " , dirName ,  " Created ") 
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")

    
    
    """
    ----------------------Live View----------------------
    """
    
#    shutil.copy('PSL\\000000000000_keypoints.json', 'Keypoints')
#    filePlotName = '000000000000_keypoints.json'
    t = time.time() + sec
    while time.time() <= t:
        eel.sleep(0.05)
#        for entry in os.scandir('Keypoints'):
#            if entry.is_file():
#                if os.path.splitext(entry)[1] == ".json":
#                    filePlotName = entry.name
#    
#        try:
#            js = json.loads(open('Keypoints\\' + filePlotName).read())
#        except ValueError:
#            print('Decoding JSON has failed')
#            pass
#    
#        # extract 'hand_right_keypoints_2d' from json file
#        for items in js['people']:
#            pose = items["pose_keypoints_2d"]
#            handRight = items["hand_right_keypoints_2d"]
#            handLeft = items["hand_left_keypoints_2d"]
#    
#        pose_points = helper.removePoints(pose)
#        posePoints = helper.join_points(pose_points)
#    
#        #  function to remove confidence points
#        hand_right_Points = helper.removePoints(handRight)
#        handRightPoints = helper.join_points(hand_right_Points)
#    
#        hand_left_points = helper.removePoints(handLeft)
#        handLeftPoints = helper.join_points(hand_left_points)
#    
#        frame = plotPose(posePoints, handRightPoints, handLeftPoints)
#    
#        cv2.imwrite('gui\\temp_images\\' + filePlotName + '.jpg', frame)
#        # reset image
#        frame = cv2.imread("PSL\\BLACK_background.jpg")
#        print("saad")
#        eel.get_fileName(filePlotName)
#        filePlotName = ''


#    eel.sleep(sec)
    #  Kill openpose
    os.system("taskkill /f /im  OpenPoseDemo.exe")
    
    
    """
    ---------------------- Auto Remove files----------------------
    """
    conf_thershold = 10
    fileNames = []
    #scan temporary folder
    for entry in os.scandir('Keypoints'):
        # store the name if entry is file and file is of ext .json
        if entry.is_file():
            if os.path.splitext(entry)[1] == ".json":
                fileNames.append(entry.name)
                
    # traverse fileNames[]
    for x in range(len(fileNames)):
        # load each file from fileName[]
        js = json.loads(open('Keypoints\\' + fileNames[x]).read())
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
            os.remove('Keypoints\\' + fileNames[x])


    """
    ----------------------plot and save----------------------
    """   
    background = 'big_background.png'
    fileNames = []
    #scan temporary folder
    for entry in os.scandir('Keypoints'):
        # store the name if entry is file and file is of ext .json
        if entry.is_file():
            if os.path.splitext(entry)[1] == ".json":
                fileNames.append(entry.name)
                
    
    # read background image
    frame = cv2.imread(background)
    
    i=1;
    
    for x in range(len(fileNames)):
        # load each file from fileName[]
        js = json.loads(open('Keypoints\\' + fileNames[x]).read())
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
        
        cv2.imwrite('gui\\captured_images\\' + str(i) + '.jpg', frame)
        i+=1
        
        
        """
        ----------------------get ref to delete files----------------------
        """ 
        
        for entry in os.scandir('Keypoints'):
            if entry.is_file():
                if os.path.splitext(entry)[1] == ".json":
                    remfileNames.append(entry.name)
        
        
        """
        ----------------------end capture_alphabet_dataset(sec)----------------------
        """  

@eel.expose
def getFileCount():
    Names = []
    for entry in os.scandir('gui\\captured_images'):
        Names.append(entry.name)
    return str(len(Names))


@eel.expose
def delete_Image(i):
    global remfileNames
    
    print(remfileNames)
    
    try:
        os.remove('Keypoints\\' + remfileNames[i-1])            
        os.remove('gui\\captured_images\\'+ str(i) + '.jpg')
    except:
        print("file not found")
        pass




@eel.expose
def getlabel(a):

    # remove whitespaces
    label = a.strip()
    print(label)

    """
    traverse 'dataset' folder ,
    find subfolder matching 'label' ,
    create folder with timestamp in  matched folder , 
    and copy everything from 'Keypoints_temp' to created folder
    """
    for entry in os.scandir('data\\datasets\\alphabets_dataset'):
        if entry.name == label:
            # current date and time
            now = datetime.now()
            # create folder with timestamp
            timestamp =  str(datetime.timestamp(now))
            dir_name = "data\\datasets\\alphabets_dataset\\" + entry.name +"\\"+ timestamp
            try:
                # Create target Directory
                os.mkdir(dir_name)
                print("Directory " , dir_name ,  " Created ")
            except FileExistsError:
                print("Directory " , dir_name ,  " already exists")

               # copy everything from 'Keypoints_temp' to created folder
            copy_tree("Keypoints", "data\\datasets\\alphabets_dataset\\" + entry.name + "\\" + timestamp )


    """ 
    Remove temp folders 
    """
    try:
        shutil.rmtree("Keypoints", ignore_errors=True, onerror=handleRemoveReadonly)
        shutil.rmtree("gui\\captured_images", ignore_errors=True, onerror=handleRemoveReadonly)
        shutil.rmtree("gui\\temp_images", ignore_errors=True, onerror=handleRemoveReadonly)
        
        print( 'Keypoints_temp folder removed')
    except:
        print("not removed")
        pass
    
@eel.expose
def db_train():
    retrain.re_train(1)












