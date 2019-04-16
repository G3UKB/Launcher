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
import imports

# Assigned id's for outlet 1-4 on a 4 port unit
# Note an anomaly, status returns 61-64 but control requires 60-63
ID = ('P60','P61','P62','P63')
REVERSE_ID = {'p61':1,'p62':2,'p63':3,'p64':4}

def connect(ip, user, password):
    """
    Connect to the IP9528 device
    
    Arguments:
        ip          -- the ip address of the device
        user        -- the username for the device
        password    -- the password for the device
    
    """
    
    # Create an OpenerDirector with support for Basic HTTP Authentication...
    auth_handler = urllib.request.HTTPBasicAuthHandler()
    auth_handler.add_password(realm='IP9258',
                              uri='http://%s' % (ip),
                              user=user,
                              passwd=password)
    opener = urllib.request.build_opener(auth_handler)
    # ...and install it globally so it can be used with urlopen.
    urllib.request.install_opener(opener)

def powerOn(ip, outlet):
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
        state = getState(ip, outlet)
        if not state:
            # Turn the outlet on 
            fd = urllib.request.urlopen('http://%s/Set.cmd?CMD=SetPower+%s=1' % (ip, ID[outlet]))
            state = getState(ip, outlet)
            if not state:
                return False, 'Outlet %s failed to turn on!' % (outlet)
    except Exception as e:
        return False, 'Exception in ip9258.powerOn [%s][%s]' % (str(e), traceback.format_exc())
    finally:
        try:
            fd.close()
        except:
            pass
        
    return True ,''

def powerOff(ip, outlet):
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
        state = getState(ip, outlet)
        if state:
            # Turn the outlet off 
            fd = urllib.request.urlopen('http://%s/Set.cmd?CMD=SetPower+%s=0' % (ip, ID[outlet]))
            state = getState(ip, outlet)
            if state:
                return False, 'Outlet %s failed to turn off!' % (outlet)
    except Exception as e:
        return False, 'Exception in ip9258.powerOff'
    finally:
        try:
            fd.close()
        except:
            pass
        
    return True ,''
    
def getState(ip, outlet):
    """
    Get the current state of the switch
    
    Arguments:
        ip  -- ip address of the device
        output  --  outlet ID
        
    """
    
    response = urllib.request.urlopen('http://%s/Set.cmd?CMD=GetPower' % (ip))
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
    
#==============================================================================================
# Test code
#==============================================================================================
# Entry point
if __name__ == '__main__':
    
    connect('192.168.1.100', 'admin', '12345678')
    powerOn('192.168.1.100', 1)
    print(getState('192.168.1.100', 1))
    sleep(5)
    powerOff('192.168.1.100', 1)