# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 13:54:32 2019

"""

import sqlite3
import numpy as np

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical

from sklearn.metrics import confusion_matrix, classification_report
from matplotlib import pyplot as plt

def train_words():    
    """
    extracting data from db
    """
    connection = sqlite3.connect("data\\db\\main_dataset.db") 
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
    
    label_encoded = to_categorical(label_encoded)
    
    X_train, X_test, y_train, y_test = train_test_split(features, label_encoded, test_size=0.2)
    
    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Initialize the constructor
    model = Sequential()
    
    # Add an input layer 
    model.add(Dense(110, activation='relu', input_shape=(110,)))
    
    # Add one hidden layer 
    model.add(Dense(64, activation='relu'))
    
    # Add one hidden layer 
    model.add(Dense(64, activation='relu'))
    
    
    # Add an output layer 
    model.add(Dense(12, activation='sigmoid'))
    
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
                       
#    model.fit(X_train, y_train,epochs=30, batch_size=1, verbose=1)
    
    
    
    
    


    history = model.fit(X_train, y_train,validation_split=0.20,epochs=25, batch_size=1, verbose=1)

#    model.save("data\\models\\word_model.h5")
    
    y_pred = model.predict(X_test)
    score = model.evaluate(X_test, y_test,verbose=1)
    #
    print("\n%s: %.2f%%" % (model.metrics_names[1], score[1]*100))
    
    # list all data in history
    print(history.history.keys())
    # summarize history for accuracy
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('Accuracy vs Epoch')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    #plt.figure(figsize = (30,30))
    plt.show()
    
    
    print(model.summary())
    cm = confusion_matrix(y_test.argmax(axis=1), y_pred.argmax(axis=1))
    
    import itertools
    plt.rcParams.update({'font.size': 16})
    def plot_confusion_matrix(cm, classes,
                              normalize=False,
                              title='Confusion matrix',
                              cmap=plt.cm.Blues):
        """
        This function prints and plots the confusion matrix.
        Normalization can be applied by setting `normalize=True`.
        """
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            print("Normalized confusion matrix")
        else:
            print('Confusion matrix, without normalization')
    
        print(cm)
    
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=0)
        plt.yticks(tick_marks, classes)
    
        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, format(cm[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
    
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
    
    l = np.array(labels) 
    l = np.unique(l)
    
    class_names = l
    
    plt.figure(figsize = (10,10))
    plot_confusion_matrix(cm, classes=class_names, normalize=True,
                          title='Normalized confusion matrix')
    
    plt.show()




























#import json
#import sqlite3
#import move
#import helperFunc as helper
#import numpy as np
#
#from sklearn import preprocessing
#from sklearn.model_selection import train_test_split
#from sklearn import metrics
#
#from sklearn import svm
#
#
#connection = sqlite3.connect("db\\main_dataset.db") 
#crsr = connection.cursor()
#
#sql = 'SELECT Rx1,Ry1'
#for x in range(2,22):
#    sql = sql + ',Rx'+str(x)+',Ry'+str(x)
#for x in range(1,22):
#    sql = sql + ',Lx'+str(x)+',Ly'+str(x)
#for x in range(1,14):
#    sql = sql + ',Px'+str(x)+',Py'+str(x)
#sql = sql + ' FROM poseDataset WHERE 1'
#
#crsr.execute(sql)
#feature_res = crsr.fetchall()
#
#feature_res = np.asarray(feature_res)
#
#features=[]
#for x in feature_res:
#    features.append(x)
#
#crsr.execute('SELECT label FROM poseDataset WHERE 1')
#label_res = crsr.fetchall()
#
#
#labels=[]
#for x in label_res:
#    labels.append(x)
##creating labelEncoder
#le = preprocessing.LabelEncoder()
## Converting string labels into numbers.
#label_encoded=le.fit_transform(np.ravel(labels,order='C'))
##print(label_encoded)
#
#X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)
#
##Create a svm Classifier
#clf = svm.SVC(kernel='linear') # Linear Kernel
##Train the model using the training sets
#clf.fit(X_train, np.ravel(y_train,order='C'))
#
##Predict the response for test dataset
#y_pred = clf.predict([features[38]])
#print( y_pred[0])
#
###Predict the response for test dataset
##
##y_pred = clf.predict(X_test)
##
##print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
#
#
#





























