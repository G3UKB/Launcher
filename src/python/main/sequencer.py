#!/usr/bin/env python
#
# sequencer.py
#
# Run invocation sequence for applications hosted on RPi's
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

class Sequencer:
    
    #-------------------------------------------------
    # Constructor 
    def __init__(self):
        dispatch_table = {
            "WINDOWS_CMD" : self.__win_cmd,
            "TELNET" : self.__telnet,
            "RELAY" : self.__relay,
            "TEST" : self.__test,
            "SLEEP" : self.__sleep
        }
        self.__cwd = os.getcwd()
    
    #-------------------------------------------------
    # Run the given sequence  
    def run_seq(self, name):
        
        seq = run_seq[name]
        for inst in seq:
            if not dispatch_table[inst][0](inst):
                break
            
    #-------------------------------------------------
    # Windows command
    def __win_cmd(self, inst):
        
        cmd = inst[1]
        name = inst[2]
        path = inst[3]
        if cmd == 'CD':
            os.chdir(path)
        elif cmd == 'CWD':
            os.chdir(self.__cwd)
        elif cmd == 'RUN_NO_SHELL':
            # Run command in the same shell
            prog = subprocess.Popen(path)
            instance_cache.add_instance(name, prog)
        elif cmd == 'RUN_WITH_SHELL':
            # Run command in a new shell
            prog = subprocess.Popen(path, creationflags=subprocess.CREATE_NEW_CONSOLE, shell=False)
            instance_cache.add_instance(name, prog)
        return True
    
    #-------------------------------------------------
    # Telnet command
    def __telnet(self, inst):
        telnet_inst = instance_cache.get_instance(inst[0])
        if telnet_inst == None:
            # Create the instance
            telnet_inst = TelnetClient(inst[0])
            instance_cache.add_instance(inst[0], telnet_inst)
        for cmd in inst:
            telnet_inst.add_command(cmd)
        return True
    
    #-------------------------------------------------
    # Relay command
    def __relay(self, inst):
        if inst[1]== "IPMainSwitch":
            powerOn(device_config["IPMainSwitch"][IP], inst[2])
        elif inst[1]== "IP5VSwitch":
            set_ip5v_relay(device_config["IP5VSwitch"][IP], device_config["IP5VSwitch"][PORT], inst[2], "on")
        return True
    
    #-------------------------------------------------
    # Test command
    def __test(self, inst):
        what = inst[1]
        if device_config[what]["STATE"] == False:
            print ("Sorry, dependency %s is not running!" %(what))
            return False
        return True

    #-------------------------------------------------
    # Sleep command
    def __sleep(self, inst):
        sleep(inst[1])
        return True
        