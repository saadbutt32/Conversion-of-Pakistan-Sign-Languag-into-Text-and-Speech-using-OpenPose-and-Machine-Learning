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

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# Import `Sequential` from `keras.models`
from keras.models import Sequential
# Import `Dense` from `keras.layers`
from keras.layers import Dense
from keras.utils import to_categorical

# js = json.loads(open('E:\\Sign_Language_Interpreter\\alif_umer.json' ).read())
# for items in js['people']:
#     handRight = items["hand_right_keypoints_2d"]

# handPoints = helper.removePoints(handRight)

# handRightResults,handRightPoints = move.centerPoints(handPoints)


connection = sqlite3.connect("db\\dataset_saad.db") 
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

print(features[0])
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

print(X_train[0])
# Initialize the constructor
model = Sequential()

# Add an input layer 
model.add(Dense(12, activation='relu', input_shape=(42,)))

# Add one hidden layer 
model.add(Dense(16, activation='relu'))


# Add an output layer 
model.add(Dense(9, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
                   
model.fit(X_train, y_train,epochs=20, batch_size=1, verbose=1)

#y_pred = model.predict(scaler.transform(np.array([handRightResults])))
#C = np.argmax(y_pred)

#y_pred = model.predict(scaler.transform(X_test))

# print(le.inverse_transform(C))

score = model.evaluate(X_test, y_test,verbose=1)

print(score)















