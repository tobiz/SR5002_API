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
import re
from subprocess import call
import os
import string

# Global variables

# Default RS232C values

BAUDRATE = 9600
RTSCTS = 0
XONXOFF  = 0
RDTMOUT  = 0.5
WRITETIMEOUT = 0.5
WAIT = 0.3

# SR5002 API defined values
ACK = 0x06
NAK = 0x15

#Global name
hdmi_port= ["", "", "", ""]
keybd = ""
mouse = ""

SURR_MODE_AUTO              = "SUR:00"
SURR_MODE_STEREO            = "SUR:01"
SURR_MODE_DOLBY             = "SUR:02"
SURR_MODE_PL2xMOVIE         = "SUR:03"
SURR_MODE_PL2MOVIE          = "SUR:04"
SURR_MODE_PL2xMUSIC         = "SUR:5"
SURR_MODE_PL2MUSIC          = "SUR:06"
SURR_MODE_PL2xGAME          = "SUR:07"
SURR_MODE_PL2GAME           = "SUR:08"
SURR_MODE_DOLBY_PROLOGIC    = "SUR:09"
SURR_MODE_EX_ES             = "SUR:0A"
SURR_MODE_VIRTUAL61         = "SUR:0B"
SURR_MODE_DTS_ES            = "SUR:0E"
SURR_MODE_NEO6_CINEMA       = "SUR:0F"
SURR_MODE_NEO6_MUSIC        = "SUR:0G"
SURR_MODE_MULTI_CHN_STEREO  = "SUR:0H"
SURR_MODE_CSII_CINEMA       = "SUR:0I"
SURR_MODE_CSII_MUSIC        = "SUR:0J"
SURR_MODE_CSII_MONO         = "SUR:0K"
SURR_MODE_VIRTUAL           = "SUR:0L"
SURR_MODE_DTS               = "SUR:0M"
SURR_MODE_DDPLUS_PL2x_MOVIE = "SUR:0O"
SURR_MODE_DDPLUS_PL2x_MUSIC = "SUR:0P"
SURR_MODE_SOURCE_DIRECT     = "SUR:0T"
SURR_MODE_PURE_DIRECT       = "SUR:0U"
SURR_MODE_NEXT              = "SUR:1"
SURR_MODE_PREV              = "SUR:2"




