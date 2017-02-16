#!/usr/bin/env python


from bottle import *

@error(404)
def error404(error):
    return "<style>*{margin:0;padding:0}</style><div style='display:flex;height: 98%;'><span style='margin: auto auto; font-size: 30px; font-weight: 700;'>Nothing Here. Sorry !</span></div>"

@route("/")
def getIndex():
    return getElements("index.html")

@route("/www/<path:path>")
def getElements(path):
    print path
    return static_file(path, root="./www/")

@route("/hello/<name>")
def index(name):
    return template('<b>Hello {{name}}</b>', name=name)

@route("/test")
def header():
    return "<h1>Test Text</h1>"

run(host='localhost', port=3001, debug=True)
