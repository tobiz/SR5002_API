#!/usr/bin/env python


import Pyro.naming
import Pyro.core
from Pyro.errors import PyroError, NamingError
import socket


#import RS232mod
import SR5002_API

###### testclass Pyro object

class actionclass(Pyro.core.ObjBase, SR5002_API.actionclass):
        pass
    

######
###### main server program
######
def main():
    # Find the Host IP address and bind to that.  If you don't do this it binds to 127.0.0.1. Note there are limitations on this, 
    # eg only works on local lan, doesn't support IPv6 addresses, but for now seems ok
    host_IP = ([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
    print "Host IP is: " + host_IP
    Pyro.config.PYRO_HOST = host_IP
    
    # Start of original example code

    Pyro.core.initServer()
    daemon = Pyro.core.Daemon()
    # locate the NS
    locator = Pyro.naming.NameServerLocator()
    print 'searching for Name Server...'
    ns = locator.getNS()
    daemon.useNameServer(ns)

    # connect a new object implementation (first unregister previous one)
    try:
        # 'RS232' is the name by which our object will be known to the outside world
       #ns.unregister('RS232')
        ns.unregister('SR5002')
    except NamingError:
        pass
            
    # connect new object implementation
    
    #daemon.connect(actionclass(), 'RS232')
    daemon.connect(actionclass(), 'SR5002')
    
    # enter the server loop.
    #print 'Server object "RS232" ready.', "on host: " + host_IP
    print 'Server object "SR5002" ready.', "on host: " + host_IP

    daemon.requestLoop()

if __name__ == "__main__":
        main()
