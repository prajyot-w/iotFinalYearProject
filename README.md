## DEVELOPMENT DOC

* Create a server that reads for multiple connections
* This can be achieved by creating a class.
* In that class there will be a method that listens for
connections constantly.
* That can be implemented using thread programming.
* Maintain an list of dictionaries that holds details
for each connection and mapping of each connection to
its counterpart. I.E. phone and car mapping.
* While the independent thread keep listening for new
connections, other methods are provided to make server
do other stuffs.
* Only listening for new connections will be implemented
inside new thread.
* The 'Main' block of server code will handle everything
related to creating server, listening for connection,
mapping devices, forwarding messages etc.
* Handle Keyboard Interrupts.
* Pass data using Json Objects for communication
* Use bottle module for server


## PROGRESS

* Server accepting multiple connections, and also storing
them in a secure array.
* Server also quitting appropriately