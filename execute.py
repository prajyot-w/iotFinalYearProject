#!/usr/bin/env python

# import RPi.GPIO as GPIO
import requests
from time import sleep

count = 0
PIN_NO = 37
DEVICE_ID = "MER123"
SERVER_URL = "http://carsecure.herokuapp.com/"

# GPIO setup ...................................
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(PIN_NO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def block_car(notification_id):
    # send block status
    print "DENYING ACCESS"
    resp = requests.post(SERVER_URL+"api/updatedeviceaction", data={"id": notification_id, "action": "BLOCK"})
    # GPIO BLOCKING CODE
    print resp.json()
    return

def allow_car(notification_id):
    # send allow status
    print "ALLOWING ACCESS"
    resp = requests.post(SERVER_URL + "api/updatedeviceaction", data={"id": notification_id, "action": "ALLOW"})
    # GPIO ALLOWING CODE
    print resp.json()
    return

def waitNact(id):
    # wait n act accordingly
    print "WATCHING"
    for x in range(5):
        sleep(5)
        resp = requests.post(SERVER_URL+"api/getnotificationbyid", data={"id": id})
        if resp.status_code == 200:
            resp = resp.json()
            if resp["status"] == "success" and resp["useraction"] != "NONE":
                if resp["useraction"] == "ALLOW":
                    allow_car(id)
                    return
                elif resp["useraction"] == "BLOCK":
                    block_car(id)
                    return
    block_car(id)

def sendAlert():
    print "SENDING ALERT"
    resp = requests.post(SERVER_URL+"api/notify", data={"deviceid": DEVICE_ID}).json()
    if resp["status"] == "success":
        print "Notified to user successfully"
        id = resp["id"]
        waitNact(id)
    else:
        ## Block the car
        print "Blocking car"

if __name__ == "__main__":
    sendAlert() # for testing
    # while True:
    #     try:
    #         GPIO.wait_for_edge(PIN_NO,GPIO.RISING)
    #         print("Intrusion Detected")
    #         sendAlert()
    #         sleep(5)
    #     except (KeyboardInterrupt, SystemExit, Exception):
    #         GPIO.cleanup()
    #         exit()


# GPIO.cleanup()
