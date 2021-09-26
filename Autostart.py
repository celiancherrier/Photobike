# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 18:50:18 2021

@author: celian
"""

import picamera
from time import sleep
import datetime
import RPi.GPIO as GPIO
import os, os.path

#duration of videos, only integer
VideoDuration=60
#Number of Frames per wheel rotation (360°)
TriggerPerWheelTurn=20
#Number of wheel rotation between two speed update (only integer, at least one). Value 1 recommended
WheelTurnPerUpdateFramerate=1
#Initialisation of Triggerperiod
CurrentTriggerPeriod=0.01
OldTriggerPeriod=0.01
TriggerPeriod=1000
#Initialisation of Timers
NewTimer=datetime.datetime.today()
OldTimer=NewTimer


#Setup GPIO
GPIO.setmode(GPIO.BCM)

# GPIO 18 (Pin 12) als Input definieren und Pullup-Widerstand aktivieren
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

#Declaration of the camera
camera=picamera.PiCamera()
TriggerCounter=0

#Function that count triggers on each wheel turn, triggers the update of framerate every WheelTurnPerUpdateFramerate turns
def CounterOfTrigger(channel):
    global TriggerCounter
    if TriggerCounter<WheelTurnPerUpdateFramerate:
        TriggerCounter+=1
    else:
        TriggerCounter=0
        Interrupt()

#Function that calculates the current speeds and adapts the current framerate
def Interrupt():
    global TriggerCounter
    global CurrentTriggerPeriod
    global OldTriggerPeriod
    global TriggerPeriod
    global NewTimer
    global OldTimer
    #Update timers for speer measurement
    NewTimer=datetime.datetime.today()
    OldTriggerPeriod=CurrentTriggerPeriod
    CurrentTriggerPeriod=(NewTimer-OldTimer).total_seconds()/WheelTurnPerUpdateFramerate
    TriggerPeriod=(CurrentTriggerPeriod+(max(0,CurrentTriggerPeriod-OldTriggerPeriod))/2)/TriggerPerWheelTurn
    OldTimer=NewTimer
    #Calculate new frequency
    Frequency=max(1,min(90,1/TriggerPeriod))
    #Update framerate with framerate_delta (update directly of framerate doesn't work during a video capture)
    camera.framerate_delta=max(Frequency-60,-59) 

#Interrput on Reed Sensor trigger
GPIO.add_event_detect(18, GPIO.RISING, callback = CounterOfTrigger, bouncetime = 50)

#Set up camera at Start
camera.resolution=(64,1800)
camera.rotation=180
sleep(2)
camera.framerate=60
camera.framerate_delta=0

NombreImages=len([name for name in os.listdir('Videos') if os.path.isfile(os.path.join('Videos', name))])

#Loop for recording single Videos
while True:
        if(TriggerPeriod<1000):    
            camera.start_recording('Videos/Video_'+str(NombreImages)+'.h264')
            camera.wait_recording(VideoDuration)
            camera.stop_recording()
            NombreImages+=1
            if NombreImages%5==0:
                camera.close()
                camera=picamera.PiCamera()
                camera.resolution=(64,1800)
                camera.rotation=180
                sleep(2)
                camera.framerate=60
                camera.framerate_delta=0