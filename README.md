# Conversion of Pakistan Sign Language into text and speech using Machine Learning
[The University of Lahore (Department of CS & IT)](https://cs.uol.edu.pk/) (Fall 2015 – Spring 2019) - Final Year Project

#### Supervised by:
[Dr. Muasser Naseer](https://faculty.uol.edu.pk/Faculty/9381/Dr%20Mudasser%20Naseer)
#### Group Members
- Muhammad Junaid Ejaz
- Muhammad Saad Qadri

#### The project is divided into 3 main modules
- RealTime sign detection module - convert Pakistan Sign Language (PSL) alphabet and words into text and speech in realtime.
- Capture Dataset modeule - Automated system for capturing and adding new data to the dataset
- PSl learning module - Learn PSL interactively

## Dependencies
##### The system uses OpenPose library for extacting skelatal features.
##### The code was developed with python 3.7 and has been tested with the libraries/versions in requirements.txt file.

## Dataset Used
We have made our own Pakistan Sign Language (PSL) dataset containing multiple samples of 37 urdu aplhabets and 12 urdu words. The dataset is made publically available at https://www.kaggle.com/saadbutt321/pakistan-sign-language-dataset

## External resources
OpenPose GitHub repo: https://github.com/CMU-Perceptual-Computing-Lab/openpose
Origin of OpenPose: https://github.com/ZheC/Realtime_Multi-Person_Pose_Estimation
Paper describing the method: https://arxiv.org/abs/1611.08050
Keras implementation of the Realtime Multi-Person Pose Estimation (my major inspiration): https://github.com/michalfaber/keras_Realtime_Multi-Person_Pose_Estimation
