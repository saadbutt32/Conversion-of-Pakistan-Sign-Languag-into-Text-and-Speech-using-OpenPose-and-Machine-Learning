# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 02:08:28 2019

"""
# Convert json data to numpy array



# system imports
import sqlite3
import json 
import numpy as np
from sklearn.utils import shuffle
      
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder





words = ['call','deaf','food','help','learn','music','run']

le = preprocessing.LabelEncoder()
# Converting string labels into numbers.
label_encoded=le.fit_transform(np.ravel(words,order='C'))

# binary encode
onehot_encoder = OneHotEncoder(sparse=False)
label_encoded = label_encoded.reshape(len(label_encoded), 1)
onehot_encoded = onehot_encoder.fit_transform(label_encoded)
onehot = np.array(onehot_encoded)



connection = sqlite3.connect("db\\main_dataset.db") 
crsr = connection.cursor()

sql = 'SELECT video,label FROM videoDataset WHERE 1 ORDER BY label'

crsr.execute(sql)
feature_res = crsr.fetchall()

num_vids = 350
max_len = 100
X = np.zeros((num_vids,max_len,411))
Y = np.zeros((num_vids,max_len,7))






count_vid = 0


# get all video names
video_name = []
for x in range(len(feature_res)):
    name = feature_res[x][0].split("\\")
    video_name.append(name[2])
    
x = np.array(video_name)
video_name = np.unique(x)



i=0
pos=0
for x in range(len(video_name)):
    
    if i>=50:
        i=0
        pos+=1
    
    count_pic = 0
    for y in range(len(feature_res)):
	
        name = feature_res[y][0].split("\\")
        pic_name = name[3]
        pic_name = pic_name[:11]
        
        
        if video_name[x] == pic_name :
            
            with open(feature_res[y][0]) as json_data:
                d = json.load(json_data)
            data = []
            data.extend(d['people'][0]['pose_keypoints_2d'])
            data.extend(d['people'][0]['face_keypoints_2d'])
            data.extend(d['people'][0]['hand_left_keypoints_2d'])
            data.extend(d['people'][0]['hand_right_keypoints_2d'])
            data = np.array(data)
            if count_pic < 100:
                X[x,count_pic,:] = data
                Y[x,count_pic,:]=onehot[pos]
                print("x = "+ str(x) + " count_pic = "+ str(count_pic) )
            count_pic+=1
    i+=1


X,Y = shuffle(X,Y,random_state = 0)

X_train = X[:280]
X_test = X[280:]
Y_train = Y[:280]
Y_test = Y[280:]

np.save('NPdata/xtrain', X_train)
np.save('NPdata/xtest', X_test)
np.save('NPdata/ytrain', Y_train)
np.save('NPdata/ytest', Y_test)
















