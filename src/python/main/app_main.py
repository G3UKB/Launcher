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
        
        # Connect to the IP Main Switch
        connect(device_config["IP9258-1"]["HOST"], device_config["IP9258-1"]["USER"], device_config["IP9258-1"]["PASSWORD"])
        
        # Sequencer runs a set of commands to instantiate a system
        sequencer = Sequencer()
        addToCache("Sequencer", sequencer)
        
        #sequencer.execute_seq("IP5VSwitch")
        
        #input("Any key to terminate")
        #telnet_inst = getInstance("IP5VSwitch")
        #if telnet_inst != None:
        #    telnet_inst.terminate()
        
        # Create the main window
        self.__w = AppWindow()
        # Make visible
        self.__w.show()
        
        # Enter event loop
        r = self.__qtapp.exec_()
        
        # Closedown
        telnet_inst = getInstance("IP5VSwitch")
        if telnet_inst != None:
            telnet_inst.terminate()
        
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