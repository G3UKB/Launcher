#!/usr/bin/env python
#
# wait_device.py
#
# We wait for the given device to come on-line by trying to start
# a telnet session. This is more reliable then a ping which may succeed
# too early.
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

#-------------------------------------------------
# Wait for device to come on-line
def wait_device(target, callback):

    config = device_config[target]
    host = config["HOST"]
    port = 23
    # We wait for 30 1s timeouts before giving up
    timeout = 2
    counter = 15
    success = False
    while True:
        try:
            # Start a telnet session
            tn = telnetlib.Telnet(host, port, timeout)
            success = True
            break
        except socket.timeout:
            if counter <= 0:
                callback ('**ERROR** - Device %s failed to come on-line!' % (target))
                break
            else:
                counter -= 1
                callback('.', CRLF=False)
        except Exception as e:
            callback ('**ERROR** - Exception from wait_device [%s][%s]' % (str(e), traceback.format_exc()))
            break
    if success:
        # Session established so device is on-line, now close it
        tn.close()
        callback("Device on_line")
        return True
    else:
        # Device failed to come on-line
        return False

