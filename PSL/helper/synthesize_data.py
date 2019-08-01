# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 13:29:45 2019

"""

import sqlite3

import PSL.helper.rotate as rotate
import PSL.helper.helperFunc as helper

def synthesize(angle):
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
    features=[]
    for x in feature_res:
        features.append(x)
    
    # extracting labels
    crsr.execute('SELECT label FROM rightHandDataset WHERE 1')
    label_res = crsr.fetchall()
    labels=[]
    for x in label_res:
        labels.append(x)
    
    
     # connecting to the database  
    connection = sqlite3.connect("data\\db\\main_dataset.db") 
    # cursor  
    crsr = connection.cursor() 
    
    
    for x in range(len(features)):
        rotated = rotate.rotate_points(features[x],-angle)
        handRightResults = helper.seperate_points(rotated)
    #    new_features.append(handRightResults)
        
        parentName = "'"+str(labels[x][0])+"'"
        
        # SQL command to insert the data in the table 
        sql_command = "INSERT INTO rightHandDataset VALUES (NULL, "+ str(handRightResults[0]) + ", "+ str(handRightResults[1]) + ","+ str(handRightResults[2]) + ","+ str(handRightResults[3]) + ","+ str(handRightResults[4]) + ","+ str(handRightResults[5]) + ","+ str(handRightResults[6]) + ","+ str(handRightResults[7]) + ","+ str(handRightResults[8]) + ","+ str(handRightResults[9]) + ","+ str(handRightResults[10]) + ","+ str(handRightResults[11]) + ","+ str(handRightResults[12]) + ","+ str(handRightResults[13]) + ","+ str(handRightResults[14]) + ","+ str(handRightResults[15]) + ","+ str(handRightResults[16]) + ","+ str(handRightResults[17]) + ","+ str(handRightResults[18]) + ","+ str(handRightResults[19]) + ","+ str(handRightResults[20]) + ","+ str(handRightResults[21]) + ","+ str(handRightResults[22]) + ","+ str(handRightResults[23]) + ","+ str(handRightResults[24]) + ","+ str(handRightResults[25]) + ","+ str(handRightResults[26]) + ","+ str(handRightResults[27]) + ","+ str(handRightResults[28]) + ","+ str(handRightResults[29]) + ","+ str(handRightResults[30]) + ","+ str(handRightResults[31]) + ","+ str(handRightResults[32]) + ","+ str(handRightResults[33]) + ","+ str(handRightResults[34]) + ","+ str(handRightResults[35]) + ","+ str(handRightResults[36]) + ","+ str(handRightResults[37]) + ","+ str(handRightResults[38]) + ","+ str(handRightResults[39]) + ","+ str(handRightResults[40]) + ","+ str(handRightResults[41]) + ","+parentName+");"
        crsr.execute(sql_command)                 
        
        rotated = rotate.rotate_points(features[x],angle)
        handRightResults = helper.seperate_points(rotated)
        
        # SQL command to insert the data in the table 
        sql_command = "INSERT INTO rightHandDataset VALUES (NULL, "+ str(handRightResults[0]) + ", "+ str(handRightResults[1]) + ","+ str(handRightResults[2]) + ","+ str(handRightResults[3]) + ","+ str(handRightResults[4]) + ","+ str(handRightResults[5]) + ","+ str(handRightResults[6]) + ","+ str(handRightResults[7]) + ","+ str(handRightResults[8]) + ","+ str(handRightResults[9]) + ","+ str(handRightResults[10]) + ","+ str(handRightResults[11]) + ","+ str(handRightResults[12]) + ","+ str(handRightResults[13]) + ","+ str(handRightResults[14]) + ","+ str(handRightResults[15]) + ","+ str(handRightResults[16]) + ","+ str(handRightResults[17]) + ","+ str(handRightResults[18]) + ","+ str(handRightResults[19]) + ","+ str(handRightResults[20]) + ","+ str(handRightResults[21]) + ","+ str(handRightResults[22]) + ","+ str(handRightResults[23]) + ","+ str(handRightResults[24]) + ","+ str(handRightResults[25]) + ","+ str(handRightResults[26]) + ","+ str(handRightResults[27]) + ","+ str(handRightResults[28]) + ","+ str(handRightResults[29]) + ","+ str(handRightResults[30]) + ","+ str(handRightResults[31]) + ","+ str(handRightResults[32]) + ","+ str(handRightResults[33]) + ","+ str(handRightResults[34]) + ","+ str(handRightResults[35]) + ","+ str(handRightResults[36]) + ","+ str(handRightResults[37]) + ","+ str(handRightResults[38]) + ","+ str(handRightResults[39]) + ","+ str(handRightResults[40]) + ","+ str(handRightResults[41]) + ","+parentName+");"
        crsr.execute(sql_command)
        
        
        
    connection.commit()  
    connection.close()


def synthesize_multiple(angle1,angle2):
    """
    extracting data from db
    """
    connection = sqlite3.connect("..\\..\\data\\db\\main_dataset.db") 
    crsr = connection.cursor()
    
    # extracting x and y points
    sql = 'SELECT x1,y1'
    for x in range(2,22):
        sql = sql + ',x'+str(x)+',y'+str(x)
    sql = sql + ' FROM rightHandDataset WHERE 1'
    crsr.execute(sql)
    feature_res = crsr.fetchall()
    features=[]
    for x in feature_res:
        features.append(x)
    
    # extracting labels
    crsr.execute('SELECT label FROM rightHandDataset WHERE 1')
    label_res = crsr.fetchall()
    labels=[]
    for x in label_res:
        labels.append(x)
    
    
     # connecting to the database  
    connection = sqlite3.connect("..\\..\\data\\db\\main_dataset.db") 
    # cursor  
    crsr = connection.cursor() 
    
    
    for x in range(len(features)):
        
        """
        sythesizing at angle 1
        """
        rotated = rotate.rotate_points(features[x],-angle1)
        handRightResults = helper.seperate_points(rotated)

        
        parentName = "'"+str(labels[x][0])+"'"
        
        # SQL command to insert the data in the table 
        sql_command = "INSERT INTO rightHandDataset VALUES (NULL, "+ str(handRightResults[0]) + ", "+ str(handRightResults[1]) + ","+ str(handRightResults[2]) + ","+ str(handRightResults[3]) + ","+ str(handRightResults[4]) + ","+ str(handRightResults[5]) + ","+ str(handRightResults[6]) + ","+ str(handRightResults[7]) + ","+ str(handRightResults[8]) + ","+ str(handRightResults[9]) + ","+ str(handRightResults[10]) + ","+ str(handRightResults[11]) + ","+ str(handRightResults[12]) + ","+ str(handRightResults[13]) + ","+ str(handRightResults[14]) + ","+ str(handRightResults[15]) + ","+ str(handRightResults[16]) + ","+ str(handRightResults[17]) + ","+ str(handRightResults[18]) + ","+ str(handRightResults[19]) + ","+ str(handRightResults[20]) + ","+ str(handRightResults[21]) + ","+ str(handRightResults[22]) + ","+ str(handRightResults[23]) + ","+ str(handRightResults[24]) + ","+ str(handRightResults[25]) + ","+ str(handRightResults[26]) + ","+ str(handRightResults[27]) + ","+ str(handRightResults[28]) + ","+ str(handRightResults[29]) + ","+ str(handRightResults[30]) + ","+ str(handRightResults[31]) + ","+ str(handRightResults[32]) + ","+ str(handRightResults[33]) + ","+ str(handRightResults[34]) + ","+ str(handRightResults[35]) + ","+ str(handRightResults[36]) + ","+ str(handRightResults[37]) + ","+ str(handRightResults[38]) + ","+ str(handRightResults[39]) + ","+ str(handRightResults[40]) + ","+ str(handRightResults[41]) + ","+parentName+");"
        crsr.execute(sql_command)                 
        
        rotated = rotate.rotate_points(features[x],angle1)
        handRightResults = helper.seperate_points(rotated)
        
        # SQL command to insert the data in the table 
        sql_command = "INSERT INTO rightHandDataset VALUES (NULL, "+ str(handRightResults[0]) + ", "+ str(handRightResults[1]) + ","+ str(handRightResults[2]) + ","+ str(handRightResults[3]) + ","+ str(handRightResults[4]) + ","+ str(handRightResults[5]) + ","+ str(handRightResults[6]) + ","+ str(handRightResults[7]) + ","+ str(handRightResults[8]) + ","+ str(handRightResults[9]) + ","+ str(handRightResults[10]) + ","+ str(handRightResults[11]) + ","+ str(handRightResults[12]) + ","+ str(handRightResults[13]) + ","+ str(handRightResults[14]) + ","+ str(handRightResults[15]) + ","+ str(handRightResults[16]) + ","+ str(handRightResults[17]) + ","+ str(handRightResults[18]) + ","+ str(handRightResults[19]) + ","+ str(handRightResults[20]) + ","+ str(handRightResults[21]) + ","+ str(handRightResults[22]) + ","+ str(handRightResults[23]) + ","+ str(handRightResults[24]) + ","+ str(handRightResults[25]) + ","+ str(handRightResults[26]) + ","+ str(handRightResults[27]) + ","+ str(handRightResults[28]) + ","+ str(handRightResults[29]) + ","+ str(handRightResults[30]) + ","+ str(handRightResults[31]) + ","+ str(handRightResults[32]) + ","+ str(handRightResults[33]) + ","+ str(handRightResults[34]) + ","+ str(handRightResults[35]) + ","+ str(handRightResults[36]) + ","+ str(handRightResults[37]) + ","+ str(handRightResults[38]) + ","+ str(handRightResults[39]) + ","+ str(handRightResults[40]) + ","+ str(handRightResults[41]) + ","+parentName+");"
        crsr.execute(sql_command)
        
        """
        sythesizing at angle 2
        """
        
        rotated = rotate.rotate_points(features[x],-angle2)
        handRightResults = helper.seperate_points(rotated)

        
        parentName = "'"+str(labels[x][0])+"'"
        
        # SQL command to insert the data in the table 
        sql_command = "INSERT INTO rightHandDataset VALUES (NULL, "+ str(handRightResults[0]) + ", "+ str(handRightResults[1]) + ","+ str(handRightResults[2]) + ","+ str(handRightResults[3]) + ","+ str(handRightResults[4]) + ","+ str(handRightResults[5]) + ","+ str(handRightResults[6]) + ","+ str(handRightResults[7]) + ","+ str(handRightResults[8]) + ","+ str(handRightResults[9]) + ","+ str(handRightResults[10]) + ","+ str(handRightResults[11]) + ","+ str(handRightResults[12]) + ","+ str(handRightResults[13]) + ","+ str(handRightResults[14]) + ","+ str(handRightResults[15]) + ","+ str(handRightResults[16]) + ","+ str(handRightResults[17]) + ","+ str(handRightResults[18]) + ","+ str(handRightResults[19]) + ","+ str(handRightResults[20]) + ","+ str(handRightResults[21]) + ","+ str(handRightResults[22]) + ","+ str(handRightResults[23]) + ","+ str(handRightResults[24]) + ","+ str(handRightResults[25]) + ","+ str(handRightResults[26]) + ","+ str(handRightResults[27]) + ","+ str(handRightResults[28]) + ","+ str(handRightResults[29]) + ","+ str(handRightResults[30]) + ","+ str(handRightResults[31]) + ","+ str(handRightResults[32]) + ","+ str(handRightResults[33]) + ","+ str(handRightResults[34]) + ","+ str(handRightResults[35]) + ","+ str(handRightResults[36]) + ","+ str(handRightResults[37]) + ","+ str(handRightResults[38]) + ","+ str(handRightResults[39]) + ","+ str(handRightResults[40]) + ","+ str(handRightResults[41]) + ","+parentName+");"
        crsr.execute(sql_command)                 
        
        rotated = rotate.rotate_points(features[x],angle2)
        handRightResults = helper.seperate_points(rotated)
        
        # SQL command to insert the data in the table 
        sql_command = "INSERT INTO rightHandDataset VALUES (NULL, "+ str(handRightResults[0]) + ", "+ str(handRightResults[1]) + ","+ str(handRightResults[2]) + ","+ str(handRightResults[3]) + ","+ str(handRightResults[4]) + ","+ str(handRightResults[5]) + ","+ str(handRightResults[6]) + ","+ str(handRightResults[7]) + ","+ str(handRightResults[8]) + ","+ str(handRightResults[9]) + ","+ str(handRightResults[10]) + ","+ str(handRightResults[11]) + ","+ str(handRightResults[12]) + ","+ str(handRightResults[13]) + ","+ str(handRightResults[14]) + ","+ str(handRightResults[15]) + ","+ str(handRightResults[16]) + ","+ str(handRightResults[17]) + ","+ str(handRightResults[18]) + ","+ str(handRightResults[19]) + ","+ str(handRightResults[20]) + ","+ str(handRightResults[21]) + ","+ str(handRightResults[22]) + ","+ str(handRightResults[23]) + ","+ str(handRightResults[24]) + ","+ str(handRightResults[25]) + ","+ str(handRightResults[26]) + ","+ str(handRightResults[27]) + ","+ str(handRightResults[28]) + ","+ str(handRightResults[29]) + ","+ str(handRightResults[30]) + ","+ str(handRightResults[31]) + ","+ str(handRightResults[32]) + ","+ str(handRightResults[33]) + ","+ str(handRightResults[34]) + ","+ str(handRightResults[35]) + ","+ str(handRightResults[36]) + ","+ str(handRightResults[37]) + ","+ str(handRightResults[38]) + ","+ str(handRightResults[39]) + ","+ str(handRightResults[40]) + ","+ str(handRightResults[41]) + ","+parentName+");"
        crsr.execute(sql_command)
        
        
        
    connection.commit()  
    connection.close()
















