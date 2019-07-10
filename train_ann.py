# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 18:55:38 2019

"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 15:09:28 2019

"""

import move
import helperFunc as helper
import scale

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


from sklearn.metrics import confusion_matrix
from matplotlib import pyplot as plt
    
"""
extracting data from db
"""
connection = sqlite3.connect("db\\main_dataset.db") 
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

# Initialize the constructor
model = Sequential()

# Add an input layer 
model.add(Dense(120, activation='relu', input_shape=(42,)))

# Add one hidden layer 
model.add(Dense(64, activation='relu'))


# Add an output layer 
model.add(Dense(36, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
                   
model.fit(X_train, y_train,epochs=10, batch_size=1, verbose=1)

#model.save("test_model.h5")


y_pred = model.predict(scaler.transform(X_test))
score = model.evaluate(X_test, y_test,verbose=1)
#
print("\n%s: %.2f%%" % (model.metrics_names[1], score[1]*100))

cm = confusion_matrix(y_test.argmax(axis=1), y_pred.argmax(axis=1))

plt.matshow(cm)















