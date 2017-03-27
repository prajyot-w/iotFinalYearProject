#!/usr/bin/env python
## Final server file

# IMPORTS
import gevent.monkey; gevent.monkey.patch_all()
from bottle import Bottle, run, static_file, request
import os
#import servPkg

app = Bottle()
ERROR_MSG = """
            <style>*{margin:0;padding:0}</style>
            <div style='display:flex;height: 98%;'>
                <span style='margin: auto auto; font-size: 30px; font-weight: 700;'>
                    Nothing Here. Sorry !
                </span>
            </div>
            """

### Server/REST Methods
## GERERAL ERROR MSG
@app.error(404)
def error404(error):
    return ERROR_MSG

## serve website
@app.route("/www/<path:path>")
def getFiles(path):
    return static_file(path, root="./www/")

@app.route("/")
def getIndex():
    return getFiles("index.html")

## serve other services
@app.post("/login")
def login():
    username = request.forms.get("username")
    password = request.forms.get("password")
    if username=='prajyot' and password=='walali':
        return "<div style='text-align:center; font-size: 30px; font-weight: 700;'>You have been successfully loged in !!</div>"
    else:
        return "<div style='text-align:center; font-size: 30px; font-weight: 700; color:red;'>Invalid Credentials</div>"

## serve rest services here
## use `/restapi` as root for all rest services

#  MAIN
print "LOG MESSAGE BEFORE MAIN"
if __name__ == "__main__":
    print "Instantiating server ... "
    run(app, server='gevent' ,port=os.environ.get('PORT',5000), debug=True, reloader=True)

