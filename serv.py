#!/usr/bin/env python
## Final server file

import os
from flask import Flask, send_from_directory, request, session, make_response
from flask_cors import CORS
import dbcon
import json

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://cifhxzeverqgqq:d4f3d95a2ff0f1edd730ea8c5d34895cb2e81b2248c89298f938824249cb435b@ec2-107-20-141-145.compute-1.amazonaws.com:5432/d6lrmj3d48nngg'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = "prajyot"

INVALID_REQUEST = """
    <link href="https://fonts.googleapis.com/css?family=Nunito" rel="stylesheet">
    <style>
    body{
    display: flex; 
    color: palevioletred;
    font-family: 'Nunito', sans-serif;
    }
    body>*{margin: auto auto;}
    </style>
    <h1>Invalid Request</h1>
    <script>
    setTimeout(function(){window.location="/";},2000);
    </script>
"""
FAILURE_MESSAGE = """
    <link href="https://fonts.googleapis.com/css?family=Nunito" rel="stylesheet">
    <style>
    body{
    display: flex; 
    color: #999;
    font-family: 'Nunito', sans-serif;
    }
    body>*{margin: auto auto;}
    </style>
    <h1>Failed</h1>
    <script>
    setTimeout(function(){window.location="/";},2000);
    </script>
"""


def checkCreds(username, key):
    if username != None and username != "" and key != None and key != "" and session[username] == key:
        return True
    return False

## serve website
@app.route("/")
def getIndex():
    return send_from_directory("www", "index.html")


@app.route("/<path:path>")
def getFiles(path):
    return send_from_directory("www", path)


## api services
@app.route("/api/getvehicle", methods=['GET'])
def getVehicle():
    email = request.cookies.get("username")
    key = request.cookies.get("key")
    if checkCreds(email, key):
        resp = dbcon.getVehicle(email)
        if resp == {}:
            resp["status"] = "failed"
        else:
            resp["status"] = "success"
    else:
        resp = {"status": "failed"}
    resp = json.dumps(resp)
    return resp

@app.route("/api/notify", methods=["POST"])
def notify():
    resp = {}
    deviceid = request.form.get("deviceid")
    respObj = dbcon.notify(deviceid)
    if respObj:
        resp["status"] = "success"
        resp["id"] = respObj.id
    else:
        resp["status"] = "failed"
    resp = json.dumps(resp)
    return resp

@app.route("/api/getnotificationbyid", methods=["POST"])
def getnotificationbyid():
    id = request.form.get("id")
    resp = {}
    respObj = dbcon.getnotificationbyid(id)
    if respObj:
        resp["status"] = "success"
        resp["id"] = respObj.id
        resp["useraction"] = respObj.useraction
    else:
        resp["status"] = "failed"
    resp = json.dumps(resp)
    return resp

@app.route("/api/updatedeviceaction", methods=["POST"])
def updatedeviceaction():
    ## ONLY ACCEPTS 'BLOCK' OR 'ALLOW'
    resp = {}
    id =request.form.get("id")
    action = request.form.get("action")
    if dbcon.updatedeviceaction(id, action):
        resp["status"] = "success"
    else:
        resp["status"] = "failed"
    resp = json.dumps(resp)
    return resp

@app.route("/api/getallnotifications", methods=["POST", "GET"])
def getallnotifications():
    email = request.cookies.get("username")
    key = request.cookies.get("key")
    resp = {}
    if checkCreds(email, key):
        respObj = dbcon.getallnotifiactions(email)
        if respObj != False:
            resp["status"] = "success"
            resp["data"] = respObj
        else:
            resp["status"] = "failed"
    else:
        resp["status"] = "failed"
    resp = json.dumps(resp)
    return resp

## serve general services
@app.route("/reguser", methods=['POST'])
def regUser():
    if request.method == 'POST':
        try:
            if dbcon.regUser(request.form["name"], request.form["email"], request.form["password1"], request.form["password2"]):
                resp = make_response("<script>window.location='registervehicle.html';</script>")
                resp.set_cookie("email", request.form["email"])
                return resp
            else:
                return FAILURE_MESSAGE
        except Exception, e:
            print "EXCEPTION AT: serv.py > regUser() > if"
            print str(e)
            return FAILURE_MESSAGE
    else:
        return INVALID_REQUEST

@app.route("/regvehicle", methods=['POST'])
def regVehicle():
    FINAL_SUCCESS_MESSAGE = """
    <link href="https://fonts.googleapis.com/css?family=Nunito" rel="stylesheet">
    <style>
    body{
    display: flex; 
    color: #999;
    font-family: 'Nunito', sans-serif;
    }
    body>*{margin: auto auto;}
    </style>
    <h1>Registration process completed successfully.</h1>
    <script>
    setTimeout(function(){window.location="/";},2000);
    </script>
    """
    if request.method == 'POST':
        name = request.form["name"]
        description = request.form["description"]
        deviceid = request.form['deviceid']
        lastchecked = "N/A"
        useremail = request.cookies.get("email")
        try:
            if dbcon.regVehicle(name, description, deviceid, lastchecked, useremail):
                resp = make_response(FINAL_SUCCESS_MESSAGE + "<script>setTimeout(function(){window.location='index.html'}, 3000);</script>")
                resp.set_cookie("email", "", expires=0)
                return resp
            else:
                return FAILURE_MESSAGE
        except Exception, e:
            print "EXCEPTION :: " + str(e)
            return FAILURE_MESSAGE

@app.route("/logout", methods=['GET'])
def logout():
    LOG_OUT_MESSAGE = """
    <link href="https://fonts.googleapis.com/css?family=Nunito" rel="stylesheet">
    <style>
    body{
    display: flex; 
    color: #999;
    font-family: 'Nunito', sans-serif;
    }
    body>*{margin: auto auto;}
    </style>
    <h1>You have been successfully logged out.</h1>
    <script>
    setTimeout(function(){window.location="/";},2000);
    </script>
    """
    username = request.cookies.get('username')
    session.pop(username, None)
    resp = make_response(LOG_OUT_MESSAGE)
    resp.set_cookie("username", "", expires=0)
    resp.set_cookie("key", "", expires=0)
    return resp

@app.route("/checkcreds", methods=['GET'])
def chkCreds():
    resp = {"status" : "unknown"}
    if checkCreds(request.cookies.get("username"), request.cookies.get("key")):
        resp["status"] = "success"
    else:
        resp["status"] = "failed"
    resp = make_response(json.dumps(resp))
    return resp

@app.route("/login", methods=['GET', 'POST'])
def checkLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if dbcon.login(username, password):
            key = dbcon.generateKey(username)
            resp = make_response("<script>window.location='home.html'</script>")
            resp.set_cookie("username", username)
            resp.set_cookie("key", key)
            session[username] = key
            return resp
        else:
            return FAILURE_MESSAGE
    else:
        try:
            username = request.cookies.get("username")
            key = request.cookies.get("key")
            if checkCreds(username, key):
                return "<script>window.location='home.html'</script>"
        except Exception:
            return FAILURE_MESSAGE
        return INVALID_REQUEST


## MAIN METHOD
if __name__ == "__main__":
    app = dbcon.inject_db(app)
    app.app_context().push()
    PORTNO = int(os.environ.get("PORT", 2121))
    print "Initiating server on port " + str(PORTNO)
    app.run(host='0.0.0.0', port=PORTNO)  # remove debug before deploying
