
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 19:02:38 2019

"""
import sqlite3 
import cv2
import json
import math
import move
import scale
import helperFunc as helper
import os
import normalize as norm
import inverse_kinematics as ik
import rotate

from matplotlib import pyplot as plt





folders = []
files = []
fileNames=[]

Dir = 'dataset'

files,fileNames,folders = helper.json_files(Dir)

js = json.loads(open("test_images\\name.json").read())
for items in js['people']:
    pose = items["pose_keypoints_2d"]
    handRight = items["hand_right_keypoints_2d"]
    handLeft = items["hand_left_keypoints_2d"]

pose_points = helper.removePoints(pose)
#posePoints = helper.join_points(pose_points)
p1 = [pose_points[0], pose_points[1]]
p2 = [pose_points[45], pose_points[46]]
distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
scaled_results,scaled_points = norm.dummyScaleBody(pose_points,distance)
poseResults,posePoints = norm.moveBody(scaled_results)

hand_right_points = helper.removePoints(handRight)
p1 = [hand_right_points[0], hand_right_points[1]]
p2 = [hand_right_points[18], hand_right_points[19]]
distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
RightResult,Points = scale.scalePoints(hand_right_points,distance)
handRightResults,handRightPoints = norm.move_to_wrist(RightResult,poseResults[8],poseResults[9])

# extract confidence points
RightConfPoints = helper.confidencePoints(handRight)
LeftConfPoints = helper.confidencePoints(handLeft)
# add all confidence points
RightConfidence = helper.confidence(RightConfPoints)
LeftConfidence = helper.confidence(LeftConfPoints)  
    
if LeftConfidence > 3:
    hand_left_points = helper.removePoints(handLeft)
    p1 = [hand_left_points[0], hand_left_points[1]]
    p2 = [hand_left_points[18], hand_left_points[19]]
    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
    if distance != 0: 
        LeftResult,Points = scale.scalePoints(hand_left_points,distance)
        handLeftResults,handLeftPoints = norm.move_to_wrist(LeftResult,poseResults[14],poseResults[15])
    else: 
        handLeftResults,handLeftPoints = norm.move_to_wrist(hand_left_points,poseResults[14],poseResults[15])

else:
    handLeftPoints = [(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0),(0, 0)]
    handLeftResults = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,]




#handRightResults,handRightPoints = move.movePoints(handRightResults,350,-0)
handRightResults,handRightPoints,handLeftResults,handLeftPoints = move.moveBothHands(handRightResults,handLeftResults,500,-100)

"""
inverse Kinematics rightArm
"""

p4 = poseResults[4]
p5 = poseResults[5]

p6 = poseResults[6]
p7 = poseResults[7]

p8 = poseResults[8]
p9 = poseResults[9]

p1 = [p4, p5]
p2 = [0, 0]
distanceX = p1[0]-p2[0]
distanceY = p1[1]-p2[1]

p4 -= distanceX
p5 -= distanceY

p6 -= distanceX
p7 -= distanceY

p8 -= distanceX
p9 -= distanceY


p1 = [p4, p5]
p2 = [p6, p7]
d1 = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )

p1 = [p6, p7]
p2 = [p8, p9]
d2 = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )


a1 = d1  # length of link a1
a2 = d2 # length of link a2 



# Desired Position of End effector
x = handRightResults[0]
x -= distanceX
y = handRightResults[1]
y -= distanceY


angle = ik.get_angle(x,y,a1,a2)




posePoints[3] = (int(posePoints[2][0]+a1),int(posePoints[2][1]))
posePoints[4] = (int(posePoints[3][0]+a2),int(posePoints[3][1]))



point4 = rotate.rotate(posePoints[4],angle[1],posePoints[3])
posePoints[4] = (int(point4[0]),int(point4[1]))

point3 = rotate.rotate(posePoints[3],angle[0],posePoints[2])
point4 = rotate.rotate(posePoints[4],angle[0],posePoints[2])

posePoints[3] = (int(point3[0]),int(point3[1]))
posePoints[4] = (int(point4[0]),int(point4[1]))


a = a1
b = a2 
p1 = [pose_points[4], pose_points[5]]
p2 = [pose_points[8], pose_points[9]]
c = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )


angleC = math.degrees( math.acos( (a**2 + b**2 - c**2)/(2*a*b) ) )

if (posePoints[3][0] > posePoints[2][0]-200) and posePoints[3][1] > 300 and posePoints[3][1] < 600:
    point3 = rotate.rotate(posePoints[3],180-angleC,posePoints[2])
#    posePoints[3] = (int(point3[0]),int(point3[1]))
    print("in condition 1")
    
if posePoints[3][1] < 300 and posePoints[3][0] < posePoints[1][0]:
    point3 = rotate.rotate(posePoints[3],270-angleC,posePoints[2])
    posePoints[3] = (int(point3[0]),int(point3[1]))
    print("in condition 2")    

if posePoints[3][0] > posePoints[1][0]:
    point3 = rotate.rotate(posePoints[3],90-angleC,posePoints[2])
#    posePoints[3] = (int(point3[0]),int(point3[1]))
    print("in condition 3")
 


"""
inverse Kinematics leftArm
"""

p4 = poseResults[10]
p5 = poseResults[11]

p6 = poseResults[12]
p7 = poseResults[13]

p8 = poseResults[14]
p9 = poseResults[15]

p1 = [p4, p5]
p2 = [0, 0]
distanceX = p1[0]-p2[0]
distanceY = p1[1]-p2[1]

p4 -= distanceX
p5 -= distanceY

p6 -= distanceX
p7 -= distanceY

p8 -= distanceX
p9 -= distanceY


p1 = [p4, p5]
p2 = [p6, p7]
d1 = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )

p1 = [p6, p7]
p2 = [p8, p9]
d2 = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )


a1 = d1  # length of link a1
a2 = d2 # length of link a2 



# Desired Position of End effector
x = handLeftResults[0]
x -= distanceX
y = handLeftResults[1]
y -= distanceY


angle = ik.get_angle(x,y,a1,a2)




posePoints[6] = (int(posePoints[5][0]+a1),int(posePoints[5][1]))
posePoints[7] = (int(posePoints[6][0]+a2),int(posePoints[6][1]))



point4 = rotate.rotate(posePoints[7],angle[1],posePoints[6])
posePoints[7] = (int(point4[0]),int(point4[1]))

point3 = rotate.rotate(posePoints[6],angle[0],posePoints[5])
point4 = rotate.rotate(posePoints[7],angle[0],posePoints[5])

posePoints[6] = (int(point3[0]),int(point3[1]))
posePoints[7] = (int(point4[0]),int(point4[1]))


a = a1
b = a2 
p1 = [pose_points[10], pose_points[11]]
p2 = [pose_points[14], pose_points[15]]
c = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )


#angleC = math.degrees( math.acos( (a**2 + b**2 - c**2)/(2*a*b) ) )

#if (posePoints[3][0] > posePoints[2][0]-200) and posePoints[3][1] > 300:
#    point3 = rotate.rotate(posePoints[3],180-angleC,posePoints[2])
#    posePoints[3] = (int(point3[0]),int(point3[1]))
#    print("in condition 1")
#    
#if posePoints[3][1] < 300 and posePoints[3][0] < posePoints[1][0]:
#    point3 = rotate.rotate(posePoints[3],270-angleC,posePoints[2])
#    posePoints[3] = (int(point3[0]),int(point3[1]))
#    print("in condition 2")    
#
#if posePoints[3][0] > posePoints[1][0]:
#    point3 = rotate.rotate(posePoints[3],90-angleC,posePoints[2])
#    posePoints[3] = (int(point3[0]),int(point3[1]))
#    print("in condition 3")    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
## Equations for Inverse kinematics
#h = math.sqrt( ((x - 0)**2)+((y - 0)**2) )  # eqn 1
#
#beta = math.degrees(-math.acos( (x**2 + y**2 - a1**2 - a2**2)/(2*a1*a2) ))
#
#alpha = math.degrees( math.atan(y/x) + math.atan( (a2*math.sin(beta)) / (a1+a2*math.cos(beta)) ) )



    
    
#
#
#X1=a1*math.cos(180)+distanceX 
#Y1=a1*math.sin(180)+distanceY 
#
#posePoints[3] = (int(X1),int(Y1))
#
#
#X2=a2*math.cos(90) +distanceX
#Y2=a2*math.sin(90) +distanceY
#
#posePoints[4] = (int(X2),int(Y2))
#



#colors = [ [0, 0, 130], [0, 0, 175],[0,0, 210],[0, 0, 250] , 
#          [0,200,160], [0,180,150],[0,230,186],[0,255,255],
#             [82,201,8], [82,204,0], [92,230,0], [102,252,6], 
#             [197,88,17], [204,82,0],[179,71,0],[227,94,5],
#             [204,0,163], [200,0,163], [196,0,163], [230,0,184]]
#    
#    
#
#color="black"
#color = color.capitalize()
#
#background = color+'_background.jpg'
#    
#frame = cv2.imread(background)
#
##calc = (int(X1+distanceX),int(Y1+distanceY))
##
##cv2.line(frame, (int(X1),int(Y1)), (int(distanceX),int(distanceY)), colors[7], 10)
##cv2.circle(frame, (int(distanceX),int(distanceY)), 5, colors[0], thickness=10, lineType=cv2.FILLED)
#
##
##cv2.line(frame, (int(X2),int(Y2)), (int(X1),int(Y1)), colors[11], 10)
##cv2.circle(frame, (int(X1),int(Y1)), 5, colors[0], thickness=10, lineType=cv2.FILLED)
##cv2.circle(frame, (int(X2),int(Y2)), 15, (0,0,0), thickness=5, lineType=-1)
##
##fig2 = plt.figure(figsize = (10,10)) # create a 20 x 20 figure 
##ax3 = fig2.add_subplot(111)
##ax3.imshow(frame, interpolation='none')
##
##plt.imshow(frame)
##plt.show()






























def plotPose(posePoints,handRightPoints,handLeftPoints):
    POSE_PAIRS = [ [1,0],[1,2],[1,5],[2,3],[3,4],[5,6],[6,7],
              [1,8],[0,15],[15,17],[0,16],[16,18]]

    HAND_PAIRS = [ [0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],
                  [10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],
                  [18,19],[19,20] ]
    
    colors = [ [0, 0, 130], [0, 0, 175],[0,0, 210],[0, 0, 250] , 
              [0,200,160], [0,180,150],[0,230,186],[0,255,255],
                 [82,201,8], [82,204,0], [92,230,0], [102,252,6], 
                 [197,88,17], [204,82,0],[179,71,0],[227,94,5],
                 [204,0,163], [200,0,163], [196,0,163], [230,0,184]]
    
    
    
    color="black"
    color = color.capitalize()
    
    background = color+'_background.jpg'
        
    frame = cv2.imread(background)
    
    
    count=0
    # Draw Skeleton
    for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]
    
        if posePoints[partA] and posePoints[partB] and posePoints[partA][0]!=0 and posePoints[partA][1]!=0 and posePoints[partB][0]!=0 and posePoints[partB][1]!=0 :
            
            if color == 'White':
                cv2.line(frame, posePoints[partA], posePoints[partB], colors[count], 10)
                cv2.circle(frame, posePoints[partA], 5, colors[count], thickness=10, lineType=cv2.FILLED)
                cv2.circle(frame, posePoints[partB], 15, (0,0,0), thickness=5, lineType=-1)
                
            else:
                cv2.line(frame, posePoints[partA], posePoints[partB], colors[count], 10)
                cv2.circle(frame, posePoints[partA], 5, (0, 0, 255), thickness=10, lineType=cv2.FILLED)
                cv2.circle(frame, posePoints[partB], 5, (255, 255, 255), thickness=15, lineType=cv2.FILLED)
        count+=1
    
    count=0
    for pair in HAND_PAIRS:
        partA = pair[0]
        partB = pair[1]
    
        if handRightPoints[partA] and handRightPoints[partB]:
            
            if color == 'White':
                cv2.line(frame, handRightPoints[partA], handRightPoints[partB], colors[count], 10)
                cv2.circle(frame, handRightPoints[partA], 5, colors[count], thickness=10, lineType=cv2.FILLED)
                cv2.circle(frame, handRightPoints[partB], 15, (0,0,0), thickness=5, lineType=-1)
                
            else:
                cv2.line(frame, handRightPoints[partA], handRightPoints[partB], colors[count], 10)
                cv2.circle(frame, handRightPoints[partA], 5, (0, 0, 255), thickness=3, lineType=cv2.FILLED)
                cv2.circle(frame, handRightPoints[partB], 5, (255, 255, 255), thickness=4, lineType=cv2.FILLED)
            count+=1
            
    
    count=0
    for pair in HAND_PAIRS:
        partA = pair[0]
        partB = pair[1]
    
        if handLeftPoints[partA] and handLeftPoints[partB]:
            
            if color == 'White':
                cv2.line(frame, handLeftPoints[partA], handLeftPoints[partB], colors[count], 10)
                cv2.circle(frame, handLeftPoints[partA], 5, colors[count], thickness=10, lineType=cv2.FILLED)
                cv2.circle(frame, handLeftPoints[partB], 15, (0,0,0), thickness=5, lineType=-1)
                
            else:
                cv2.line(frame, handLeftPoints[partA], handLeftPoints[partB], colors[count], 10)
                cv2.circle(frame, handLeftPoints[partA], 5, (0, 0, 255), thickness=3, lineType=cv2.FILLED)
                cv2.circle(frame, handLeftPoints[partB], 5, (255, 255, 255), thickness=4, lineType=cv2.FILLED)
            count+=1
    
    
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    return frame


frame = plotPose(posePoints,handRightPoints,handLeftPoints)

fig2 = plt.figure(figsize = (10,10)) # create a 20 x 20 figure 
ax3 = fig2.add_subplot(111)
ax3.imshow(frame, interpolation='none')

plt.imshow(frame)
plt.show()



















