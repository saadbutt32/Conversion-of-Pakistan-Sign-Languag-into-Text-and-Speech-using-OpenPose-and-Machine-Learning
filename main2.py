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
import ann_match
import time

from pygame import mixer # for sound

from tkinter import Tk
from tkinter import Label

# for error handling
import errno, stat, shutil
import sys, signal


"""
Handling Errors While removing temp folders
"""     
def signal_handler(signal, frame):
    # Removing Keypoints Folder
    shutil.rmtree("Keypoints", ignore_errors=True, onerror=handleRemoveReadonly)
    os.system("taskkill /f /im  OpenPoseDemo.exe")
    root.destroy()
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

"""
Tkinter window
"""
root = Tk()
root.geometry("300x300+1600+100") #Width x Height
l = Label(root, text= "‬")
l.config(font=("Courier", 100))
l.pack()
root.update()

"""
Starting OpenPoseDemo.exe
and storing json files to temporary folder [Keypoints] 
"""
print('Starting OpenPose')
os.chdir('openpose')
p = subprocess.Popen('build\\x64\\Release\\OpenPoseDemo.exe --hand  --write_json ..\\Keypoints --net_resolution 128x128  --number_people_max 1', shell=True)
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


"""
Load each .json file from Keypoints folder and
predict the label 
"""
def match():
    label=''
    lastLabel = ''
    for entry in os.scandir('Keypoints'):
        if entry.is_file():
            if os.path.splitext(entry)[1] == ".json":
                fileName = entry.name     
    try:
        label = ann_match.match_ann('Keypoints\\'+fileName) 
    except:
        pass
    
    if label != 'no match' and label != 'no confidence' and label != lastLabel:
        lastLabel = label  
        
        l[ "text" ]=label
        root.update()
        mp3 = "speech\\"+label+".mp3"
        mixer.init()
        mixer.music.load(mp3)
        mixer.music.play()
        return label
        
        

label=""
while True:
#    time.sleep(0.5)
#    try:

        label = match()
        if label!=None and label != "":
            print(label)   

#    except UnboundLocalError:
#        print("UnboundLocalError")
    
 
root.mainloop()







    
    
    
    
    
    
    
    
    
    
    
    
    

