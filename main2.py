# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 14:03:43 2019

"""
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 22:38:14 2018
"""

import os
import subprocess
import svm_match

from pygame import mixer # for sound

# for error handling
import errno, stat, shutil
import sys, signal
import eel

"""
Handling Errors While removing temp folders
"""     
eel.init("gui")

def signal_handler(signal, frame):
    # Removing Keypoints Folder
    shutil.rmtree("Keypoints", ignore_errors=True, onerror=handleRemoveReadonly)
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
shutil.rmtree("Keypoints", ignore_errors=True, onerror=handleRemoveReadonly)

@eel.expose
def openpose():
    """
    Starting OpenPoseDemo.exe
    and storing json files to temporary folder [Keypoints] 
    """
    print('Starting OpenPose')
    os.chdir('openpose')
    p = subprocess.Popen('bin\\OpenPoseDemo.exe --hand  --write_json ..\\Keypoints --net_resolution 128x128  --number_people_max 1', shell=True)
    os.chdir('..')
    
    """
    Creating temp folder and initializing with zero padded json file
    """
    dirName = 'Keypoints'
    fileName = '000000000000_keypoints.json'
     
    try:
        # Create target Directory
        os.mkdir(dirName)
        shutil.copy(fileName, dirName)
        print("Directory " , dirName ,  " Created ") 
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")
    

@eel.expose
def match():
    
    """
    Load each .json file from Keypoints folder and
    predict the label 
    """
    label=''
    lastLabel = ''
    for entry in os.scandir('Keypoints'):
        if entry.is_file():
            if os.path.splitext(entry)[1] == ".json":
                fileName = entry.name     
    try:
       label = svm_match.match_svm('Keypoints\\'+fileName)
    except:
        pass
    
    if label != 'no match' and label != 'no confidence' and label != lastLabel:
        lastLabel = label  
        
        mp3 = "speech\\"+label+".mp3"
        mixer.init()
        mixer.music.load(mp3)
        mixer.music.play()
        return label
        

eel.start('main.html',size=(1000,600))

label=""
while True:
        
#    time.sleep(0.5)
#    try:

        label = match()
        if label!=None and label != "":
            print(label)   
#    except UnboundLocalError:
#        print("UnboundLocalError")
    








    
    
    
    
    
    
    
    
    
    
    
    
    

