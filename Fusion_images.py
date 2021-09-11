# -*- coding: utf-8 -*-
"""
2021.08.28
Celian Cherrier
v1.0

"""

#include Libraries
import numpy as np
import cv2
import os, os.path

#================================================================================
#Variables you can change
#================================================================================
#Folder with images to process
FolderWithImages="Frames"
#Output Folder for saving result images
OutputFolder='Result'
#Width of frames, defined in Autostart.py
FotoWidthInput=64
#Heigth of frames, defined in Autostart.py
FrameHeigth=1800
#Width of the middle of the frame you wish to use
FotoWidth=16
#Calculation of Offset for centering the image extraction
OffsetRealFotoWidth=int((FotoWidthInput-FotoWidth)/2)
#Number of single frames you wish to merge in one image
NumberFotoPerFrame=1000
#Number of images to produce 
NumberImageToProduce=21
# Ratio of the image merged with a gradient
FusionRatio=0.5
#================================================================================
#================================================================================

#START Fusion ================================
#calculation of various elements needed in order to merge images with a gradient instead of sticking images next to one another
LineToFuse=int(FusionRatio*FotoWidth)
LinesMiddle=FotoWidth-2*LineToFuse
MatrixFusionLeft=np.zeros((FrameHeigth,LineToFuse))

for i in range(LineToFuse):
    MatrixFusionLeft[:,i]=(i+1)/LineToFuse

MatrixFusionRight=np.flip(MatrixFusionLeft)-(1/LineToFuse)

#END Fusion ================================

#count images in folder
NumberOfFiles=len([name for name in os.listdir(FolderWithImages) if os.path.isfile(os.path.join(FolderWithImages, name))])

#Generate images
for k in range (NumberImageToProduce):
    Frame=np.zeros((FrameHeigth,(FotoWidth-LineToFuse)*NumberFotoPerFrame,3))
    for i in range(NumberFotoPerFrame):
        #iriri
        
        ImgName=FolderWithImages+'/Frame_'+str(i+NumberFotoPerFrame*k+1)+'.jpg'
        img = cv2.imread(ImgName, cv2.IMREAD_COLOR)
        img=img[:,OffsetRealFotoWidth:OffsetRealFotoWidth+FotoWidth,:]
        
        #FUSION=====
        #START: for each channel (RGB) adds the input image according to the gradient Matrix in the start of the output image
        if i>0:
            Frame[:,i*(FotoWidth-LineToFuse):i*(FotoWidth-LineToFuse)+LineToFuse,0]+=(img[:,0:LineToFuse,0]*MatrixFusionLeft).astype(int) 
            Frame[:,i*(FotoWidth-LineToFuse):i*(FotoWidth-LineToFuse)+LineToFuse,1]+=(img[:,0:LineToFuse,1]*MatrixFusionLeft).astype(int)
            Frame[:,i*(FotoWidth-LineToFuse):i*(FotoWidth-LineToFuse)+LineToFuse,2]+=(img[:,0:LineToFuse,2]*MatrixFusionLeft).astype(int)
        else:
            Frame[:,i*(FotoWidth-LineToFuse):i*(FotoWidth-LineToFuse)+LineToFuse,:]=img[:,0:LineToFuse,:]
        #MIDDLE: for each channel (RGB) adds the input image to the middle of the output image
        Frame[:,i*(FotoWidth-LineToFuse)+LineToFuse:(i+1)*(FotoWidth-LineToFuse),:]=img[:,LineToFuse:FotoWidth-LineToFuse,:]
        #END: for each channel (RGB) adds the input image according to the gradient Matrix in the end of the output image
        if i<NumberFotoPerFrame-1:
            Frame[:,(i+1)*(FotoWidth-LineToFuse):i*(FotoWidth-LineToFuse)+FotoWidth,0]+=(img[:,FotoWidth-LineToFuse:FotoWidth,0]*MatrixFusionRight).astype(int)
            Frame[:,(i+1)*(FotoWidth-LineToFuse):i*(FotoWidth-LineToFuse)+FotoWidth,1]+=(img[:,FotoWidth-LineToFuse:FotoWidth,1]*MatrixFusionRight).astype(int)
            Frame[:,(i+1)*(FotoWidth-LineToFuse):i*(FotoWidth-LineToFuse)+FotoWidth,2]+=(img[:,FotoWidth-LineToFuse:FotoWidth,2]*MatrixFusionRight).astype(int)
        else:
            Frame[:,(i+1)*(FotoWidth-LineToFuse)-LineToFuse:(i+1)*(FotoWidth-LineToFuse),:]=img[:,FotoWidth-LineToFuse:FotoWidth,:]  
    #Save the result    
    cv2.imwrite(OutputFolder+"/Result4_"+str(NumberFotoPerFrame*k)+".jpg",Frame)
    print("Image "+str(k+1)+" from "+str(NumberImageToProduce)+" processed.\n")