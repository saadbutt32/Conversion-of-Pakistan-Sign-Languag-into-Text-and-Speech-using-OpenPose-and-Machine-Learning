# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 03:44:00 2019

"""
import ann_match

import os
import subprocess
from tkinter import Label
import tkinter
import cv2
import PIL.Image, PIL.ImageTk

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
    window.destroy()
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
helper functions
"""
def waithere():
    var = tkinter.IntVar()
    window.after(2000, var.set, 1)
    print("waiting...")
    window.wait_variable(var)

skip_sign = False
def skip():
    global skip_sign
    skip_sign = True

"""
labels and image files
"""
labels = ['ا','ب','پ','ت‬','ٹ‬','ث‬','ج‬','چ‬','ح‬','خ‬','د‬','ڈ‬','ذ‬','ر‬','ڑ‬','ز‬','ژ‬','س‬','ش‬','ص‬','ض‬','ط‬','ظ‬','ع‬','غ‬','ف‬','ق‬','ک‬','گ‬','ل‬','م‬','و‬','ء‬','ہ‬','ی‬','ے‬']

fileNames=[]
Dir = 'learn'
for entry in os.scandir(Dir):
    if entry.is_file():
            fileNames.append(entry.path)


"""
Creating a window
"""
window = tkinter.Tk()
window.title("Learn Sign Language")

s = Label(window, text= "")
s.config(font=("Courier", 20))
s.pack()

# Create a canvas that can fit the above image
canvas = tkinter.Canvas(window, width = 1000, height = 700)
canvas.pack()

l = Label(window, text= "")
l.config(font=("Courier", 20))
l.pack()

B = tkinter.Button(window, text ="Skip", command = skip)
B.pack()

"""
Starting OpenPoseDemo.exe
and storing json files to temporary folder [Keypoints] 
"""
print('Starting OpenPose')
os.chdir('openpose')
p = subprocess.Popen('bin\\OpenPoseDemo.exe --display 0 --render_pose 0 --hand  --write_json ..\\Keypoints --net_resolution 128x128  --number_people_max 1', shell=True)
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



label=''       
for x in range(len(fileNames)):
    
    skip_sign=False
    
    # Load an image using OpenCV
    cv_img = cv2.cvtColor(cv2.imread("learn\\"+str(x+1)+".png"), cv2.COLOR_BGR2RGB)
    
    # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
    height, width, no_channels = cv_img.shape
    
    s[ "text" ]="Make the sign for ‬"+ labels[x]
    
#    font = cv2.FONT_HERSHEY_SIMPLEX
#    cv2.putText(cv_img,'Try Again',(400,100), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
    
    
    
    # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
    photo = PIL.ImageTk.PhotoImage( image = PIL.Image.fromarray(cv_img))
    # Add a PhotoImage to the Canvas
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
    window.update()
    
    count=0
    while label!=labels[x]:
        if skip_sign==True:
            break
        try:
    
            for entry in os.scandir('Keypoints'):
                if entry.is_file():
                    if os.path.splitext(entry)[1] == ".json":
                        fileName = entry.name
                       
            try:
                label = ann_match.match_ann('Keypoints\\'+fileName) 
            except:
                pass
            
            if count==1000:
                count=0
                l[ "text" ]="Not a valid sign"
                window.update()
            count+=1    
    
        except UnboundLocalError:
            print("UnboundLocalError")
    
    l[ "text" ]="Good"
    window.update()
    waithere()

# Run the window loop
window.mainloop()



















