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
"""
import sqlite3

class Database:
    """
    DATABASE DOC
    """

    def __init__(self): # connect to database
        self.conn = sqlite3.Connection("../db.sqlite")

    def __del__(self):  # close connection
        self.conn.close()

    ## method to create all tables
    def createAllTables(self):
        userTable = """
            CREATE TABLE user (
                id int primary key,
                name varchar(50) not null,
                phone_no varchar(13) not null,
                email varchar(50) not null,
                password varchar(60) not null
            )
        """

        deviceTable = """
            CREATE TABLE device (
                id int primary key,
                type varchar(10) not null,
                device_unique_key varchar(50) not null
            )
        """

        mapTable = """
            CREATE TABLE map (
                userId int not null,
                deviceId int not null,
                FOREIGN KEY (userId) REFERENCES user(id),
                FOREIGN KEY (deviceId) REFERENCES device(id)
            )
        """
        queryList = (userTable, deviceTable, mapTable)
        for query in queryList:
            try:
                self.conn.execute(query)
            except Exception:
                print "Error occured while executing following query :: " + query




if __name__ == "__main__":
    db = Database()
    db.createAllTables()
