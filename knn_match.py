# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 01:24:30 2019

"""

import json
import sqlite3
import math
import move
import helperFunc as helper
import scale
import numpy as np

from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from sklearn import metrics
from sklearn.model_selection import train_test_split


#def match_knn(fileName):
# js = json.loads(open('E:\\Sign_Language_Interpreter\\dal_umais.json'  ).read())
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

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = knn.predict(X_test)
#print(y_pred)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))