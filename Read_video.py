# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 18:29:54 2021

@author: celian
"""

import cv2

i=0

# Number of videos generated to process
NumberVideosToProcess=26

#Loop over video
for videoprise in range(NumberVideosToProcess):

    #Open video
    cap = cv2.VideoCapture('Video_'+str(videoprise)+'.mp4')
    if (cap.isOpened()== False):
        print("Error opening video stream or file")
    
    #Loop over frames of the video
    while(cap.isOpened()):
        ret,frame=cap.read()
        if ret==False:
            break
        #Export frame as image
        cv2.imwrite('Frames/Frame_'+str(i)+'.jpg',frame)
        #increment counter
        i+=1
        #Feedback on Process
        print('Video'+str(videoprise)+'/'+str(NumberVideosToProcess)+' processed')
        