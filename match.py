# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 01:43:14 2018

"""

import json
import sqlite3
import math
import move
import helperFunc as helper
import scale


i=1
class StdevFunc:
    """
    For use as an aggregate function in SQLite
    """
    def __init__(self):
       try:
         self.M = 0.0
         self.S = 0.0
         self.k = 0
       except:
         pass

    def step(self, value):
        try:
            # automatically convert text to float, like the rest of SQLite
            val = float(value) # if fails, skips this iteration, which also ignores nulls
            tM = self.M
            self.k += 1
            self.M += ((val - tM) / self.k)
            self.S += ((val - tM) * (val - self.M))
        except:
            pass

    def finalize(self):
        if self.k <= 1: # avoid division by zero
            return None
        else:
            return math.sqrt(self.S / (self.k-1))
        

def match(fileName):
     
    sd_mult = 2.5
    tolerence = 9
    
    js = json.loads(open(fileName).read())
    for items in js['people']:
        handRight = items["hand_right_keypoints_2d"]
    
    handPoints = helper.removePoints(handRight)
    
    handRightResults,handRightPoints = move.centerPoints(handPoints)
    
#    p1 = [Results[0], Results[1]]
#    p2 = [Results[17], Results[18]]
#    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
#    
##    print(distance)
#    
#    handRightResults,handRightPoints = scale.scalePoints(Results,distance)
    
    # connecting to the database  
    connection = sqlite3.connect("db\\dataset_saad.db") 
    connection.create_aggregate("stdev", 1, StdevFunc)
    crsr = connection.cursor()
    
    crsr.execute("SELECT count(distinct(label)) FROM rightHandDataset")
    count = crsr.fetchall()
    crsr.execute("SELECT distinct(label) FROM rightHandDataset") 
    label = crsr.fetchall() 
    c = count[0][0]
    
    handRightX1 = []
    handRightY1 = []
    
    for x in range(0,len(handRightResults),2): 
        handRightX1.append(handRightResults[x])
    for x in range(1,len(handRightResults),2): 
        handRightY1.append(handRightResults[x])
    
    result_count = 0
    result = ""
    
    
    result_points = []  
    score = 0;
    for y in range(0,c):
        result1 = []
        result2 = [] 
        
        l = label[y][0]
        l = "'" + l + "'"
        
        sql_avg =  'SELECT avg(x1),avg(y1)'
        sql_sd = 'SELECT STDEV(x1),STDEV(y1)'
        
        for x in range(2,22):
            sql_avg = sql_avg + ', avg(x'+str(x)+'),avg(y'+str(x)+')'
            sql_sd = sql_sd + ', STDEV(x'+str(x)+'),STDEV(y'+str(x)+')'
        
        sql_avg = sql_avg + ' FROM rightHandDataset WHERE label = '+ l 
        sql_sd = sql_sd + ' FROM rightHandDataset WHERE label = '+ l 
        
        #print(sql_sd)
    
        crsr.execute(sql_avg)
        ans1 = crsr.fetchall()
        
        for i in ans1: 
            result1.append(i)
            try:     
                crsr.execute(sql_sd)
            except:
                pass
        ans2 = crsr.fetchall()
        
        for i in ans2: 
            result2.append(i)
    
        handRightX2 = []
        handRightY2 = []
        
        
        
        for x in range(0,len(result1[0]),2): 
            handRightX2.append(result1[0][x])
        for x in range(1,len(result1[0]),2): 
            handRightY2.append(result1[0][x])
        
        avgSd = []
        
        for x in range(0,len(result2[0]),2): 
            avgSd.append(((result2[0][x] + result2[0][x+1])/2))
        
        
        match_count = 0
        
        
        
        for x in range(len(handRightX1)):
            p1 = [handRightX1[x], handRightY1[x]]
            p2 = [handRightX2[x], handRightY2[x]]
        
            if (math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )) <= avgSd[x] * sd_mult :
                match_count+=1
        
        
        if match_count > result_count:
            result_count = match_count
            score = match_count
            result_points = result1
            if result_count > tolerence:
                result = label[y][0]
            else:
                result = "no match"
        
        
#        print(l)
#        print(match_count)
##        print(result1)
#    
#    print("\n--------------------------------------------------------------")
#    print(result)
#    print("--------------------------------------------------------------")
#    
    connection.commit()  
    connection.close()
    
    return result,result_points,score















