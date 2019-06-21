# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 04:01:24 2019

"""
from matplotlib import pyplot as plt
import plot 

frame = []
frame = plot.plot_db_label('ا')

for x in range(len(frame)):
    plt.imshow(frame[x])
    plt.show()