#!/usr/bin/env python

import RPi.GPIO as GPIO
from pushetta import Pushetta
from time import sleep

count=0
PIN_NO=37 

# pushetta setup ..............................
API = "dd26b7688319812ed4c220fb72de905ccd9d2d8a"
CHANNEL_NAME = "CarSecSys"
MESSAGE = "Your Car Has Been Intruded."
p = Pushetta(API)

def startupAlert():
    p.pushMessage(CHANNEL_NAME,"Intrusion Detection Device is ON")
    return
    
def sendAlert():
    p.pushMessage(CHANNEL_NAME,MESSAGE)
    return

# GPIO setup ...................................
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_NO, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

startupAlert()
while True:
    try:
        GPIO.wait_for_edge(PIN_NO,GPIO.RISING)
        print("Intrusion Detected")
        sendAlert()
        sleep(5)
    except (KeyboardInterrupt, SystemExit, Exception):
        GPIO.cleanup()
        exit()


GPIO.cleanup()
