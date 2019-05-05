#!/usr/bin/env python
#
# ip9258.py
#
# Python ip9258 IP power switch control for the Launcher application
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

# Assigned id's for outlet 1-4 on a 4 port unit
# Note an anomaly, status returns 61-64 but control requires 60-63
ID = ('P61','P62','P63','P64')
REVERSE_ID = {'p61':1,'p62':2,'p63':3,'p64':4}

#=====================================================
# Driver for the IP9258 IP Power Switch
#=====================================================
class IP9258:
    
    #-------------------------------------------------
    # Constructor
    def __init__(self):
        
        self.__message = None

    #-------------------------------------------------
    # Set message callback  
    def set_msg_callback(self, message):
        
        self.__message = message
        
    #-------------------------------------------------
    # Connect a device
    def connect(self, ip, user, password):
        """
        Connect to the IP9528 device
        
        Arguments:
            ip          -- the ip address of the device
            user        -- the username for the device
            password    -- the password for the device
        
        """
        
        # Create an OpenerDirector with support for Basic HTTP Authentication...
        auth_handler = urllib.request.HTTPBasicAuthHandler()
        auth_handler.add_password(realm="IP9258",
                                  uri='http://%s' % (ip),
                                  user=user,
                                  passwd=password)
        self.__opener = urllib.request.build_opener(auth_handler)
    
    #-------------------------------------------------
    # Energise a relay
    def powerOn(self, ip, outlet):
        """
        Attempt to turn power on on the IP9528 device
        
        Arguments:
            ip          -- the ip address of the device
            outlet      -- the outlet 1-4
        
        """
        if outlet < 1 or outlet > 4:
            return False, 'Outlet must be 1-4'
        
        try:
            # Get the current state
            state = self.getState(ip, outlet)
            if not state:
                # Turn the outlet on 
                fd = self.__opener.open('http://%s/Set.cmd?CMD=SetPower+%s=1' % (ip, ID[outlet-1]))
                state = self.getState(ip, outlet)
                if not state:
                    return False, 'Outlet %s failed to turn on!' % (outlet)
        except Exception as e:
            self.__message('Exception in ip9258.powerOn [%s][%s]' % (str(e), traceback.format_exc()))
            return False
        finally:
            try:
                fd.close()
            except:
                pass
        return True
    
    #-------------------------------------------------
    # De-energise a relay
    def powerOff(self, ip, outlet):
        """
        Attempt to turn power off on the IP9528 device
        
        Arguments:
            ip          -- the ip address of the device
            outlet      -- the outlet 1-4
        
        """
        
        if outlet < 1 or outlet > 4:
            return False, 'Outlet must be 1-4'
        
        try:
            # Get the current state
            state = self.getState(ip, outlet)
            if state:
                # Turn the outlet off 
                fd = self.__opener.open('http://%s/Set.cmd?CMD=SetPower+%s=0' % (ip, ID[outlet-1]))
                state = self.getState(ip, outlet)
                if state:
                    self.__message('Outlet %s failed to turn off!' % (outlet))
                    return False
        except Exception as e:
            self.__message('Exception in ip9258.powerOff')
            return False
        finally:
            try:
                fd.close()
            except:
                pass
            
        return True
    
    #-------------------------------------------------
    # Get current relay state   
    def getState(self, ip, outlet):
        """
        Get the current state of the switch
        
        Arguments:
            ip  -- ip address of the device
            output  --  outlet ID
            
        """
        
        response = self.__opener.open('http://%s/Set.cmd?CMD=GetPower' % (ip))
        data = str(response.read(100))
        n = data.find('<html>')
        m = data.find('</html>')
        data = data[n+6:m]   
        data = data.split(',')
        for item in data:
            theOutlet, state = item.split('=')
            if outlet == REVERSE_ID[theOutlet.lower()]:
                if state == '1': return True
        return False
    