#!/usr/bin/env python
# IMPORTS
import socket

num=0
## SAMPLE CLIENT PROGRAM
def connectNow(i):
    s = socket.socket()
    host = '127.0.0.1'
    port = 8787
    s.connect((host,port))
    msg = " ".join(['DATA PACKET',str(i)])
    s.send(msg)
    s.close
#
### RECEIVE DATA
#print s.recv(1024)
#s.close()

## CREATE CLASS OF CLIENT 
## TO MAKE INTEGRATION WITH
## RASPBERRY PI GPIO PINS 
## MORE MANAGEABLE
if __name__ == "__main__":
    try:
        while True:
            x = raw_input("Connect with server ? (y/n) ")
            if x.lower().strip() == 'y':
                num+=1
                connectNow(num)
    except KeyboardInterrupt:
        print "\nTerminating Client"