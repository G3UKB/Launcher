#
# config.py
#
# Configuration for IP 5V switch applications hosted on RPi's
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

global_config = {
    "IPMainSwitch" : {
        "HOST" : '192.168.1.100',
        "USER" : 'admin',
        "PASSWORD" : '12345678',
    },
        
    "IP5VSwitch" : {
        "HOST" : '192.168.1.109',
        "USER" : 'pi',
        "PASSWORD" : 'raspberry',
        "CMD_SEQ" : (
            ('cd /home/pi/Projects/IP5vSwitch/src/python', '$'),
            ('python3 ip5v_web.py', '$'),   
        )
    },
    "AntennaSwitch" : {
        "HOST" : '192.168.1.178',
        "PORT" : 8888,
    },
}

sequences = {
    "AntennaSwitch" : [
        
    ],
    "HPSDR" : [
        ["IPMainSwitch", 2],
        ["SDRLibEConnector"]
    ],
    "FCDProPlus" : [
        # Turn on the IP5V RPi on port 3
        ["IPMainSwitch", 3],
        # Wait for boot to complete
        ["SLEEP", 5],
        # Send command sequences to start the minimal server
        ["CMD", 'cd /home/pi/Projects/IP5vSwitch/src/python', '$']
        ["CMD", 'python3 ip5v_web_min.py', '$']
        # Turn on the RPi device on port 1
        ["IP5VSwitch", 1],
        # Wait for boot to complete
        ["SLEEP", 5],
        # Start the FCD server process
        []
        # Start the client SDR application
        ["SDRLibEConnector"]
    ]
}
