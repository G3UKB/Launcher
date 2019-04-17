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

device_config = {
    "IPMainSwitch" : {
        "HOST" : '192.168.1.100',
        "USER" : 'admin',
        "PASSWORD" : '12345678'
    },   
    "IP5VSwitch" : {
        "HOST" : '192.168.1.109',
        "PORT" : 8080,
        "USER" : 'pi',
        "PASSWORD" : 'raspberry',
        "CMD_SEQ" : (
            ('cd /home/pi/Projects/IP5vSwitch/src/python', '$'),
            ('python3 ip5v_web.py', '$')  
        )
    },
    "AntennaSwitch" : {
        "HOST" : '192.168.1.178',
        "PORT" : 8888
    },
    "FCD" : {
        "HOST" : '192.168.1.110',
        "USER" : 'pi',
        "PASSWORD" : 'raspberry'
    },
}

run_seq = {
    "AntennaSwitch" : [
        # Turn on the Antenna Switch RPi on port 1
        ["RELAY", "IPMainSwitch", 1],
        # Wait for boot to complete
        ["SLEEP", 1],
        ["WINDOWS_CMD", "CD", "E:/Projects/AntennaSwitch/trunk/python"],
        ["WINDOWS_CMD", "RUN_NO_SHELL", "python antswui.py"]
    ],
    "HPSDR" : [
        # Turn on the HPSDR on port 2
        ["RELAY", "IPMainSwitch", 2],
        # Start the client SDR application
        ["WINDOWS_CMD", "CD", "E:/Projects/SDRLibE/trunk/connector/Release"],
        ["WINDOWS_CMD", "RUN_WITH_SHELL", "SDRLibEConnector.exe"],
        ["WINDOWS_CMD", "CWD"]
    ],
    "FCDProPlus" : [
        # Turn on the IP5V RPi on port 3
        ["RELAY", "IPMainSwitch", 3],
        # Wait for boot to complete
        ["SLEEP", 5],
        # Send command sequences to start the minimal HTML server on the RPi
        ["TELNET", "IP5VSwitch", "cd /home/pi/Projects/IP5vSwitch/src/python", "$"],
        ["TELNET", "IP5VSwitch", "python3 ip5v_web_min.py", "$"],
        # Turn on the RPi hosting the FCD on port 1
        ["RELAY", "IP5VSwitch", 1],
        # Wait for boot to complete
        ["SLEEP", 5],
        # Start the FCD server process
        ["TELNET", "FCD", "cd /home/pi/FCD", "$"],
        ["TELNET", "FCD", "./SDRAlsaSrv.exe", "$"],
        # Start the client SDR application
        ["WINDOWS_CMD", "CD", "E:/Projects/SDRLibE/trunk/connector/Release"],
        ["WINDOWS_CMD", "RUN_WITH_SHELL", "SDRLibEConnector.exe"],
        ["WINDOWS_CMD", "CWD"]
    ]
}
