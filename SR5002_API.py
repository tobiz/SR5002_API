#!/usr/bin/env python


#
# Copyright (C) 2014 P.J.Robinson
#
# SR5002_API is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This API provides network control of the Marantz SR5002 via its RS232C port.
# To use this API, run a Pyro name server on the machine which is RS232 connected to the
# Marantz SR5002.  It could be run on any machine on the local network
# Then set up an RS232 config file on the machine RS232C connected to the SR5002
# and then start the RS232server.py.
# To use the API from any local network connected machine call RS232_init first with a parameter 
# of the config file name for the machine running the server (ie the one RS232C connected to
# the SR5002.
# To send a command to the SR5002 either send a sequence of commands, space separated, as a string
# using SR5002_cmd or call each API function separately 

import time
import socket
import ConfigParser
import serial

# Global variables
# Default RS232C values

BAUDRATE = 9600
RTSCTS = 0
XONXOFF  = 0
RDTMOUT  = 0.5
WRITETIMEOUT = 0.5
WAIT = 0.3

class actionclass:
    def mul(self, arg1, arg2): return arg1 * arg2
    def add(self, arg1, arg2): return arg1 + arg2
    def sub(self, arg1, arg2): return arg1 - arg2
    def div(self, arg1, arg2): return arg1 / arg2  
    def hello(self):
        host_IP = ([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
        return "Hello from: " + host_IP
    
    def RS232_init(self, arg1):
        # This reads the config file supplied as a parameter arg1 and
        # uses the values to initialise the server
        CONFIG_FILE = arg1       
        try:
            open(CONFIG_FILE, 'r');
        except IOError :
            #Config file does not exist so use defaults
            #conf = "FALSE";
            print "Config file not found: " , CONFIG_FILE
            return False
        else:
            #Config file exist so use it
            print "Config file found " , CONFIG_FILE 
            config = ConfigParser.ConfigParser() ;
            config.read(CONFIG_FILE) ;
        
        self.usb_dev = config.get("Driver", "USBDEV") 
        if self.usb_dev == "" :
            print "ERROR: No usb device specified so exit" 
            return False
        else :
            print "USB device is: " + self.usb_dev 
            
        self.baudrate = config.get("Driver", "BAUDRATE") 
        if self.baudrate == "" :
            print "Baudrate not specified, use default : " , self.baudrate
            self.baudrate = BAUDRATE
        print "Baudrate is: ", self.baudrate
        
        self.rtscts = config.get("Driver", "RTSCTS") 
        if self.rtscts == "" :
            print "Rtscts not specified, use default : " , self.rtscts
            self.rtscts = RTSCTS
        print "Rtscts is: ", self.rtscts
        
        self.xonxoff = config.get("Driver", "XONXOFF") 
        if self.xonxoff == "" :
            print "xonxoff not specified, use default : " , self.xonxoff
            self.xonxoff = XONXOFF
        print "xonxoff is: ", self.xonxoff
        
        self.rdtmout = config.get("Driver", "RDTMOUT") 
        if self.rdtmout == "" :
            print "rdtmout not specified, use default : " , self.rdtmout
            self.rdtmout = RDTMOUT
        self.rdtmout = float(self.rdtmout)
        print "rdtmout is: ", self.rdtmout
        
        self.writeTimeout = config.get("Driver", "WRITETIMEOUT") 
        if self.writeTimeout == "" :
            print "WriteTimeout not specified, use default : " , self.writeTimeout
            self.writeTimeout = WRITETIMEOUT
        self.writeTimeout = float(self.writeTimeout)
        print "WriteTimeout is: ", self.writeTimeout
        
        self.wait_t = config.get("Driver", "WAIT") 
        if self.wait_t == "" :
            print "wait_t not specified, use default : " , self.wait_t
            self.wait_t = WAIT
        self.wait_t = float(self.wait_t)
        print "wait_t is: ", self.wait_t
        
        self.test_mode = config.get("Driver", "TEST")
        if self.test_mode == "yes":
            print "Running in test mode, don't use RS232 just print"
        else:
            self.test_mode == "no"
            print "Running in live mode, use RS232 port"
         
        # Finished initialising the RS232 driver
        return True
    
    def RS232_Driver(self, arg1):
        print "RS232_Driver called"
        if self.test_mode == "yes":
            print "RS232_Driver called in test mode"
            rtn = True
        else:    
            ser=serial.Serial(port=self.usb_dev, 
                              baudrate=self.baudrate, 
                              bytesize=8,
                              rtscts=self.rtscts,
                              xonxoff=self.xonxoff, 
                              timeout=self.rdtmout,
                              writeTimeout=self.writeTimeout,
                              )
            print "Open serial"
            ser.open() ;
            print 'Time before write' , time.time() ;
            rtn = ser.write(arg1);
            #print 'Time after write' , time.time() ;
            time.sleep(self.wait_t)   
            #print 'Before read' , time.time() ;
            #rd = ser.read(size=8) ;    
            #print 'After read' , time.time() ;
            print 'read rtn=' , rtn 
            ser.close()
        print "RS232_Driver exit"
        return rtn
    
    def SR5002_cmd(self, arg1): 
        # This function sends the supplied string parameter sequence to the
        # SR5002 via the RS232 port command by command
        # It returns ?? (the response code from the call?)
        # Open temporary file for reading.
        # File should have 1 line with all the SR5002 commands on it separated by space
        #sr5002cmd = SR5002CMD ;
        
        print "SR5002_cmd Called"
       
        print "USB port on this machine"
       
        print "Command string = " + arg1 
        params = arg1.split()
        nos_params = len(params)
        print "Params after split = " + str(params)
        print "Nos params = " + str(len(params))
    
        for i in range (0, nos_params): 
            cmd = '@' + params[i] + '\r'
            print 'Cmd=' + cmd    
            #print 'Before write' , time.time() ;
            #rtn = ser.write(cmd);
            #print 'After write' , time.time() ;
            #time.sleep(self.wait_t)   
            #print 'Before read' , time.time() ;
            #rd = ser.read(size=8) ;    
            #print 'After read' , time.time() ;
            #print 'rtn=' , rtn ;
            #print 'read rtn=' , rd ;
            self.RS232_Driver(cmd)
        
        #ser.close() 
        print "Exit SR5002_cmd"
        return True
 
    def SR5002_PWR_off (self):
        return self.SR5002_cmd("PWR:1")
    
    def SR5002_PWR_on (self):
        return self.SR5002_cmd("PWR:2")
    
    def SR5002_Audio_Toggle(self):
        return self.SR5002_cmd("AMT:0")
    
    def SR5002_Audio_Mute_off(self):
        return self.SR5002_cmd("AMT:1")
    
    def SR5002_Audio_Mute_on(self):
        return self.SR5002_cmd("AMT:2")
    
    def SR5002_Vol_up(self):
        return self.SR5002_cmd("VOL:1")
    
    def SR5002_Vol_down(self):
        return self.SR5002_cmd("VOL:2")
    
    def SR5002_Vol_Set(self, arg1):
        if arg1 > 18 :
            return False
        if arg1 < -99 :
            return False
        val = "VMT:0" + str(arg1)
        return self.SR5002_cmd(val)
    
    def SR5002_Bass_up(self):
        return self.SR5002_cmd("TOB:1")
    
    def SR5002_Bass_down(self):
        return self.SR5002_cmd("TOB:2")
    
    def SR5002_Treble_up(self):
        return self.SR5002_cmd("TOT:1")
    
    def SR5002_Treble_down(self):
        return self.SR5002_cmd("TOT:2") 
    
    def SR5002_SRC_TV(self):
        return self.SR5002_cmd("SRC:1")
    
    def SR5002_SRC_DVD(self):
        return self.SR5002_cmd("SRC:2")
    
    def SR5002_SRC_VCR1(self):
        return self.SR5002_cmd("SRC:3")
    
    def SR5002_SRC_VCR2(self):
        return self.SR5002_cmd("SRC:5")
    
    def SR5002_SRC_AUX1(self):
        return self.SR5002_cmd("SRC:9")
    
    def SR5002_SRC_AUX2(self):
        return self.SR5002_cmd("SRC:A")
    
    def SR5002_SRC_CD(self):
        return self.SR5002_cmd("SRC:C")
    
    def SR5002_HDMI_Audio_mode_enable(self):
        return self.SR5002_cmd("HAM:1")
    
    def SR5002_HDMI_Audio_mode_thru(self):
        return self.SR5002_cmd("HAM:2")
    
    def SR5002_7p1_Input_toggle(self):
        return self.SR5002_cmd("71C:0")
    
    def SR5002_7p1_Input_off(self):
        return self.SR5002_cmd("71C:1")
    
    def SR5002_7p1_Input_on(self):
        return self.SR5002_cmd("71C:2")
    
    def SR5002_SPK_SEL(self):
        return self.SR5002_cmd("SPK:0")
    
    def SR5002_SPK_A_off(self):
        return self.SR5002_cmd("SPK:1")
    
    def SR5002_SPK_A_on(self):
        return self.SR5002_cmd("SPK:2")
    
    def SR5002_SPK_B_off(self):
        return self.SR5002_cmd("SPK:3")
    
    def SR5002_SPK_B_on(self):
        return self.SR5002_cmd("SPK:4")
    
    
    
    
    
