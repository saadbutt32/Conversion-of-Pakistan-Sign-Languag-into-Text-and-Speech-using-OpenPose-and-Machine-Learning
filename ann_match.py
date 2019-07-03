# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 15:09:28 2019

"""

import json
import sqlite3
import math
import move
import helperFunc as helper
import scale
import numpy as np

from matplotlib import pyplot as plt

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# Import `Sequential` from `keras.models`
from keras.models import Sequential
# Import `Dense` from `keras.layers`
from keras.layers import Dense
from keras.utils import to_categorical
from keras.models import load_model


model = load_model("ann_model.h5")
print("model loaded")

def match_ann(fileName):
    js = json.loads(open(fileName ).read())
    for items in js['people']:
        handRight = items["hand_right_keypoints_2d"]
    
    confPoints = helper.confidencePoints(handRight)
    confidence = helper.confidence(confPoints)
    if confidence > 12:
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
        label_encoded=le.fit_transform(labels)
        #print(label_encoded)
        
        label_encoded = to_categorical(label_encoded)
        
        X_train, X_test, y_train, y_test = train_test_split(features, label_encoded, test_size=0.2)
        
        # Define the scaler 
        scaler = StandardScaler().fit(X_train)
        
        # Scale the train set
        X_train = scaler.transform(X_train)
        
        # Scale the test set
        X_test = scaler.transform(X_test)
        
#        print(X_train[0])
#        # Initialize the constructor
#        model = Sequential()
#        
#        # Add an input layer 
#        model.add(Dense(120, activation='relu', input_shape=(42,)))
#        
#        # Add one hidden layer 
#        model.add(Dense(64, activation='relu'))
#        
#        
#        # Add an output layer 
#        model.add(Dense(36, activation='sigmoid'))
#        
#        model.compile(loss='binary_crossentropy',
#                      optimizer='adam',
#                      metrics=['accuracy'])
#                           
#        model.fit(X_train, y_train,epochs=10, batch_size=1, verbose=1)
#        model.save("ann_model.h5")
        
        y_pred = model.predict(scaler.transform(np.array([handRightResults])))
        C = np.argmax(y_pred)
        
#        y_pred = model.predict(scaler.transform(X_test))
#        score = model.evaluate(X_test, y_test,verbose=1)
#        #
#        print("\n%s: %.2f%%" % (model.metrics_names[1], score[1]*100))
        
        result = le.inverse_transform([C])
        
        return result[0]
    else:
        return "no confidence"



#
#model.save("model.h5")
#
#model = load_model("model.h5")
## predict
#predictions = model.predict(X_test)














