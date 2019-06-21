# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 04:01:24 2019

"""

import db_helper as dbh
from matplotlib import pyplot as plt
import plot 

# create table if not exists
dbh.create_table()
# add all records from 'dataset' to 'db\main_databse.db'
dbh.populate_db()


frame = []
frame = plot.plot_db_label('ا')

for x in range(len(frame)):
    plt.imshow(frame[x])
    plt.show()