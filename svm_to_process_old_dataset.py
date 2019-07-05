# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 01:36:42 2019

"""

import svm_match
import os
import shutil



folders = []
files = []
fileNames=[]

Dir = 'dataset_old'

for entry in os.scandir(Dir):
    if entry.is_dir():
        folders.append(entry.path)
        for entry1 in os.scandir(entry.path):
            if entry1.is_dir():
                folders.append(entry1.path)
            elif entry1.is_file():
                if os.path.splitext(entry1)[1] == ".json":
                    files.append(entry1.path)
                    fileNames.append(entry1.name)
    elif entry.is_file():
        if os.path.splitext(entry)[1] == ".json":
            files.append(entry.path)
            fileNames.append(entry.name)
            
            

for x in range(len(files)):
    try:
        label = svm_match.match_svm(files[x])         
    except:
        pass 
    
    if label != 'no match' and label != 'no confidence':
        shutil.copy(files[x], 'tem_old_dataset_complete//'+label)














