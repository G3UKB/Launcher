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
        "PASSWORD" : 'raspberry',
        "STATE" : False
    },
    "AntennaSwitch" : {
        "HOST" : '192.168.1.178',
        "PORT" : 8888,
        "STATE" : False
    },
    "HPSDR" : {
        "STATE" : False
    },
    "FCD" : {
        "HOST" : '192.168.1.110',
        "USER" : 'pi',
        "PASSWORD" : 'raspberry',
        "STATE" : False
    },
}

run_seq = {
    "IP5VSwitch.ON" : [
        # Turn on the IP5V RPi on IP-1 port 3
        ["RELAY", "IP9258-1", True, 3],
        # Wait for boot to complete
        ["SLEEP", 10],
        # Send command sequences to start the minimal HTML server on the RPi
        ["TELNET", "IP5VSwitch", "cd /home/pi/Projects/IP5vSwitch/src/python", "$"],
        ["TELNET", "IP5VSwitch", "python3 ip5v_web_min.py 2>/dev/null", "$"]
    ],
    "IP5VSwitch.OFF" : [
        ["RELIANCE", "Camera"],
        ["RELIANCE", "FCDProPlus"],
        # Shutdown the RPi
        ["TELNET", "IP5VSwitch", "sudo shutdown -h now", "$"],
        # Wait for shutdown to complete
        ["SLEEP", 10],
        # Turn off the IP5V RPi on IP-1 port 3
        ["RELAY", "IP9258-1", False, 3],
    ],
    "Camera.ON" : [
        # Ensure IP5VSwitch is on
        ["DEPENDENCY", "IP5VSwitch"],
        # Turn on the light on IP-1 port 4
        ["RELAY", "IP9258-1", True, 4],
        # Turn on the RPi hosting the Camera on port 2
        ["RELAY", "IP5VSwitch", True, 1],
        # Wait for boot to complete
        ["SLEEP", 10],
        # Start the camera stream
        ["TELNET", "Camera", "cd /home/pi/VLC", "$"],
        ["SLEEP", 1],
        ["TELNET", "Camera", "./vlc.sh 2>/dev/null", "$"],
        # Start the client VLC (with the correct stream?)
        ["WINDOWS_CMD", "CD", "", "C:\Program Files (x86)\VideoLAN\VLC"],
        ["WINDOWS_CMD", "RUN_WITH_SHELL", "CameraVLC", "vlc.exe"],
        ["WINDOWS_CMD", "CWD", "", ""]
    ],
    "Camera.OFF" : [
        # Turn off the light on IP-1 port 4
        ["RELAY", "IP9258-1", False, 4],
        # Shutdown the RPi
        ["TELNET", "Camera", "sudo shutdown -h now", "$"],
        # Wait for shutdown to complete
        ["SLEEP", 10],
        # Turn off the RPi hosting the Camera on port 2
        ["RELAY", "IP5VSwitch", False, 1],
        # Terminate application
        ["WINDOWS_CMD", "TERM", "CameraVLC", ""]
    ],
    "AntennaSwitch.ON" : [
        # Turn on the Antenna Switch RPi on port 1
        ["RELAY", "IP9258-1", True, 1],
        # Wait for boot to complete
        ["SLEEP", 1],
        ["WINDOWS_CMD", "CD", "", "E:/Projects/AntennaSwitch/trunk/python"],
        ["WINDOWS_CMD", "RUN_NO_SHELL", "AntSwitchApp", "python antswui.py"],
        ["WINDOWS_CMD", "CWD", "", ""]
    ],
    "AntennaSwitch.OFF" : [
        # Turn off the Antenna Switch RPi on port 1
        ["RELAY", "IP9258-1", False, 1],
        # Terminate application
        ["WINDOWS_CMD", "TERM", "AntSwitchApp", ""]
    ],
    "HPSDR.ON" : [
        # Can't run this and the FCD at the same time
        ["CONSTRAINT", "FCD"],
        # Turn on the HPSDR on port 2
        ["RELAY", "IP9258-1", True, 2],
        # Start the SDRLibE server application
        ["WINDOWS_CMD", "CD", "", "E:/Projects/SDRLibE/trunk/connector/Release"],
        ["WINDOWS_CMD", "RUN_WITH_SHELL", "SDRLibEConnector", "SDRLibEConnector.exe"],
        # Start the SDR client application
        ["WINDOWS_CMD", "CD", "", "E:/Projects/SDRLibEConsole/trunk/src/python/main"],
        ["WINDOWS_CMD", "RUN_WITH_SHELL", "SDRLibEConsole", "python app_main.py manual"],
        ["WINDOWS_CMD", "CWD", "", ""]
    ],
    "HPSDR.OFF" : [
        # Turn off the HPSDR on port 2
        ["RELAY", "IP9258-1", False, 2],
        # Terminate applications
        ["WINDOWS_CMD", "TERM", "SDRLibEConnector", ""]
        ["WINDOWS_CMD", "TERM", "SDRLibEConsole", ""]
    ],
    "FCDProPlus.ON" : [
        # Can't run this and the HPSDR at the same time
        ["CONSTRAINT", "HPSDR"],
        # Ensure IP5VSwitch is on
        ["DEPENDENCY", "IP5VSwitch"],
        # Turn on the RPi hosting the FCD on port 1
        ["RELAY", "IP5VSwitch", True, 0],
        # Wait for boot to complete
        ["SLEEP", 10],
        # Start the FCD server process
        ["TELNET", "FCD", "cd /home/pi/FCD", "$"],
        ["TELNET", "FCD", "./SDRAlsaSrv.exe", "$"],
        # Start the SDRLibE server application
        ["WINDOWS_CMD", "CD", "", "E:/Projects/SDRLibE/trunk/connector/Release"],
        ["WINDOWS_CMD", "RUN_WITH_SHELL", "SDRLibEConnector", "SDRLibEConnector.exe"],
        # Start the SDR client application
        ["WINDOWS_CMD", "CD", "", "E:/Projects/SDRLibEConsole/trunk/src/python/main"],
        ["WINDOWS_CMD", "RUN_WITH_SHELL", "SDRLibEConsole", "python app_main.py manual"],
        ["WINDOWS_CMD", "CWD", "", ""]
    ],
    "FCDProPlus.OFF" : [
        # Shutdown the RPi
        ["TELNET", "FCDProPlus", "sudo shutdown -h now", "$"],
        # Wait for shutdown to complete
        ["SLEEP", 10],
        # Turn off the RPi hosting the FCD on port 1
        ["RELAY", "IP5VSwitch", False, 0],
        # Terminate applications
        ["WINDOWS_CMD", "TERM", "SDRLibEConnector", ""]
        ["WINDOWS_CMD", "TERM", "SDRLibEConsole", ""]
    ]
}
