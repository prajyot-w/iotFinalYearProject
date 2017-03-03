#!/usr/bin/env python

import RPi.GPIO as GPIO
import requests
from time import sleep

count=0
PIN_NO=37 

def sendAlert():
    p.pushMessage(CHANNEL_NAME,MESSAGE)
    return

# GPIO setup ...................................
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN_NO, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

if __name__ == "__main__":
    print "Hello"
else:
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
