#!/usr/bin/env python
## Final server file

import os
from flask import Flask, send_from_directory, request
import dbcon

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

INVALID_REQUEST = "<h1 style='color:red; text-align:center;>Invalid Request</h1>"
SUCCESS_MESSAGE = "<h1>SUCCESSFULL</h1>"
FAILURE_MESSAGE = "<h1>FAILED</h1>"

## serve website
@app.route("/")
def getIndex():
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
                return SUCCESS_MESSAGE
            else:
                return FAILURE_MESSAGE
        except Exception, e:
            print "EXCEPTION AT: serv.py > regUser() > if"
            print str(e)
            return FAILURE_MESSAGE
    else:
        return INVALID_REQUEST


@app.route("/login", methods=['POST'])
def checkLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if dbcon.login(username, password):
            return SUCCESS_MESSAGE
        else:
            return FAILURE_MESSAGE
    else:
        return INVALID_REQUEST


## MAIN METHOD
if __name__ == "__main__":
    # dbManager = servPkg.DbManager(app)
    app = dbcon.inject_db(app)
    app.app_context().push()
    PORTNO = int(os.environ.get("PORT", 2121))
    print "Initiating server on port " + str(PORTNO)
    app.run(host='0.0.0.0', port=PORTNO)  # remove debug before deploying
