#!/usr/bin/env python


import Pyro.naming, Pyro.core
from Pyro.errors import NamingError

import SR5002_API

# locate the NS
locator = Pyro.naming.NameServerLocator()
print 'Searching Name Server...',
ns = locator.getNS()

# resolve the Pyro object
print 'finding object'
try:
        URI = ns.resolve('SR5002')
        print 'URI:', URI
except NamingError, x:
        print 'Couldn\'t find object, nameserver says:', x
        raise SystemExit

# create a proxy for the Pyro object, and return that
SR5002 = Pyro.core.getProxyForURI(URI)

#print SR5002.mul(111, 9)
#print SR5002.add(100, 222)
#print SR5002.sub(222, 100)
#print SR5002.div(2.0, 9.0)
#print SR5002.mul('*', 10)
#print SR5002.add('String1', 'String2')
print SR5002.hello()
print SR5002.RS232_init("/home/pi/workspace/SR5002_API/src/SR5002_RS232.conf")
#print SR5002.SR5002_cmd("ABC DEF GHI")
#print SR5002.SR5002_PWR_off()
#print SR5002.SR5002_PWR_Stat()
#print SR5002.SR5002_PWR_on()
#print SR5002.SR5002_PWR_Stat()
#print SR5002.SR5002_PWR_off()
#print SR5002.SR5002_PWR_Stat()
#print SR5002.SR5002_Audio_Toggle()
#print SR5002.SR5002_Audio_Mute_off()
#print SR5002.SR5002_Audio_Mute_on()
#print SR5002.SR5002_Vol_up()
#print SR5002.SR5002_Vol_down()
#print SR5002.SR5002_Vol_Set(10)
#print SR5002.SR5002_Surr_Mode(SURR_MODE_CSII_MUSIC) 
#
# Test status commands
#
#print SR5002.SR5002_PWR_Stat()
#print SR5002.SR5002_HDMI_Mode()
#print SR5002.SR5002_SRC_Slct() # Can't run in test mode as RS232 has to return value
#print SR5002.SR5002_cmd("@SLP:1")



print SR5002.SR5002_SRC_TV()
print SR5002.SR5002_SRC_DVD()

