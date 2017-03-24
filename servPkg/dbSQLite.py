"""
Trying to connect sqlite v3 database.
==================================================
* sqlite3 library is available by default in system as
  you install python version 2.5.* and above
* This makes it easy to integrate with any project.
* always run conn.commit() after insertion or updation
  to make db save the changes into file.
* Use hashlib library for password encryption and use
  ssh224 method in that library to calculate hash
* By default a rowid column is present in every table
  no need to take an id column explicitly.
"""
import sqlite3
import hashlib

class Database:
    """
    DATABASE DOC
    """

    def __init__(self): # connect to database
        self.conn = sqlite3.Connection("../db.sqlite")

    def __del__(self):  # close connection
        self.conn.close()

    def setNotification(self):
        pass

    def getNotification(self):
        pass

    def registerVehical(self, name, description, deviceUniqueKey):
        query = "INSERT INTO VEHICAL (name, vehical, device_unique_key) values ('"+name+"','"+description+"','"+deviceUniqueKey+"')"
        print query
        self.conn.execute(query)
        self.conn.commit()

    def registerUser(self, name, phoneno, email, userPassword):
        passHash = hashlib.sha224(userPassword)
        query = "INSERT INTO USER (name, phone_no, email, password, cookie) values ('"+name+"','"+phoneno+"','"+email+"','"+passHash.hexdigest()+"','') "
        self.conn.execute(query)
        self.conn.commit()

    ## method to create all tables
    def createAllTables(self):
        """USE ONCE TO CREATE DB"""
        userTable = """
            CREATE TABLE user (
                name varchar(50) not null,
                phone_no varchar(13) not null,
                email varchar(50) not null,
                password varchar(60) not null,
                cookie varchar(250)
            )
        """

        vehicalTable = """
            CREATE TABLE vehical (
                name varchar(60) null,
                description varchar(250),
                device_unique_key varchar(50) not null
            )
        """

        mapTable = """
            CREATE TABLE map (
                userId int not null,
                deviceId int not null,
                FOREIGN KEY (userId) REFERENCES user(rowid),
                FOREIGN KEY (deviceId) REFERENCES vehical(rowid)
            )
        """

        notifications = """
            CREATE TABLE notification (
                id int not null,
                type varchar(250),
                message varchar(250),
                status varchar(20),
                timestamp varchar(50),
                action varchar(20),
                FOREIGN KEY (id) REFERENCES vehical(rowid)
            )
        """
        queryList = (userTable, vehicalTable, mapTable, notifications)
        for query in queryList:
            try:
                self.conn.execute(query)
            except Exception:
                print "Error occured while executing following query :: " + query




if __name__ == "__main__":
    db = Database()
    # db.createAllTables()
    db.registerUser("Prajyot", "9867448922", "prajyotwalali.21@gmail.com", "prajyot")