class actionclass:
    # The following are a few test functions
    def mul(self, arg1, arg2): return arg1 * arg2
    def add(self, arg1, arg2): return arg1 + arg2
    def sub(self, arg1, arg2): return arg1 - arg2
    def div(self, arg1, arg2): return arg1 / arg2  
    def hello(self):
        host_IP = ([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
        return "Hello from: " + host_IP
    
    def find_dev(self, arg1):
        print "find_dev called"  
        for self.item in os.listdir("/dev/input/by-path"):
            if self.item.find(arg1) > -1:
                print "Exit find_dev value returned is: ", self.item
                return self.item
        print "Exit find_dev return False"
        return False
    
    def RS232_init(self, arg1):
        # This reads the config file supplied as a parameter arg1 and
        # uses the values to initialise the server
        
        
                
        CONFIG_FILE = arg1       
        try:
            open(CONFIG_FILE, 'r');
        except IOError :
            #Config file does not exist so use defaults
            #conf = "FALSE";
            print "Config file not found, use defaults: " , CONFIG_FILE
            #return False
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
        
        print "End of RS232 Device Section"
        # Section handling keyboard/mouse mapping to HDMI port
        # screen output connections.  This needs a change in SR5002_SRC_x
        # to switch keyboard & mouse input to the corresponding IP address,
        # ie the server connected to the HDMI port
        
        print "Start Keyboard and Mouse config"
        self.x = 0   
        for self.i in [0, 1, 2]:
            self.x = self.x + 1 
            print "i is: ", self.i
            print "x is: ", self.x
            hdmi_port[self.x] = config.get("Keyboard", "HDMI" + str(self.x))
            if hdmi_port[self.x] == "":
                print "No IP defined for HDMI port: ", self.x
            else:
                print "HDMI port : ", str(self.x), "connected to IP: ", hdmi_port[self.x]
                            
        
        global keybd_dev 
        keybd_dev = self.find_dev("event-kbd")
        if not keybd_dev:
            print "Keyboard event device not found"
            return False
        print "Keyboard dev is: ", keybd_dev
             
        global mouse_dev 
        mouse_dev = self.find_dev("event-mouse")
        if not keybd_dev:
            print "Mouse event device not found"
            return False
        print "Mouse event dev is: ", mouse_dev
         
        # Finished initialising the RS232 driver
        return True
    
    def RS232_Driver(self, arg1):
        # The driver writes or reads to/from the serial port
        # If the command is a get status command, eg "@CMD:?" then
        # it reads the corresponding status from the serial port.
        # If it's not a get status command then it writes to the 
        # serial port.
        
        
        print "RS232_Driver called. Arg1 is: ", arg1
        #with self.lock:
        #print "Lock aquired: ", self.lock
        #print "RS232_Driver called"
        if self.test_mode == "yes":
            print "RS232_Driver called in test mode. Command is: " + arg1
            print "RS232_Driver exit"
            return True
           
        ser=serial.Serial(port=self.usb_dev, 
                          baudrate=self.baudrate, 
                          bytesize=8,
        #                  rtscts=self.rtscts,
        #                  xonxoff=self.xonxoff, 
                          timeout=self.rdtmout,
                          writeTimeout=self.writeTimeout,
                          )
        print "Open serial. Ser is: ", ser
        rtn = ser.open() 
        #print 'Time after open()' , time.time()
        print "ser.open rtns is: ", rtn
        # Status request format "@" ; "Status cmd:" ; "?" ; "0xD"
        # Where "Status cmd:" is 3 char code terminated by ":"
        # Note, above ";" is a meta character separator
        # Command formatting
        l = len(arg1)
        cmd = '%s%s\r'%(arg1[0],arg1[1:l-1])
        #string = ':'.join(x.encode('hex') for x in cmd)
        #i = 0
        #for x in cmd:
        #    print "Char: " + str(i) + "is: " + x
        #    i = i + 1
        #print "Nos chars in cmd is: ", i
        #print "Hex of cmd is: ", string
        print "cmd is: "
        print cmd
        if arg1[5] == "?":
            print "Get status request: ", arg1
            rtn = ser.write(cmd)
            rd = ser.read(len(arg1)) 
            #print 'Time after read' , time.time()
            string = ':'.join(x.encode('hex') for x in rd)
            #print "Hex of Read returned is: ", string
            print "Read returned: ", rd
            if not self.chk_ACK(rd):
                pass
            ser.close()
            return True
            
            if string[3:5] == "15":
                print "NAK returned"
            ser.close()
            print "RS232_Driver exit"
            return True
        rtn = ser.write(cmd)
        print "ser.write() rtns: ", rtn
        print 'Time after write' , time.time() 
        time.sleep(self.wait_t)   
        #print 'Before read' , time.time() ;
        # Read back n bytes
        #rd = ser.read(size=rtn) 
        #print 'Time after read' , time.time()
        #print "read returned: ", rd 
        # Should return "@"; x06 ; x0D, ie "@"; ACK ; CR 
        # or "@"; x15 ; x0D, ie "@"; NAK ; CR
        # Where AK & NAK are hex values defined above and CR is Carriage
        # Return character
        #print "Read returned: ", res
        #if rd[1] == ACK:
        #    ser.close()
        #    return True
        #if rd[1] == NAK:
        #    ser.close()
        #    return False
        #print 'ACK nor NAK found: ' , rd[1] 
        ser.close()
        print "RS232_Driver exit"
        return True
    
    def chk_ACK(self, arg1):
            string = ':'.join(x.encode('hex') for x in arg1)
            #print "Hex of Read returned is: ", string
            if string[3:5] == "15":
                print "NAK returned"
                return False
            if string[3:5] == "06":
                print "ACK returned"
                return True
   
    def switch_keybd(self, arg1):
        # Sends keyboard and mouse inputs to the IP address specified in arg1
        # by calling a shell command like:
        # $ cat /dev/input/by-path/platform-i8042-serio-0-event-kbd | nc <IP> 4444
        # and
        # $ cat /dev/input/by-path/platform-i8042-serio-0-event-mouse | nc <IP> 4445
        # The client, recipient machine runs:
        # $ nc -l -p 4444 > /dev/input/by-path/platform-i8042-serio-0-event-kbd etc
        # to receive the keyboard input and process them itself.
        # Note watch out for the nc params, -l -p is different on different sys.
        print "switch_keybd called with: ", arg1
        cmd1 = "cat %s | nc %s 4444"%(keybd_dev, arg1)
        cmd2 = "cat %s | nc %s 4445"%(mouse_dev, arg1)
        print "Remote keyboard cmd is: ", cmd1
        print "Remote mouse cmd is: ", cmd2
        #call([cmd1])
        #call([cmd2])
        return True
    
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
            print 'Cmd in SR5002_cmd is: ' + cmd  
            rtn = self.RS232_Driver(cmd) 
        print "Exit SR5002_cmd"
        return rtn
 
    def SR5002_PWR_toggle (self):
        return self.SR5002_cmd("PWR:0")
    
    def SR5002_PWR_off (self):
        return self.SR5002_cmd("PWR:1")
    
    def SR5002_PWR_on (self):
        return self.SR5002_cmd("PWR:2") 
    
    def SR5002_PWR_Global_off (self):
        return self.SR5002_cmd("PWR:3")  
    
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
    
    def SR5002_Vol_up_fast (self):
        return self.SR5002_cmd("VOL:3")
    
    def SR5002_Vol_dwn_fast (self):
        return self.SR5002_cmd("VOL:4")
    
    def SR5002_Bass_up(self):
        return self.SR5002_cmd("TOB:1")
    
    def SR5002_Bass_down(self):
        return self.SR5002_cmd("TOB:2")
    
    def SR5002_Treble_up(self):
        return self.SR5002_cmd("TOT:1")
    
    def SR5002_Treble_down(self):
        return self.SR5002_cmd("TOT:2") 
    
    def SR5002_SRC_TV(self):
        print "SR5002_SRC_TV() called"
        self.switch_keybd(hdmi_port[1])
        return self.SR5002_cmd("SRC:1")
    
    def SR5002_SRC_DVD(self):
        self.switch_keybd(hdmi_port[2])
        return self.SR5002_cmd("SRC:2")
    
    def SR5002_SRC_VCR1(self):
        self.switch_keybd(hdmi_port[3])
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
    
    def SR5002_Surr_Mode(self, arg1):
        return self.SR5002_cmd(arg1)
#
# Status commands, return status of SR5002 for supplied parameter
#
    def SR5002_PWR_Stat(self):
        stat = self.SR5002_cmd("PWR:?")
        if stat == "PWR:1":
            return "OFF"
        if stat == "PWR:2":
            return "ON"
        else:
            return stat
    
    def SR5002_HDMI_Mode(self):
        stat = self.SR5002_cmd("HAM:?")
        if stat == "HAM:1":
            return "ENABLE"
        if stat == "HAM:2":
            return "THROUGH"
        else:
            return stat
    
    def SR5002_SRC_Slct(self):
        stat = self.SR5002_cmd("SRC:?")
        # SR5002 returns "SRC:va" where v & a are in the range 0x0-0xF
        # and v is video source and a is audio source
        video = stat[4]
        audio = stat[5]
        rtn[0] = video
        rtn[1] = audio
        return rtn
    
    def SR5002_API_Audio_mode(self):
        stat = self.SR5002_cmd("AMT:?")
        if stat == "AMT:1":
            return "OFF"
        if stat == "AMT:2":
            return "ON"
    
    def SR5002_API_71C_mode(self):
        stat = self.SR5002_cmd("71C:?")
        if stat == "71C:1":
            return "OFF"
        if stat == "71C:2":
            return "ON"
    
    
    
    
