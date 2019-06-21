# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 15:09:28 2019

"""

import json
import sqlite3
import move
import helperFunc as helper
import numpy as np

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn import metrics

from sklearn import svm




def match_svm(fileName):
    js = json.loads(open(fileName ).read())
    for items in js['people']:
        handRight = items["hand_right_keypoints_2d"]
    
    confPoints = helper.confidencePoints(handRight)
    confidence = helper.confidence(confPoints)
    if confidence > 10.4:
        handPoints = helper.removePoints(handRight)
        
        handRightResults,handRightPoints = move.centerPoints(handPoints)
        
        
        connection = sqlite3.connect("db\\main_dataset.db") 
        crsr = connection.cursor()
        
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
        
        crsr.execute('SELECT label FROM rightHandDataset WHERE 1')
        label_res = crsr.fetchall()
        
        
        labels=[]
        for x in label_res:
            labels.append(x)
        #creating labelEncoder
        le = preprocessing.LabelEncoder()
        # Converting string labels into numbers.
        label_encoded=le.fit_transform(np.ravel(labels,order='C'))
        #print(label_encoded)
        
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)
        
        #Create a svm Classifier
        clf = svm.SVC(kernel='linear') # Linear Kernel
        #Train the model using the training sets
        clf.fit(X_train, np.ravel(y_train,order='C'))
        
        #Predict the response for test dataset
        y_pred = clf.predict([handRightResults])
        
        #y_pred = clf.predict(X_test)
        
        return y_pred[0]
        #print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
    else:
        return "no confidence"














