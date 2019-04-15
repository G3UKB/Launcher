#!/usr/bin/env python
#
# telnet_ip5v.py
#
# Telnet client for IP 5V switch application hosted by RPi
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

import telnetlib
from time import sleep
import telnet_base

#=====================================================
# A threaded telnet session for the IP5V RPi
#=====================================================
class TelnetIP5v(telnet_base.TelnetBase):
    
    #-------------------------------------------------
    # Constructor
    def __init__(self):
      
      super(TelnetIP5v, self).__init__('192.168.1.109', 'pi', 'raspberry')
      
    #-------------------------------------------------
    # Thread entry point
    def run(self):
       self.execute('cd /home/pi/Projects/IP5vSwitch/src/python', '$')
       self.execute('python3 ip5v_web.py', '$')
       print('Started IP5V Switch application...')
       # Wait for the exit event
       self.telnet_evt.wait()
       self.close()
       print("Telnet session terminated")
    
    #-------------------------------------------------
    # Terminate the session  
    def terminate(self):
       self.telnet_evt.set() 
    
#==============================================================================================
# Main code
#==============================================================================================
# Entry point
if __name__ == '__main__':
    
    global telnet_evt
    
    client = TelnetIP5v()
    client.start()
    sleep(20)
    client.terminate()
    