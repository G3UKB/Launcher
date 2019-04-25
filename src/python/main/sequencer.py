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
from main.imports import *

#=====================================================
# The sequencer for script execution
#=====================================================
class Sequencer(threading.Thread):
    
    #-------------------------------------------------
    # Constructor 
    def __init__(self):
        # Init base
        threading.Thread.__init__(self)
        
        # Create a q for communication
        self.__q = queue.Queue()
      
        self.__dispatch_table = {
            "WINDOWS_CMD" : self.__win_cmd,
            "TELNET" : self.__telnet,
            "RELAY" : self.__relay,
            "TEST" : self.__test,
            "SLEEP" : self.__sleep
        }
        self.__cwd = os.getcwd()
    
    #-------------------------------------------------
    # Terminate the session  
    def terminate(self):
       self.__q.put("TERM")
    
    #-------------------------------------------------
    # Set callback  
    def set_callback(self, callback):
        
        self.__callback = callback

    #-------------------------------------------------
    # Run the given sequence  
    def execute_seq(self, seq_name):
        
        self.__q.put(seq_name)
        
    #-------------------------------------------------
    # Thread entry point  
    def run(self):
        
        # Wait for commands
        while True:
            try:
                seq_name = self.__q.get(timeout=2)
                if seq_name == "TERM": break
                seq = run_seq[seq_name]
                for inst in seq:
                    print ("Sequence: %s" %(inst))
                    if not self.__dispatch_table[inst[0]](inst):
                        break
                print ("End of sequence")
                # Let whoever know we are done
                self.__callback()
            except :
                # Timeout
                continue
            
        print("Sequence thread terminating")
        
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
            prog = Popen(path)
            addToCache(name, prog)
        elif cmd == 'RUN_WITH_SHELL':
            # Run command in a new shell
            prog = Popen(path, creationflags=CREATE_NEW_CONSOLE, shell=False)
            addToCache(name, prog)
        return True
    
    #-------------------------------------------------
    # Telnet command
    def __telnet(self, inst):
        telnet_inst = getInstance(inst[1])
        print("\n\nTelnet command ", telnet_inst, inst)
        if telnet_inst == None:
            # Create the instance
            print("Create inst")
            telnet_inst = TelnetClient(inst[1])
            addToCache(inst[1], telnet_inst)
            telnet_inst.start()
        telnet_inst.add_cmd([inst[2], inst[3]])
        return True
    
    #-------------------------------------------------
    # Relay command
    def __relay(self, inst):
        if inst[1]== "IP9258-1":
            if inst[2]:
                powerOn(device_config["IP9258-1"]["HOST"], inst[3])
            else:
                powerOff(device_config["IP9258-1"]["HOST"], inst[3])
        elif inst[1]== "IP9258-2":
            if inst[2]:
                powerOn(device_config["IP9258-2"]["HOST"], inst[3])
            else:
                powerOff(device_config["IP9258-2"]["HOST"], inst[3])
        elif inst[1]== "IP5VSwitch":
            if inst[2]:
                set_ip5v_relay(device_config["IP5VSwitch"]["HOST"], device_config["IP5VSwitch"]["PORT"], inst[3], "on")
            else:
                set_ip5v_relay(device_config["IP5VSwitch"]["HOST"], device_config["IP5VSwitch"]["PORT"], inst[3], "off")
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
        