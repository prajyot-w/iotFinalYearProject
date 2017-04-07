#!/usr/bin/env python

import urllib
from urllib2 import *
import json
import sys

## SERVER API KEY
MY_API_KEY = "AAAAdL_qwcI:APA91bE71l5R9Gb5jR74cA7jPv4AnT4NgW7Lgd3UVYavBN4iq69qvzEByOnk3oMnbvgx-GR0Ym8ts4_WSdJkCm_mx67nkjs4cUupwWOC4hJ7qQrLkEzsZ8O_HpkA7SgrM4Kc8TtHpAT1"
header = {
    "Authorization": "key=" + MY_API_KEY,
    "Content-type": "application/json"
}

if __name__ == "__main__":
    messageTitle = sys.argv[1]
    messageBody = sys.argv[2]
    data = {
        "to": sys.argv[3],  # put key over here
        "notification": {
            "body": messageBody,
            "title": messageTitle,
            "icon": "ic_cloud_white_48dp"
        }
    }
    dataAsJson = json.dumps(data)
    request = Request("https://fcm.googleapis.com/fcm/send", dataAsJson, header)
    print urlopen(request).read()
