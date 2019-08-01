"""
Created on Fri Jul  5 09:45:03 2019

"""

import PSL.helper.db_helper as dbh
import PSL.helper.synthesize_data as synth
import PSL.alphabet_recognition.train_alphabet_model as alphabet_model
import PSL.word_recognition.train_word_model as word_model

# 0 = 'alphabet mode' , 1 = 'word mode'
#mode = 1

def re_train(mode):
    if mode == 0:
        # create table if not exists
        dbh.create_table()
        # add all records from 'dataset' to 'db\main_databse.db'
        dbh.populate_db()
        
        # add rotated data 'db\main_databse.db'
        # func takes angle of rotation as parameter 
        synth.synthesize(20)
        alphabet_model.train_alphabets()
        
    if mode == 1:
        # create table if not exists
        dbh.create_pose_table()
        # add all records from 'dataset' to 'db\main_databse.db'
        dbh.populate_words()
        
        word_model.train_words()



