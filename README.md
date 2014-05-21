SR5002_API
==========

A Python API for network control of the Marantz SR5002 AV amp by its RS232C port

This API provides network control of the Marantz SR5002 via its RS232C port.
To use this API, run a Pyro name server on the machine which is RS232 connected to the
Marantz SR5002.  It is not essential to run the Pyro name server on the machine connected to the Marantz,
it could be run on any machine on the local network.  Where and how the Pyro name server is
run is covered in the Pyro documentation (Note to self: add details on this later).

Then set up an RS232 config file on the machine RS232C connected to the SR5002
and then start the RS232server.py.

To use the API from any local network connected machine call RS232_init first with a parameter 
of the config file name for the machine running the server (ie the one RS232C connected to
the SR5002.

To send a command to the SR5002 either send a sequence of commands, space separated, as a string
using SR5002_cmd or call each API function separately.

To be done
1 Add error handling
