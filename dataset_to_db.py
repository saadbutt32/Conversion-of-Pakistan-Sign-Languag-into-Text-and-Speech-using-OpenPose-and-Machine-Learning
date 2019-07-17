# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 09:45:03 2019

"""

import db_helper as dbh
import synthesize_data as synth

# create table if not exists
dbh.create_table()

# add all records from 'dataset' to 'db\main_databse.db'
dbh.populate_db()

# sythesize at two different angles (4 angles[- and +])
#synth.synthesize_multiple(10,20)

# add rotated data 'db\main_databse.db'
# func takes angle of rotation as parameter 
synth.synthesize(20)

