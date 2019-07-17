# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 23:30:17 2019

"""

import numpy as np
from numpy import *

a1 = 6.2  # length of link a1 in cm
a2 = 5.2  # length of link a2 in cm
a3 = 0  # length of link a3 in cm
a4 = 7  # length of link a4 in cm

theta_1 = 45  # theta 1 angle in degrees
theta_2 = 45  # theta 2 angle in degrees

theta_1 = (theta_1/180)*pi  # theta 1 in radians
theta_2 = (theta_2/180)*pi  # theta 2 in radians

R0_1 = [[cos(theta_1), -sin(theta_1), 0],
        [sin(theta_1), cos(theta_1), 0],
        [0, 0, 1]]

R1_2 = [[cos(theta_2), -sin(theta_2), 0],
        [sin(theta_2), cos(theta_2), 0],
        [0, 0, 1]]

R0_2 = dot(R0_1, R1_2)  # dot product

# Displacement vectors
d0_1 = [[a2*cos(theta_1)], [a2*sin(theta_1)], [a1]]
d1_2 = [[a4*cos(theta_2)], [a4*sin(theta_2)], [a3]]

# Homogeneous transformation matrix from Joint 0 to 1
H0_1 = concatenate((R0_1, d0_1), 1)  # 1 appends to the right
H0_1 = concatenate((H0_1, [[0, 0, 0, 1]]), 0)  # 0 appends to the bottom

print(matrix(H0_1))
print('\n')

# Homogeneous transformation matrix from Joint 1 to 2
H1_2 = concatenate((R1_2, d1_2), 1)  # 1 appends to the right
H1_2 = concatenate((H1_2, [[0, 0, 0, 1]]), 0)  # 0 appends to the bottom

# Homogeneous transformation matrix from Joint 1 to 2
H0_2 = dot(H0_1, H1_2)

print(matrix(H0_2))












