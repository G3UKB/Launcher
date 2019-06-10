#
# config.py
#
# Configuration for all supported devices
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
        "UI" : False,
        "HOST" : '192.168.1.100',
        "USER" : 'admin',
        "PASSWORD" : '12345678'
    },
    "IP9258-2" : {
        "UI" : False,
        "HOST" : '192.168.1.101',
        "USER" : 'admin',
        "PASSWORD" : '12345678'
    }, 
    "IP5VSwitch" : {
        "UI" : True,
        "LABEL" : "IP 5v Switch",
        "HOST" : '192.168.1.109',
        "PORT" : 8080,
        "USER" : 'pi',
        "PASSWORD" : 'raspberry',
        "STATE" : False
    },
    "PortSwitch" : {
        "UI" : True,
        "LABEL" : "IP Port Switch",
        "HOST" : '192.168.1.111',
        "PORT" : 8080,
        "USER" : 'pi',
        "PASSWORD" : 'raspberry',
        "STATE" : False
    },
    "Camera" : {
        "UI" : True,
        "LABEL" : "Camera",
        "HOST" : '192.168.1.108',
        "USER" : 'pi',
        "PASSWORD" : 'raspberry',
        "STATE" : False
    },
    "AntennaSwitch" : {
        "UI" : True,
        "LABEL" : "Antenna Switch",
        "HOST" : '192.168.1.178',
        "PORT" : 8888,
        "STATE" : False
    },
    "HPSDR" : {
        "UI" : True,
        "LABEL" : "HPSDR",
        "STATE" : False
    },
    "FCD" : {
        "UI" : True,
        "LABEL" : "FUNcube Dongle Pro+",
        "HOST" : '192.168.1.110',
        "USER" : 'pi',
        "PASSWORD" : 'raspberry',
        "STATE" : False
    },
    "LoopTuner" : {
        "UI" : True,
        "LABEL" : "Loop Tuner",
        "STATE" : False
    },
    "SatRot" : {
        "UI" : True,
        "LABEL" : "Az/El Rotator",
        "STATE" : False
    },
    "VNA" : {
        "UI" : True,
        "LABEL" : "Mini VNA",
        "STATE" : False
    },
    "LinuxDesktop" : {
        "UI" : True,
        "LABEL" : "Linux Desktop",
        "HOST" : 'bob-desktop-linux',
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
        # Start with the config for the ip5v switch
        ["TELNET", "IP5VSwitch", "python3 ip5v_web_min.py conf/ip5v.conf 2>/dev/null", "$"]
    ],
    "IP5VSwitch.OFF" : [
        ["RELIANCE", "PortSwitch"],
        ["RELIANCE", "Camera"],
        ["RELIANCE", "FCD"],
        # Shutdown the RPi
        ["TELNET", "IP5VSwitch", "sudo shutdown -h now", "$"],
        # Wait for shutdown to complete
        ["SLEEP", 10],
        # Turn off the IP5V RPi on IP-1 port 3
        ["RELAY", "IP9258-1", False, 3],
        # Close telnet
        ["TELNET_CLOSE", "IP5VSwitch"]
    ],
    "PortSwitch.ON" : [
        # Ensure IP5VSwitch is on
        ["DEPENDENCY", "IP5VSwitch"],
        # Turn on the RPi hosting the PortSwitch on port 1
        ["RELAY", "IP5VSwitch", True, 0],
        # Wait for boot to complete
        ["SLEEP", 10],
        # Send command sequences to start the minimal HTML server on the RPi
        ["TELNET", "PortSwitch", "cd /home/pi/Projects/IP5vSwitch/src/python", "$"],
        # Start with the config for the port switch
        ["TELNET", "PortSwitch", "python3 ip5v_web_min.py conf/portsw.conf 2>/dev/null", "$"]
    ],
    "PortSwitch.OFF" : [
        ["RELIANCE", "FCD"],
        # Shutdown the RPi
        ["TELNET", "PortSwitch", "sudo shutdown -h now", "$"],
        # Wait for shutdown to complete
        ["SLEEP", 10],
        # Turn off the RPi hosting the PortSwitch on port 1
        ["RELAY", "PortSwitch", False, 0],
        # Close telnet
        ["TELNET_CLOSE", "PortSwitch"]
    ],
    "Camera.ON" : [
        # Ensure IP5VSwitch is on
        ["DEPENDENCY", "IP5VSwitch"],
        # Turn on the light on IP-2 port 1
        ["RELAY", "IP9258-2", True, 1],
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
        ["WINDOWS_CMD", "RUN_WITH_SHELL", "CameraVLC", "vlc.exe rtsp://192.168.1.108:8554/"],
        ["WINDOWS_CMD", "CWD", "", ""]
    ],
    "Camera.OFF" : [
        # Turn off the light on IP-2 port 1
        ["RELAY", "IP9258-2", False, 1],
        # Shutdown the RPi
        ["TELNET", "Camera", "sudo shutdown -h now", "$"],
        # Wait for shutdown to complete
        ["SLEEP", 10],
        # Turn off the RPi hosting the Camera on port 2
        ["RELAY", "IP5VSwitch", False, 1],
        # Terminate application
        ["WINDOWS_CMD", "TERM", "CameraVLC", ""],
        # Close telnet
        ["TELNET_CLOSE", "Camera"]
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
        ["WINDOWS_CMD", "TERM", "SDRLibEConnector", ""],
        ["WINDOWS_CMD", "TERM", "SDRLibEConsole", ""]
    ],
    "FCDProPlus.ON" : [
        # Can't run this and the HPSDR at the same time
        ["CONSTRAINT", "HPSDR"],
        # Ensure IP5VSwitch is on
        ["DEPENDENCY", "IP5VSwitch"],
        # Turn on the RPi hosting the FCD on port 2
        ["RELAY", "IP5VSwitch", True, 1],
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
        # Turn off the RPi hosting the FCD on port 2
        ["RELAY", "IP5VSwitch", False, 2],
        # Terminate applications
        ["WINDOWS_CMD", "TERM", "SDRLibEConnector", ""],
        ["WINDOWS_CMD", "TERM", "SDRLibEConsole", ""],
        # Close telnet
        ["TELNET_CLOSE", "FCDProPlus"]
    ],
    "LoopTuner.ON" : [
        ["MSG", "Not Implemented!"]
    ],
    "LoopTuner.OFF" : [
        ["MSG", "Not Implemented!"]
    ],
    "SatRot.ON" : [
        ["MSG", "Not Implemented!"]
    ],
    "SatRot.OFF" : [
        ["MSG", "Not Implemented!"]
    ],
    "VNA.ON" : [
        ["MSG", "Not Implemented!"]
    ],
    "VNA.OFF" : [
        ["MSG", "Not Implemented!"]
    ],
    "LinuxDesktop.ON" : [
        # Turn on the computer on IP-1 port 4
        ["RELAY", "IP9258-1", True, 4],
        # Wait for the computer to boot. It's a slow machine!
        ["SLEEP", 40],
        # Start the VNC client application
        ["WINDOWS_CMD", "RUN_WITH_SHELL", "vncviewer", "vncviewer %s:0" % (device_config["LinuxDesktop"]["HOST"])]
    ],
    "LinuxDesktop.OFF" : [
        # Turn off the computer on IP-1 port 4
        ["DIALOG", "Please terminate your session and press OK when done."],
        # Stop the VNC client application
        ["WINDOWS_CMD", "TERM", "vncviewer", ""],
        # Turn off the computer on IP-1 port 4
        ["RELAY", "IP9258-1", False, 4],
        
    ],
}
