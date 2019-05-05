#!/usr/bin/env python
#
# app_main.py
#
# Main module for applications hosted on RPi's
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
import sys
sys.path.append('..')
from main.imports import *

#=====================================================
# Main application class
#=====================================================
class AppMain:
    
    #-------------------------------------------------
    # Start application
    def app_main(self):
        
        # The one and only QT application
        self.__qtapp = QApplication([])
        
        # Create instances and connect to the IP Main Switch(s)
        ip9258_1 = IP9258()
        ip9258_1.connect(device_config["IP9258-1"]["HOST"], device_config["IP9258-1"]["USER"], device_config["IP9258-1"]["PASSWORD"])
        addToCache("IP9258-1", ip9258_1)
        ip9258_2 = IP9258()
        ip9258_2.connect(device_config["IP9258-2"]["HOST"], device_config["IP9258-2"]["USER"], device_config["IP9258-2"]["PASSWORD"])
        addToCache("IP9258-2", ip9258_2)
        
        # Create an Event for signalling between gui and sequencer threads
        self.__seq_wait_event = threading.Event()
        self.__seq_wait_event.clear()
        
        # Sequencer runs a set of commands to instantiate a system
        sequencer = Sequencer(self.__seq_wait_event)
        addToCache("Sequencer", sequencer)
        sequencer.start()
        
        # Create the main window
        self.__w = AppWindow(self.__seq_wait_event)
        # Make visible
        self.__w.show()
        
        # Enter event loop
        r = self.__qtapp.exec_()
        
        # Closedown
        telnet_inst = getInstance("IP5VSwitch")
        if telnet_inst != None:
            telnet_inst.terminate()
        sequencer.terminate()
        
#-------------------------------------------------
# Start processing and wait for user to exit the application
def main():
    try:  
        app = AppMain()
        sys.exit(app.app_main())
        
    except Exception as e:
        print ('Exception from main code','Exception [%s][%s]' % (str(e), traceback.format_exc()))

#-------------------------------------------------
# Enter here when run as script        
if __name__ == '__main__':
    main()