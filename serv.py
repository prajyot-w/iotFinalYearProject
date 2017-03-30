#!/usr/bin/env python
## Final server file

import os
from flask import Flask, send_from_directory, request, session, make_response, redirect, url_for
import dbcon

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = "prajyot"

INVALID_REQUEST = "<h1 style='color:red; text-align:center;>Invalid Request</h1>"
SUCCESS_MESSAGE = "<h1>SUCCESSFULL</h1>"
FAILURE_MESSAGE = "<h1>FAILED</h1>"


def checkCreds(username, key):
    if username != None and username != "" and key != None and key != "" and session[username] == key:
        return True
    return False

## serve website
@app.route("/")
def getIndex():
    try:
        username = request.cookies.get("username")
        key = request.cookies.get("key")
        if checkCreds(username, key):
            return send_from_directory("www", "home.html")
        else:
            return send_from_directory("www", "index.html")
    except Exception:
        return send_from_directory("www", "index.html")


@app.route("/<path:path>")
def getFiles(path):
    return send_from_directory("www", path)

## create all db tables
@app.route("/createall")
def createAll():
    try:
        dbcon.createAll()
        return "Successful"
    except Exception:
        return "Failed"

## serve general services
@app.route("/reguser", methods=['POST'])
def regUser():
    if request.method == 'POST':
        try:
            if dbcon.regUser(request.form["name"], request.form["email"], request.form["password1"], request.form["password2"]):
                resp = make_response(SUCCESS_MESSAGE + "<script>window.location='registervehicle.html';</script>")
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
    if request.method == 'POST':
        name = request.form["name"]
        description = request.form["description"]
        deviceid = request.form['deviceid']
        lastchecked = "N/A"
        useremail = request.cookies.get("email")
        try:
            if dbcon.regVehicle(name, description, deviceid, lastchecked, useremail):
                resp = make_response(SUCCESS_MESSAGE + "<script>setTimeout(function(){window.location='index.html'}, 3000);</script>")
                resp.set_cookie("email", "", expires=0)
                return resp
            else:
                return FAILURE_MESSAGE
        except Exception, e:
            print "EXCEPTION :: " + str(e)
            return FAILURE_MESSAGE

@app.route("/logout", methods=['GET'])
def logout():
    username = request.cookies.get('username')
    session.pop(username, None)
    resp = make_response("logout")
    resp.set_cookie("username", "", expires=0)
    resp.set_cookie("key", "", expires=0)
    return resp

@app.route("/login", methods=['GET', 'POST'])
def checkLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if dbcon.login(username, password):
            key = dbcon.generateKey(username)
            resp = make_response(SUCCESS_MESSAGE + "<script>window.location='home.html'</script>")
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
                return SUCCESS_MESSAGE
        except Exception:
            return FAILURE_MESSAGE
        return INVALID_REQUEST


## MAIN METHOD
if __name__ == "__main__":
    # dbManager = servPkg.DbManager(app)
    app = dbcon.inject_db(app)
    app.app_context().push()
    PORTNO = int(os.environ.get("PORT", 2121))
    print "Initiating server on port " + str(PORTNO)
    app.run(host='0.0.0.0', port=PORTNO)  # remove debug before deploying
