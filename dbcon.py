from flask_sqlalchemy import SQLAlchemy
import hashlib

db = SQLAlchemy()

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
        if(password1 == password2):
            password = hashlib.sha224(password1).hexdigest()
            user = User(name, email, password)
            db.session.add(user)
            db.session.commit()
            return True
        else:
            return False
    else:
        return False

def login(uname, paswd):
    paswd = hashlib.sha224(paswd).hexdigest()
    result = User.query.filter_by(email=uname, password=paswd).first()
    if result == None:
        return False
    else:
        return True

def createAll():
    db.create_all()

## Injects db connection inside of flask app
def inject_db(app):
    """
        Injects database inside flask app.
    """
    db.init_app(app)
    return app
