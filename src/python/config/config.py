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
    "IP9258-1" : {
        "HOST" : '192.168.1.100',
        "USER" : 'admin',
        "PASSWORD" : '12345678'
    },
    "IP9258-2" : {
        "HOST" : '192.168.1.101',
        "USER" : 'admin',
        "PASSWORD" : '12345678'
    }, 
    "IP5VSwitch" : {
        "HOST" : '192.168.1.109',
        "PORT" : 8080,
        "USER" : 'pi',
        "PASSWORD" : 'raspberry',
        "STATE" : False
    },
    "Camera" : {
        "HOST" : '192.168.1.108',
        "USER" : 'pi',
        "PASSWORD" : 'raspberry'
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
    "IP5VSwitch" : [
        # Turn on the IP5V RPi on IP-1 port 3
        ["RELAY", "IP9258-1", 3],
        # Wait for boot to complete
        ["SLEEP", 10],
        # Send command sequences to start the minimal HTML server on the RPi
        ["TELNET", "IP5VSwitch", "cd /home/pi/Projects/IP5vSwitch/src/python", "$"],
        ["TELNET", "IP5VSwitch", "python3 ip5v_web_min.py", "$"]
    ],
    "Camera" : [
        # Ensure IP5VSwitch is on
        ["TEST", "IP5VSwitch"],
        # Turn on the light on IP-1 port 4
        ["RELAY", "IP9258-1", 4],
        # Turn on the RPi hosting the Camera on port 2
        ["RELAY", "IP5VSwitch", 1],
        # Wait for boot to complete
        ["SLEEP", 10],
        # Start the camera stream
        ["TELNET", "Camera", "cd /home/pi/VLC", "$"],
        ["SLEEP", 1],
        ["TELNET", "Camera", "./vlc.sh 2>/dev/null", "$"],
        # Start the client VLC (with the correct stream?)
        ["WINDOWS_CMD", "CD", "", "C:\Program Files (x86)\VideoLAN\VLC"],
        ["WINDOWS_CMD", "RUN_WITH_SHELL", "Camera", "vlc.exe"],
        ["WINDOWS_CMD", "CWD", "", ""]
    ],
    "AntennaSwitch" : [
        # Turn on the Antenna Switch RPi on port 1
        ["RELAY", "IP9258-1", 1],
        # Wait for boot to complete
        ["SLEEP", 1],
        ["WINDOWS_CMD", "CD", "", "E:/Projects/AntennaSwitch/trunk/python"],
        ["WINDOWS_CMD", "RUN_NO_SHELL", "AntSwitch", "python antswui.py"],
        ["WINDOWS_CMD", "CWD", "", ""]
    ],
    "HPSDR" : [
        # Turn on the HPSDR on port 2
        ["RELAY", "IP9258-1", 2],
        # Start the client SDR application
        ["WINDOWS_CMD", "CD", "", "E:/Projects/SDRLibE/trunk/connector/Release"],
        ["WINDOWS_CMD", "RUN_WITH_SHELL", "Connector", "SDRLibEConnector.exe"],
        ["WINDOWS_CMD", "CWD", "", ""]
    ],
    "FCDProPlus" : [
        # Ensure IP5VSwitch is on
        ["TEST", "IP5VSwitch"],
        # Turn on the RPi hosting the FCD on port 1
        ["RELAY", "IP5VSwitch", 0],
        # Wait for boot to complete
        ["SLEEP", 5],
        # Start the FCD server process
        ["TELNET", "FCD", "cd /home/pi/FCD", "$"],
        ["TELNET", "FCD", "./SDRAlsaSrv.exe", "$"],
        # Start the client SDR application
        ["WINDOWS_CMD", "CD", "", "E:/Projects/SDRLibE/trunk/connector/Release"],
        ["WINDOWS_CMD", "RUN_WITH_SHELL", "Connector", "SDRLibEConnector.exe"],
        ["WINDOWS_CMD", "CWD", "", ""]
    ]
}
