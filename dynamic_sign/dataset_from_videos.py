# -*- coding: utf-8 -*-

import os
import subprocess


folders = []
files = []
fileNames = []
for entry in os.scandir('video_dataset_raw'):
    if entry.is_dir():
        folders.append(entry.name)
        for entry1 in os.scandir(entry.path):
            if entry1.is_dir():
                folders.append(entry1.name)

count=0
         
for x in range(0,len(folders)):
    try:  
        os.mkdir("video_dataset_processed_2fr\\" + folders[x])
        for entry in os.scandir('video_dataset_raw\\'+ folders[x]):
            if entry.is_file():
                files.append(entry.name)
                os.chdir('openpose') 
                output = subprocess.call('openpose\\build\\x64\\Release\\OpenPoseDemo.exe --video video_dataset_raw\\' + folders[x] +'\\'+entry.name+' --hand --face --net_resolution 128x128  --frame_step 2 --write_json video_dataset_processed_2fr\\'+folders[x]+'\\'+ os.path.splitext(entry.name)[0]  +'  --number_people_max 1 --display 0 --render_pose 0')
                os.chdir('..') 
                count+=1
                print(count)
    except FileExistsError:
        print("Directory " , folders[x] ,  " already exists")

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    