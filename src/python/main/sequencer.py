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
    def __init__(self, evnt):
        # Init base
        threading.Thread.__init__(self)
        
        # Sync event
        self.__evnt = evnt
        
        # Create a q for communication
        self.__q = queue.Queue()
      
        self.__dispatch_table = {
            "WINDOWS_CMD" : self.__win_cmd,
            "WAIT_DEVICE" : self.__wait_device,
            "TELNET" : self.__telnet,
            "TELNET_CLOSE" : self.__telnet_close,
            "RELAY" : self.__relay,
            "DEPENDENCY" : self.__dependent,
            "CONSTRAINT" : self.__constraint,
            "RELIANCE" : self.__reliance,
            "SLEEP" : self.__sleep,
            "DIALOG" : self.__dialog,
            "MSG" : self.__msg
        }
        self.__cwd = os.getcwd()
    
    #-------------------------------------------------
    # Terminate the session  
    def terminate(self):
       self.__q.put("TERM")
    
    #-------------------------------------------------
    # Set callback  
    def set_callback(self, complete, message):
        
        self.__complete = complete
        self.__message = message
    #-------------------------------------------------
    # Set message callback  
    def set_msg_callback(self, message):
        
        self.__message = message
        
    #-------------------------------------------------
    # Set complete callback  
    def set_complete_callback(self, complete):
        
        self.__complete = complete
        
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
                    self.__message ("Sequence: %s" %(inst))
                    if not self.__dispatch_table[inst[0]](inst):
                        # Let whoever know we are done with error
                        self.__complete(False)
                        break
                self.__message ("End of sequence")
                # Let whoever know we are done successful
                self.__complete(True)
            except :
                # Timeout
                continue
            
        self.__message("Sequence thread terminating")
        
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
            if platform == 'linux' or platform == 'linux2':
                prog = Popen(path, shell=False)
            else:
                prog = Popen(path, creationflags=CREATE_NEW_CONSOLE, shell=False)
            addToCache(name, prog)
        elif cmd == 'TERM':
            # Get Popen object
            obj = getInstance(name)
            if obj != None:
                obj.terminate()
            # Must remove as the program was terminated
            removeInstance(name)
                
        return True
    
    #-------------------------------------------------
    # Wait device command
    def __wait_device(self, inst):
        if wait_device(inst[1], self.__message):
            # Device on-line
            return True
        else:
            return False
        
    #-------------------------------------------------
    # Telnet command
    def __telnet(self, inst):
        telnet_inst = getInstance(inst[1])
        if telnet_inst == None:
            # Create the instance
            telnet_inst = TelnetClient()
            telnet_inst.set_callback (self.__message)
            if telnet_inst.connect(inst[1]):
                addToCache(inst[1], telnet_inst)
                telnet_inst.start()
            else:
                return False
        telnet_inst.add_cmd([inst[2], inst[3]])
        return True
    
    #-------------------------------------------------
    # Telnet close
    def __telnet_close(self, inst):
        # Close the telnet session and remove the instance
        telnet_inst = getInstance(inst[1])
        if telnet_inst != None:
           telnet_inst.terminate()
           removeInstance(inst[1])
        return True
           
    #-------------------------------------------------
    # Relay command
    def __relay(self, inst):
        if inst[1]== "IP9258-1":
            if inst[2]:
                getInstance("IP9258-1").powerOn(device_config["IP9258-1"]["HOST"], inst[3])
            else:
                getInstance("IP9258-1").powerOff(device_config["IP9258-1"]["HOST"], inst[3])
        elif inst[1]== "IP9258-2":
            if inst[2]:
                getInstance("IP9258-2").powerOn(device_config["IP9258-2"]["HOST"], inst[3])
            else:
                getInstance("IP9258-2").powerOff(device_config["IP9258-2"]["HOST"], inst[3])
        elif inst[1]== "IP5VSwitch":
            if inst[2]:
                set_web_relay(device_config["IP5VSwitch"]["HOST"], device_config["IP5VSwitch"]["PORT"], inst[3], "on")
            else:
                set_web_relay(device_config["IP5VSwitch"]["HOST"], device_config["IP5VSwitch"]["PORT"], inst[3], "off")
        elif inst[1]== "PortSwitch":
            if inst[2]:
                set_web_relay(device_config["PortSwitch"]["HOST"], device_config["PortSwitch"]["PORT"], inst[3], "on")
            else:
                set_web_relay(device_config["PortSwitch"]["HOST"], device_config["PortSwitch"]["PORT"], inst[3], "off")
        return True
    
    #-------------------------------------------------
    # Dependency command
    def __dependent(self, inst):
        what = inst[1]
        if device_config[what]["STATE"] == False:
            self.__message ("**WARN** - dependency %s is not running!" %(what))
            return False
        return True
    
    #-------------------------------------------------
    # Constraint command
    def __constraint(self, inst):
        what = inst[1]
        if device_config[what]["STATE"] == True:
            self.__message ("**WARN** - constraint %s is running!" %(what))
            return False
        return True
    
    #-------------------------------------------------
    # Reliance command
    def __reliance(self, inst):
        what = inst[1]
        if device_config[what]["STATE"] == True:
            self.__message ("**WARN** - please stop %s first as it relies on this service!" %(what))
            return False
        return True
    
    #-------------------------------------------------
    # Sleep command
    def __sleep(self, inst):
        sleep(inst[1])
        return True
    
    #-------------------------------------------------
    # Dialog command
    def __dialog(self, inst):
        self.__message (inst[1], True)
        # Wait for the gui operation to complete
        self.__evnt.wait()
        self.__evnt.clear()
        return True

    #-------------------------------------------------
    # Message command
    def __msg(self, inst):
        self.__message (inst[1])
        return True    