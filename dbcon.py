from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pytz import timezone
import hashlib

db = SQLAlchemy()
SECRET_KEY = "Prajyot Prabhat Ranvijay"

## DB TABLES
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r with email %r>' % (self.username, self.email)


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(300))
    device_unique_key = db.Column(db.String(100))
    last_checked = db.Column(db.String(50)) # timestamp

    def __init__(self, name, description, device_unique_key, last_checked):
        self.name = name
        self.description = description
        self.device_unique_key = device_unique_key
        self.last_checked = last_checked

    def __repr__(self):
        return '<Vehical %r described as %r>' % (self.name, self.description)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #type = db.Column(db.String(100)) # holding
    #message = db.Column(db.String(100))
    deviceid = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    timestamp = db.Column(db.String(140))
    useraction = db.Column(db.String(20))
    status = db.Column(db.String(20))  # records action taken by RaspberryPi

    def __init__(self, deviceid):
        self.deviceid = deviceid
        self.status = "WAITING"
        self.timestamp = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')  # sets timestamp according to IST
        self.useraction = "NONE"

    def __repr__(self):
        return "<Notification id %r for %r at %r>" % (self.id, self.deviceid, self.timestamp)


class UserDeviceMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    deviceid = db.Column(db.Integer, db.ForeignKey('vehicle.id'))

    def __init__(self, userid, deviceid):
        self.userid = userid
        self.deviceid = deviceid


## DB METHODS
def regUser(name, email, password1, password2):
    """
    Check all conditions for valid password
    and create sha224 hash sum of password
    and check if invalid characters are present
    in all fields
    """
    user = None
    if (name.find("'") < 0 and name.find('"') < 0 and email.find("'") < 0 and email.find('"') < 0 and password1.find(
        "'") < 0 and password1.find('"') < 0 and password2.find("'") < 0 and password2.find('"') < 0):
        if(password1 == password2 and password1 != None and password1 != ""):
            password = hashlib.sha224(password1).hexdigest()
            user = User(name, email, password)
            try:
                db.session.add(user)
            except Exception, e:
                db.session.rollback()
                print(str(e))
                return False
            db.session.commit()
            return True
        else:
            return False
    else:
        return False

def getVehicle(email):
    # query = "select * from vehicle where id in (select deviceid from user_device_map where userid in (select id from public.user where email='%s'))" % email
    # try:
    #     result = db.engine.execute(query).fetchall()
    # except Exception, e:
    #     print str(e)
    #     db.session.rollback()
    # resObj = {}
    # if len(result) == 1:
    #     resObj["name"] = result[0][1]
    #     resObj["description"] = result[0][2]
    # return resObj
    return ""

def regVehicle(name, description, device_unique_key, last_checked, user_name):
    """
    Register device and map user accordingly.
    """
    query = "select * from vehicle where device_unique_key='%s' " % device_unique_key
    vehicle = Vehicle(name, description, device_unique_key, last_checked)
    user = User.query.filter_by(email=user_name).all()
    if(len(db.engine.execute(query).fetchall())<=0 and len(user) == 1):
        # register vehicle and map user in following user table
        try:
            user = user[0]
            try:
                db.session.add(vehicle)
            except Exception, e:
                db.session.rollback()
                print str(e)
                return False
            db.session.commit()
            udmap = UserDeviceMap(user.id, vehicle.id)
            db.session.add(udmap)
            db.session.commit()
            return True
        except Exception, e:
            print "ERROR OCCURED :: %s" % str(e)
            return False
    else:
        # throw error that the device already exists in db
        return False

def login(uname, paswd):
    paswd = hashlib.sha224(paswd).hexdigest()
    result = User.query.filter_by(email=uname, password=paswd).first()
    if result == None:
        return False
    else:
        return True

def generateKey(username):
    toDigest = SECRET_KEY + username + datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S')
    hexDigest = hashlib.sha224(toDigest).hexdigest()
    return hexDigest

def notify(deviceid):
    vehicle = Vehicle.query.filter_by(device_unique_key=deviceid).first()
    notification = Notification(vehicle.id)
    try:
        try:
            db.session.add(notification)
        except Exception, e:
            db.session.rollback()
            print str(e)
            return False
        db.session.commit()
        return notification
    except Exception, e:
        print str(e)
        return False

def getnotificationbyid(id):
    print type(id)
    resp = Notification.query.filter_by(id=id).first()
    if resp != None:
        return resp
    else:
        return False

def updatedeviceaction(id, action):
    query = "update notification set status='%s' where id='%s'" % (action, id)
    try:
        db.engine.execute(query)
        return True
    except Exception, e:
        db.session.rollback()
        print str(e)
        return False

def updateuseraction(id, action):
    query = "update notification set useraction='%s' where id='%s'" % (action, id)
    try:
        db.engine.execute(query)
        return True
    except Exception, e:
        db.session.rollback()
        print str(e)
        return False


def getallnotifiactions(email):
    # query = """select * from notification where deviceid in (select deviceid from user_device_map where userid in (select id from public.user where email='%s')) order by timestamp desc""" % email
    # result = db.engine.execute(query).fetchall()
    # resp = []
    # for x in result:
    #     resp.append({"id": x[0], "deviceid": x[1], "timestamp": x[2], "useraction": x[3], "status": x[4]})
    # if len(resp) > 0:
    #     return resp
    # else:
    #     return False
    return ""

## table management
def createAll():
    db.create_all()

def dropAll():
    db.drop_all()

## Injects db connection inside of flask app
def inject_db(app):
    """
        Injects database inside flask app.
    """
    db.init_app(app)
    return app
