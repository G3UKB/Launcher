#!/usr/bin/env python
#
# telnet_client.py
#
# Telnet client for applications hosted on RPi's
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

import os,sys
sys.path.append('..')
import telnetlib
from time import sleep
from config import config
import telnet_base

#=====================================================
# A threaded telnet session for the IP5V RPi
#=====================================================
class TelnetClient(telnet_base.TelnetBase):
    
    #-------------------------------------------------
    # Constructor
    def __init__(self, target):
      
      self.__target = target
      self.__config = config.global_config[target]
      host = self.__config["HOST"]
      user = self.__config["USER"]
      password = self.__config["PASSWORD"]
      super(TelnetClient, self).__init__(host, user, password)
      
    #-------------------------------------------------
    # Thread entry point
    def run(self):
        
        for cmd in self.__config["CMD_SEQ"]:
            self.execute(cmd[0], cmd[1])
        print('Started %s application...' % (self.__target))
        # Wait for the exit event
        self.telnet_evt.wait()
        self.close()
        print("Telnet session for application %s terminated" % (self.__target))
    
    #-------------------------------------------------
    # Terminate the session  
    def terminate(self):
       self.telnet_evt.set() 
    
#==============================================================================================
# Test code
#==============================================================================================
# Entry point
if __name__ == '__main__':
    
    client = TelnetClient("IP5VSwitch")
    client.start()
    sleep(20)
    client.terminate()
    