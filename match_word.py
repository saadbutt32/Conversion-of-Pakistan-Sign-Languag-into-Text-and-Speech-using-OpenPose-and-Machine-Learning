# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 16:22:06 2019

"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 15:09:28 2019

"""

import move
import helperFunc as helper
import scale
import normalize as norm

import json
import sqlite3
import math
import numpy as np

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from keras.models import load_model


model = load_model("word_model.h5")
print("model loaded")


def match_ann(fileName):
    js = json.loads(open(fileName).read())
    for items in js['people']:
        pose = items["pose_keypoints_2d"]
        handRight = items["hand_right_keypoints_2d"]
        handLeft = items["hand_left_keypoints_2d"]
    
    
    
    RightConfPoints = helper.confidencePoints(handRight)
    LeftConfPoints = helper.confidencePoints(handLeft)
    # add all confidence points
    RightConfidence = helper.confidence(RightConfPoints)
    LeftConfidence = helper.confidence(LeftConfPoints)
    # remove file if confidence is less than threshold
    if RightConfidence > 12:
        if LeftConfidence > 12 or LeftConfidence < 2 :
            
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
                handLeftResults = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,]
            
            posePoints = []
            for x in range(18):
                posePoints.append(poseResults[x])
            for x in range(30,38):
                posePoints.append(poseResults[x])
            
            results = handRightResults + handLeftResults + posePoints
            
            """
            extracting data from db
            """
            connection = sqlite3.connect("db\\main_dataset.db") 
            crsr = connection.cursor()
            
            # extracting x and y points
            sql = 'SELECT Rx1,Ry1'
            for x in range(2,22):
                sql = sql + ',Rx'+str(x)+',Ry'+str(x)
            for x in range(1,22):
                sql = sql + ',Lx'+str(x)+',Ly'+str(x)
            for x in range(1,14):
                sql = sql + ',Px'+str(x)+',Py'+str(x)
            sql = sql + ' FROM poseDataset WHERE 1'
            crsr.execute(sql)
            feature_res = crsr.fetchall()
            feature_res = np.asarray(feature_res)
            features=[]
            for x in feature_res:
                features.append(x)
            
            # extracting labels
            crsr.execute('SELECT label FROM poseDataset WHERE 1')
            label_res = crsr.fetchall()
            labels=[]
            for x in label_res:
                labels.append(x)
                
            #creating labelEncoder
            le = preprocessing.LabelEncoder()
            # Converting string labels into numbers.
            label_encoded=le.fit_transform(labels)
            
            """
            to_categorical` converts label_encoded into a matrix with as many
            columns as there are classes. The number of rows stays the same.
            """
            label_encoded = to_categorical(label_encoded)
            
            X_train, X_test, y_train, y_test = train_test_split(features, label_encoded, test_size=0.2)
            
            """
            The idea behind StandardScaler is that it will transform your data
            such that its distribution will have a mean value 0 and standard deviation of 1.
            Given the distribution of the data, each value in the dataset will have the sample mean value 
            subtracted, and then divided by the standard deviation of the whole dataset.
            """
            scaler = StandardScaler().fit(X_train)
            X_train = scaler.transform(X_train)
            X_test = scaler.transform(X_test)
            
    #        # function for training the model
    #        train(X_train,y_train)
            
            y_pred = model.predict(scaler.transform(np.array([results])))
            
            #argmax gives the index of the greatest number in the given row or column
            C = np.argmax(y_pred)
            
            result = le.inverse_transform([C])
            
            return result[0]
        else:
            return "no confidence"
    else:
        return "no confidence"























