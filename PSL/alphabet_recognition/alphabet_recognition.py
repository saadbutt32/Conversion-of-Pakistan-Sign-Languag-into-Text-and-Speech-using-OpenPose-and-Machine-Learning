# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 15:09:28 2019

"""

import PSL.helper.move as move
import PSL.helper.helperFunc as helper
import PSL.helper.scale as scale

import json
import sqlite3
import math
import numpy as np

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from keras.utils import to_categorical
from keras.models import load_model


model = load_model("data\\models\\alphabet_model.h5")
print("alphabet model loaded")


def match_ann(fileName):
    js = json.loads(open(fileName ).read())
    for items in js['people']:
        handRight = items["hand_right_keypoints_2d"]

    confPoints = helper.confidencePoints(handRight)
    confidence = helper.confidence(confPoints)
    if confidence > 10.2:
        handPoints = helper.removePoints(handRight)

        """
        experimenting with scaling 
        """
        p1 = [handPoints[0], handPoints[1]]
        p2 = [handPoints[18], handPoints[19]]
        distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )

        Result,Points = scale.scalePoints(handPoints,distance)
        handRightResults,handRightPoints = move.centerPoints(handPoints)
        
        """
        extracting data from db
        """
        connection = sqlite3.connect("data\\db\\main_dataset.db") 
        crsr = connection.cursor()

        # extracting x and y points
        sql = 'SELECT x1,y1'
        for x in range(2,22):
            sql = sql + ',x'+str(x)+',y'+str(x)
        sql = sql + ' FROM rightHandDataset WHERE 1'
        crsr.execute(sql)
        feature_res = crsr.fetchall()
        feature_res = np.asarray(feature_res)
        features=[]
        for x in feature_res:
            features.append(x)

        # extracting labels
        crsr.execute('SELECT label FROM rightHandDataset WHERE 1')
        label_res = crsr.fetchall()
        labels=[]
        for x in label_res:
            labels.append(x)
    
        #creating labelEncoder
        le = preprocessing.LabelEncoder()
        # Converting string labels into numbers.
        label_encoded=le.fit_transform(labels)

        label_encoded = to_categorical(label_encoded)

        X_train, X_test, y_train, y_test = train_test_split(features, label_encoded, test_size=0.2)
        
        scaler = StandardScaler().fit(X_train)
        X_train = scaler.transform(X_train)
        X_test = scaler.transform(X_test)

        y_pred = model.predict(scaler.transform(np.array([handRightResults])))

        C = np.argmax(y_pred)

        result = le.inverse_transform([C])

        return result[0]
    else:
        return "no confidence"
