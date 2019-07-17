# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 17:55:56 2019

"""

import numpy as np 
import matplotlib.pyplot as plt 
import math

# Robot Link Length Parameter
link = [188, 173]
# Robot Initial Joint Values (degree)
angle = [0, 0]
# Target End of Effector Position
target = [0, 0, 0] 




def rotateZ(theta):
    rz = np.array([[math.cos(theta), - math.sin(theta), 0, 0],
                   [math.sin(theta), math.cos(theta), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])
    return rz

def translate(dx, dy, dz):
    t = np.array([[1, 0, 0, dx],
                  [0, 1, 0, dy],
                  [0, 0, 1, dz],
                  [0, 0, 0, 1]])
    return t

# Forward Kinematics
# Input initial angles and length of links
# Output positions each points
def FK(angle, link):
    n_links = len(link)
    P = []
    P.append(np.eye(4))
    for i in range(0, n_links):
        R = rotateZ(angle[i]/180*math.pi)
        T = translate(link[i], 0, 0)
        P.append(P[-1].dot(R).dot(T))
    return P

def IK(target, angle, link, max_iter = 10000, err_min = 0.1):
    solved = False
    err_end_to_target = math.inf
    
    for loop in range(max_iter):
        for i in range(len(link)-1, -1, -1):
            P = FK(angle, link)
            end_to_target = target - P[-1][:3, 3]
            err_end_to_target = math.sqrt(end_to_target[0] ** 2 + end_to_target[1] ** 2)
            if err_end_to_target < err_min:
                solved = True
            else:
                # Calculate distance between i-joint position to end effector position
                # P[i] is position of current joint
                # P[-1] is position of end effector
                cur_to_end = P[-1][:3, 3] - P[i][:3, 3]
                cur_to_end_mag = math.sqrt(cur_to_end[0] ** 2 + cur_to_end[1] ** 2)
                cur_to_target = target - P[i][:3, 3]
                cur_to_target_mag = math.sqrt(cur_to_target[0] ** 2 + cur_to_target[1] ** 2)

                end_target_mag = cur_to_end_mag * cur_to_target_mag

                if end_target_mag <= 0.0001:    
                    cos_rot_ang = 1
                    sin_rot_ang = 0
                else:
                    cos_rot_ang = (cur_to_end[0] * cur_to_target[0] + cur_to_end[1] * cur_to_target[1]) / end_target_mag
                    sin_rot_ang = (cur_to_end[0] * cur_to_target[1] - cur_to_end[1] * cur_to_target[0]) / end_target_mag

                rot_ang = math.acos(max(-1, min(1,cos_rot_ang)))

                if sin_rot_ang < 0.0:
                    rot_ang = -rot_ang

                # Update current joint angle values
                angle[i] = angle[i] + (rot_ang * 180 / math.pi)

                if angle[i] >= 360:
                    angle[i] = angle[i] - 360
                if angle[i] < 0:
                    angle[i] = 360 + angle[i]
                  
        if solved:
            break
            
    return angle, err_end_to_target, solved, loop

# Have not implemented
def get_angle(x,y,d1,d2):
    global target, link, angle, ax
    
    link = [d1, d2]
    
    target[0] = x
    target[1] = y
    
    
    # Inverse Kinematics
    angle, err, solved, iteration = IK(target, angle, link, max_iter=1000)
    
    return angle






















































#import numpy as np 
#import matplotlib.pyplot as plt 
#import math
#
## Robot Link Length Parameter
#link = [188, 173]
## Robot Initial Joint Values (degree)
#angle = [0, 0]
## Target End of Effector Position
#target = [0, 0, 0] 
#
## Create figure to plot
#fig = plt.figure() 
#ax = fig.add_subplot(1,1,1)
#
## Draw Axis
#def draw_axis(ax, scale=1.0, A=np.eye(4), style='-', draw_2d = False):
#    xaxis = np.array([[0, 0, 0, 1], 
#                      [scale, 0, 0, 1]]).T
#    yaxis = np.array([[0, 0, 0, 1], 
#                      [0, scale, 0, 1]]).T
#    zaxis = np.array([[0, 0, 0, 1], 
#                      [0, 0, scale, 1]]).T
#    
#    xc = A.dot( xaxis )
#    yc = A.dot( yaxis )
#    zc = A.dot( zaxis )
#    
#    if draw_2d:
#        ax.plot(xc[0,:], xc[1,:], 'r' + style)
#        ax.plot(yc[0,:], yc[1,:], 'g' + style)
#    else:
#        ax.plot(xc[0,:], xc[1,:], xc[2,:], 'r' + style)
#        ax.plot(yc[0,:], yc[1,:], yc[2,:], 'g' + style)
#        ax.plot(zc[0,:], zc[1,:], zc[2,:], 'b' + style)
#
#def rotateZ(theta):
#    rz = np.array([[math.cos(theta), - math.sin(theta), 0, 0],
#                   [math.sin(theta), math.cos(theta), 0, 0],
#                   [0, 0, 1, 0],
#                   [0, 0, 0, 1]])
#    return rz
#
#def translate(dx, dy, dz):
#    t = np.array([[1, 0, 0, dx],
#                  [0, 1, 0, dy],
#                  [0, 0, 1, dz],
#                  [0, 0, 0, 1]])
#    return t
#
## Forward Kinematics
## Input initial angles and length of links
## Output positions each points
#def FK(angle, link):
#    n_links = len(link)
#    P = []
#    P.append(np.eye(4))
#    for i in range(0, n_links):
#        R = rotateZ(angle[i]/180*math.pi)
#        T = translate(link[i], 0, 0)
#        P.append(P[-1].dot(R).dot(T))
#    return P
#
#def IK(target, angle, link, max_iter = 10000, err_min = 0.1):
#    solved = False
#    err_end_to_target = math.inf
#    
#    for loop in range(max_iter):
#        for i in range(len(link)-1, -1, -1):
#            P = FK(angle, link)
#            end_to_target = target - P[-1][:3, 3]
#            err_end_to_target = math.sqrt(end_to_target[0] ** 2 + end_to_target[1] ** 2)
#            if err_end_to_target < err_min:
#                solved = True
#            else:
#                # Calculate distance between i-joint position to end effector position
#                # P[i] is position of current joint
#                # P[-1] is position of end effector
#                cur_to_end = P[-1][:3, 3] - P[i][:3, 3]
#                cur_to_end_mag = math.sqrt(cur_to_end[0] ** 2 + cur_to_end[1] ** 2)
#                cur_to_target = target - P[i][:3, 3]
#                cur_to_target_mag = math.sqrt(cur_to_target[0] ** 2 + cur_to_target[1] ** 2)
#
#                end_target_mag = cur_to_end_mag * cur_to_target_mag
#
#                if end_target_mag <= 0.0001:    
#                    cos_rot_ang = 1
#                    sin_rot_ang = 0
#                else:
#                    cos_rot_ang = (cur_to_end[0] * cur_to_target[0] + cur_to_end[1] * cur_to_target[1]) / end_target_mag
#                    sin_rot_ang = (cur_to_end[0] * cur_to_target[1] - cur_to_end[1] * cur_to_target[0]) / end_target_mag
#
#                rot_ang = math.acos(max(-1, min(1,cos_rot_ang)))
#
#                if sin_rot_ang < 0.0:
#                    rot_ang = -rot_ang
#
#                # Update current joint angle values
#                angle[i] = angle[i] + (rot_ang * 180 / math.pi)
#
#                if angle[i] >= 360:
#                    angle[i] = angle[i] - 360
#                if angle[i] < 0:
#                    angle[i] = 360 + angle[i]
#                  
#        if solved:
#            break
#            
#    return angle, err_end_to_target, solved, loop
#
## Have not implemented
#def onclick(event):
#    global target, link, angle, ax
#    target[0] = event.xdata
#    target[1] = event.ydata
#    
#    print("Target Position : ", target)
#    plt.cla()
#    ax.set_xlim(-50, 1950)
#    ax.set_ylim(-50, 1080)
#
#    # Inverse Kinematics
#    angle, err, solved, iteration = IK(target, angle, link, max_iter=1000)
#    
#    P = FK(angle, link)
#    for i in range(len(link)):
#        start_point = P[i]
#        end_point = P[i+1]
#        ax.plot([start_point[0,3], end_point[0,3]], [start_point[1,3], end_point[1,3]], linewidth=5)
#        # draw_axis(ax, scale=5, A=P[i+1], draw_2d=True)
#
#    if solved:
#        print("\nIK solved\n")
#        print("Iteration :", iteration)
#        print("Angle :", angle)
#        print("Target :", target)
#        print("End Effector :", P[-1][:3, 3])
#        print("Error :", err)
#    else:
#        print("\nIK error\n")
#        print("Angle :", angle)
#        print("Target :", target)
#        print("End Effector :", P[-1][:3, 3])
#        print("Error :", err)
#    plt.show()
#
#def main():
#    fig.canvas.mpl_connect('button_press_event', onclick)
#    fig.suptitle("Cyclic Coordinate Descent - Inverse Kinematics", fontsize=12)
#    ax.set_xlim(-50, 1950)
#    ax.set_ylim(-50, 1080)
#
#    # Forward Kinematics
#    P = FK(angle, link)
#    # Plot Link
#    for i in range(len(link)):
#        start_point = P[i]
#        end_point = P[i+1]
#        ax.plot([start_point[0,3], end_point[0,3]], [start_point[1,3], end_point[1,3]], linewidth=5)
#        # draw_axis(ax, scale=5, A=P[i+1], draw_2d=True)
#    plt.show()
#
#if __name__ == "__main__":
#    main()
















































#from numpy import *
#
#a1 = 0  # length of link a1 in cm
#a2 = 188.2 # length of link a2 in cm
#a3 = 0  # length of link a3 in cm
#a4 = 173.6  # length of link a4 in cm
#
## Desired Position of End effector
#x = 1000
#y = 600
#
## Equations for Inverse kinematics
#r1 = sqrt(x**2+y**2)  # eqn 1
#phi_1 = arccos((a4**2-a2**2-r1**2)/(-2*a2*r1))  # eqn 2
#phi_2 = arctan2(y, x)  # eqn 3
#theta_1 = rad2deg(phi_2-phi_1)  # eqn 4 converted to degrees
#
#phi_3 = arccos((r1**2-a2**2-a4**2)/(-2*a2*a4))
#theta_2 = 180-rad2deg(phi_3)
#
#print('theta one: ', theta_1)
#print('theta two: ', theta_2)















#def deg(rad ):
#    return rad * 180 / math.pi
#
#def angle_of_rot(len1,len2,d,resX,resY,orgX,orgY):
#    length0 = len1
#    length1 = len2
#    
#    # Distance from Joint0 to Target
#    length2 = d
#     
#    #Inner angle alpha
#    cosAngle0 = ((length2 * length2) + (length0 * length0) - (length1 * length1)) / (2 * length2 * length0);
#    angle0 = math.acos(cosAngle0) * math.Rad2Deg;
#     
#    #Inner angle beta
#    cosAngle1 = ((length1 * length1) + (length0 * length0) - (length2 * length2)) / (2 * length1 * length0);
#    angle1 = math.acos(cosAngle1) * math.Rad2Deg;
#     
#    #Angle from Joint0 and Target
#    p1 = [resX, resY]
#    p2 = [orgX, orgY]
#    distanceX = p1[0]-p2[0]
#    distanceY = p1[1]-p2[1]
#    diff = (distanceX,distanceY)
#    atan = math.Atan2(diff.y, diff.x) * math.Rad2Deg;
#     
#    #So they work in Unity reference frame
#    jointAngle0 = atan - angle0  #Angle A
#    jointAngle1 = 180 - angle1  #Angle B
#    return jointAngle0 , jointAngle1























#def angle_of_rot(len1,len2,d,resX,resY):
#    
#
#    """
#    The lengths of the two segments of the robot’s arm. 
#    Using the same length for both segments allows the robot
#    to reach the (0,0) coordinate.
#    """
##    len1 = 182.2
##    len2 = 172.6
##    resX=72.0
##    resY=22.0
#    
#    """
#    The law of cosines, transfomred so that C is the unknown.
#    The names of the sides and angles correspond to the standard 
#    names in mathematical writing. Later, we have to map the sides 
#    and angles from our scenario to a, b, c, and C, respectively.
#    """
#    def lawOfCosines(a, b, c):
#    	return math.acos((a*a + b*b - c*c) / (2 * a * b))
#    
#    """
#    The distance from (0,0) to (x,y). HT to Pythagoras.
#    """
#    def distance(x, y ):
#    	return math.sqrt(x*x + y*y)
#    
#    """
#    Calculating the two joint angles for given x and y.
#    """
#    def angles(x, y ) :
#        #First, get the length of line dist.
#        dist = d
#        
#        #Calculating angle D1 is trivial. Atan2 is a modified arctan() function
#        #that returns unambiguous results.
#    
#        D1 = math.atan2(y, x)
#        
#        #D2 can be calculated using the law of cosines where
#        #a = dist, b = len1, and c = len2.
#    
#        D2 = lawOfCosines(dist, len1, len2)
#        #Then A1 is simply the sum of D1 and D2.
#    
#        A1 = D1 + D2
#    
#        #A2 can also be calculated with the law of cosine, but this time with a = len1, b = len2, and c = dist.
#        A2 = lawOfCosines(len1, len2, dist)
#    
#        return A1, A2
#    
#    """
#    Convert radians into degrees.
#    """
#    def deg(rad ):
#    	return rad * 180 / math.pi
#    
#    
#    x, y = resX, resY
#    a1, a2 = angles(x, y)
#    return deg(a1),deg(a2)
##    print("x="+ str(x) +" y= "+ str(y) + " \nA1= "+ str(a1) +" deg(a1)= "+ str(deg(a1)) +" \nA2= "+ str(a2)+ " deg(a2)= "+str(deg(a2)))
#
















