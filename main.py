# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 22:38:14 2018
"""
import cv2
import os
import subprocess
import json
import sqlite3
import match
#import knn_match
import plot
from matplotlib import pyplot as plt
import msvcrt
import math
import svm_match

import errno, os, stat, shutil

import sys, signal
def signal_handler(signal, frame):
    shutil.rmtree("Keypoints", ignore_errors=True, onerror=handleRemoveReadonly)
    print( 'All done')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def handleRemoveReadonly(func, path, exc):
  excvalue = exc[1]
  if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
      os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
      func(path)
  else:
      raise
      


print('Starting OpenPose')
#--net_resolution 128x128 --process_real_time --number_people_max 1
os.chdir('openpose')
#os.chdir('C:\\123Drive\\Python\\openpose-1.4.0-win64-gpu-binaries')
output = subprocess.Popen('build\\x64\\Release\\OpenPoseDemo.exe --hand  --write_json ..\\Keypoints --net_resolution 128x128  --number_people_max 1', shell=True)

os.chdir('..')

dirName = 'Keypoints'
fileName = '000000000000_keypoints.json'
 
try:
    # Create target Directory
    os.mkdir(dirName)
    shutil.copy(fileName, dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")

lastLabel = ''
while True:
    try:
        fileNames = []
        for entry in os.scandir('Keypoints'):
            if entry.is_file():
                if os.path.splitext(entry)[1] == ".json":
                    fileNames.append(entry.name)
                    fileName = entry.name
                    
        #background = 'background.png'
        try:
            label = svm_match.match_svm('Keypoints\\'+fileName) 
            #label,result_points,score = match.match('Keypoints\\'+fileName)
        except:
            pass
        
        if label != 'no match' and label != 'no confidence' and label != lastLabel:
            lastLabel = label  
            print("matched Reference =  (" + label + ")" )
#            
          
#    except KeyboardInterrupt:
#        #os.remove("E:\\Sign_Language_Interpreter\\Keypoints")
#        shutil.rmtree("E:\\Sign_Language_Interpreter\\Keypoints", ignore_errors=True, onerror=handleRemoveReadonly)
#        print( 'All done')
#        break
#        # If you actually want the program to exit
#        raise
    except UnboundLocalError:
        print("null")
    
    
    
#label,result_points,score = match.match('Keypoints\\'+fileName)

#fileName = 'chay.json'
#background = 'big_background.png'
#
##label,points,score = match.match(fileName)
#label = knn_match.match_knn(fileName) 
#
#print("input " + fileName)
#frame = plot.plot_skeleton(fileName,background,True,True )
#frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
#plt.imshow(frame)
#plt.show()
##cv2.imwrite('scale_test.jpg',frame)
#
##point = [(150.0, 150.0, 139.0367283251963, 142.79913849025868, 120.60193515298829, 137.31412408008674, 101.54787521908978, 139.29584570930726, 86.34835452419829, 139.75753522638843, 103.8482851359316, 125.44815440813277, 83.23085823310218, 123.35675452294042, 68.49581056203887, 122.20018527098992, 54.44092562366391, 120.94380388954544, 105.87196901902587, 129.62366639710757, 93.97710537014193, 146.74233865250693, 92.37213454315659, 162.38934314202587, 90.71113558643118, 176.95616543149782, 110.73318051036645, 135.74926621254593, 100.2357459099949, 150.83385633880113, 108.00602302564855, 160.21498457407876, 108.0955533020968, 170.6784843807935, 119.03314926765552, 141.2635335505551, 113.0295924744509, 154.31807075558277, 119.18674438987878, 159.37321813263003, 128.7586631602857, 161.6141186671063)]
##frame = plot.plot_points(point,background)
##frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
##plt.imshow(frame)
##plt.show()
#####cv2.imwrite('scale_input.jpg',frame)
##
##p1 = [150, 150]
##p2 = [105, 129]
##distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
##
##print(distance)
#
#
##print("matched Reference = " + label + "  score = "+str(score))
#print("matched Reference = " + label )
##frame = plot.plot_points(points,background )
##frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
##plt.imshow(frame)
##plt.show()




    
    
    
    
    
    
    
    
    
    
    
    
    
