# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 06:39:45 2019

"""

import numpy as np
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, LSTM, Dropout
from keras.layers import TimeDistributed, BatchNormalization
from keras.optimizers import Adam
from sklearn.metrics import f1_score, confusion_matrix, roc_auc_score, precision_score
from sklearn.metrics import recall_score, accuracy_score
from sklearn.preprocessing import normalize
import matplotlib.pyplot as plt
from keras.models import load_model


# import data
X_train = np.load('NPdata\\xtrain.npy')
Y_train = np.load('NPdata\\ytrain.npy')
X_test = np.load('NPdata\\xtest.npy')
Y_test = np.load('NPdata\\ytest.npy')

# build model
print("Building model")

model = Sequential()
model.add(LSTM(128, input_shape=(100, 411), return_sequences = True))
model.add(Dropout(0.5))                             
model.add(BatchNormalization())

model.add(LSTM(128, input_shape=(100, 411), return_sequences = True))
model.add(Dropout(0.5))                             
model.add(BatchNormalization())

model.add(LSTM(64, input_shape=(100, 411), return_sequences = True))
model.add(Dropout(0.5))                             
model.add(BatchNormalization())

model.add(LSTM(32, input_shape=(100, 411), return_sequences = True))
model.add(Dropout(0.5))                             
model.add(BatchNormalization())

model.add(TimeDistributed(Dense(7))) 
model.add(Activation('softmax'))
myOptimizer = Adam(lr = 0.006) 
model.compile(loss='categorical_crossentropy', optimizer=myOptimizer, metrics=['categorical_accuracy'])

# summarize model
print(model.summary())

# train model
model.fit(X_train, Y_train, batch_size=6, epochs = 50) 

# evaluate
loss, acc = model.evaluate(X_test, Y_test)

print("Test set accuracy = ", acc)
print("Test set loss = ", loss)

model.save("model.h5")

model = load_model("model.h5")
# predict
predictions = model.predict(X_test)

# initialize metrics
f1 = 0 # f1 score
f1WithZeros = 0 # f1 score if we just always predicted 'no sign'
rs = 0 # recall score
ra = 0 # ROC AUC score
acs = 0 # accuracy score
cm = np.zeros((7,7)) # confusion matrix
allZeroPredictions = np.zeros((7,1))
allZeroPredictions[0] = 1
numExamples = 0

for i in range(predictions.shape[0]):
	for j in range(predictions.shape[1]):
		index = np.argmax(predictions[i,j,:])
		predictionsOneHot = np.zeros((7,1))
		predictionsOneHot[index] = 1
		f1 += f1_score(Y_test[i,j,:], predictionsOneHot, average='macro')  
		f1WithZeros += f1_score(Y_test[i,j,:], allZeroPredictions, average='macro') 
		rs += recall_score(Y_test[i,j,:], predictionsOneHot)
		#ra += roc_auc_score(Y_test[i,j,:], predictionsOneHot)
		acs += accuracy_score(Y_test[i,j,:], predictionsOneHot)

		Y_TestInteger = np.zeros((1,1))
		predictionsInteger = np.zeros((1,1))
		Y_TestInteger[0] = np.argmax(Y_test[i,j,:])

		predictionsInteger[0] = np.argmax(predictionsOneHot)


		cm = np.add(cm, confusion_matrix(Y_TestInteger, predictionsInteger, labels = [0, 1, 2, 3, 4, 5, 6]))
		numExamples = numExamples + 1

# print scores so we can compare the performance of models
print("F1 score of actual predictions = ", (f1/numExamples))
print("F1 score of predicting all 0s = ", (f1WithZeros/numExamples))
print("Recall score: ", rs/numExamples)
print("ROC AUC score: ", ra/numExamples)
print("Accuracy score: ", acs/numExamples)
print("Confusion matrix: ", cm)

## normalize for ease of viewing
#cm = normalize(cm, axis=0, norm='6')
#cm = normalize(cm, axis=1, norm='6')

# plot
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(cm)
plt.title('Confusion matrix of the classifier')
fig.colorbar(cax)
ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
ax.set_yticks([0, 1, 2, 3, 4, 5, 6])
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()









#
#
#import sqlite3
#import json
#
#
#connection = sqlite3.connect("db\\main_dataset.db") 
#crsr = connection.cursor()
#
#sql = 'SELECT video,label FROM videoDataset WHERE 1 ORDER BY label'
#
#crsr.execute(sql)
#feature_res = crsr.fetchall()
#
#num_vids = 1
#max_len = 150
#X = np.zeros((num_vids,max_len,411))
#Y = np.zeros((num_vids,max_len,7))
#
#
#
#
#
#
#count_vid = 0
#
#
## get all video names
#video_name = []
#for x in range(len(feature_res)):
#    name = feature_res[x][0].split("\\")
#    video_name.append(name[2])
#    
#x = np.array(video_name)
#video_name = np.unique(x)
#
#
#
#i=0
#pos=0
#for x in range(1):
#    
#    if i>=50:
#        i=0
#        pos+=1
#    
#    count_pic = 0
#    for y in range(len(feature_res)):
#	
#        name = feature_res[y][0].split("\\")
#        pic_name = name[3]
#        pic_name = pic_name[:11]
#        
#        
#        if video_name[x] == pic_name :
#            
#            with open(feature_res[y][0]) as json_data:
#                d = json.load(json_data)
#            data = []
#            data.extend(d['people'][0]['pose_keypoints_2d'])
#            data.extend(d['people'][0]['face_keypoints_2d'])
#            data.extend(d['people'][0]['hand_left_keypoints_2d'])
#            data.extend(d['people'][0]['hand_right_keypoints_2d'])
#            data = np.array(data)
#            if count_pic < 150:
#                X[x,count_pic,:] = data
#                print("x = "+ str(x) + " count_pic = "+ str(count_pic) )
#            count_pic+=1
#
#
#
#
#predictions = model.predict(X)











