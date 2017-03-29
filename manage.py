"""
Manage all database, tables and data
related maintainance work like creating
all tables, droping all tables, generating 
default data for demo purposes, clearing 
data from notification etc.
"""
#!/usr/bin/env python
import serv
import dbcon
import sys

## configuring connections
serv.app = dbcon.inject_db(serv.app)
serv.app.app_context().push()

if __name__ == '__main__':
    argument = sys.argv[1]
    try:
        if argument == "create":
            print "Creating All Tables"
            dbcon.createAll()
        elif argument == "drop":
            print "Dropping All Tables"
            dbcon.dropAll()
        elif argument == "recreate":
            print "Recreating All Tables"
            dbcon.dropAll()
            dbcon.createAll()
        print "Done."
    except Exception, e:
        print "Unsuccessful :: " + str(e)