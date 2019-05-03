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

# All imports
import sys
sys.path.append('..')
from main.imports import *

#=====================================================
# A threaded telnet session for the IP5V RPi
#=====================================================
class TelnetClient(TelnetBase):
    
    #-------------------------------------------------
    # Constructor
    def __init__(self):
      # Create a q
      self.__q = queue.Queue()
      super(TelnetClient, self).__init__()
    
    #-------------------------------------------------
    # Add a command
    def add_cmd(self, cmd):
        self.__q.put(cmd)
        
    #-------------------------------------------------
    # Thread entry point
    def run(self):
        self.message('Starting %s telnet session...' % (self.target))
        # Wait for commands
        while True:
            try:
                cmd = self.__q.get(timeout=2)
                if cmd == "TERM": break
                self.execute(cmd[0], cmd[1])
            except :
                # Timeout
                continue
            
        self.close()
        self.message("Telnet session for %s terminated" % (self.target))
    
    #-------------------------------------------------
    # Terminate the session  
    def terminate(self):
       self.__q.put("TERM")
    
#==============================================================================================
# Test code
#==============================================================================================
# Entry point
def cb(msg):
    print(msg)
    
if __name__ == '__main__':
    
    client = TelnetClient()
    client.set_callback(cb)
    if client.connect("IP5VSwitch"):
        client.start()
        sleep(10)
        print("Execute")
        client.execute( "cd /home/pi/Projects/IP5vSwitch/src/python", "$")
        print("Done execute")
        
    else:
        print("Connect fail!")
    client.terminate()
    