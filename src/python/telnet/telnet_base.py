#!/usr/bin/env python
#
# telnet_base.py
#
# Telnet base class for IP 5V switch application hosted by RPi
# 
# Copyright (C) 2019 by G3UKB Bob Cowdery
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#    
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#    
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#    
#  The author can be reached by email at:   
#     bob@bobcowdery.plus.com
#


# All imports
from main.imports import *

#=====================================================
# The base class for the RPi telnet sessions
#=====================================================
class TelnetBase(threading.Thread):
    
    #-------------------------------------------------
    # Constructor
    def __init__(self):
        # Init base
        threading.Thread.__init__(self)
        
    #-------------------------------------------------
    # Connect session
    def connect(self, target):
        
        self.target = target
        self.__config = device_config[target]
        host = self.__config["HOST"]
        user = self.__config["USER"]
        password = self.__config["PASSWORD"]
        try:
            # Start a telnet session
            self.__tn = telnetlib.Telnet(host)
            # Logon with given credentials
            self.__tn.read_until(b"login: ")
            self.__tn.write((user +'\n').encode('ascii'))
            if password:
                self.__tn.read_until(b"Password: ")
                self.__tn.write((password +'\n').encode('ascii'))
            # Wait for the prompt
            self.__tn.read_until(b"$")
            self.message("Logon to %s successful" % (host))
        except Exception as e:
            self.message ('**ERROR** - Exception from TelnetBase.__init__()','Exception [%s][%s]' % (str(e), traceback.format_exc()))
    
    #-------------------------------------------------
    # Close session
    def close(self):
        
        self.__tn.close()
    
    #-------------------------------------------------
    # Set callback  
    def set_callback(self, message):
        
        self.message = message

    #-------------------------------------------------
    # Execute given cmd and read until resp
    def execute(self, cmd, resp):
        
        self.__tn.write((cmd + '\n').encode('ascii'))
        sleep(0.2)
        self.message (self.__tn.read_very_eager().decode('ascii'))
        #self.__tn.read_until(resp.encode('ascii'))

    