#!/usr/bin/env python
#
# telnet_client.py
#
# Telnet client for Launcher application
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

import getpass
import telnetlib
from time import sleep

HOST = "192.168.1.109"
user = input("Enter your remote account: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)

tn.read_until(b"login: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
tn.read_until(b"$")
print("About to cd")
tn.write(b"cd /home/pi/Projects/IP5vSwitch/src/python\n")
tn.read_until(b"$")
print("About to run")
tn.write(b"python3 ip5v_web.py\n")
tn.read_until(b"STARTED")
print("Running")
input("Return to exit")
tn.write(b"exit\n")

#print(tn.read_all().decode('ascii'))