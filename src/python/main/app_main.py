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
import imports


#=====================================================
# Main application class
#=====================================================
class AppMain:
    
    #-------------------------------------------------
    # Start application
    def app_main(self):
        
        # Connect to the IP Main Switch
        ip9258.connect(device_config["IPMainSwitch"][IP], device_config["IPMainSwitch"][USER], device_config["IPMainSwitch"][PASSWORD])
        
        # Sequencer runs a set of commands to instantiate a system
        sequencer = Sequencer()
        instance_cache.addToCache("Sequencer", sequencer)
        
        sequencer.run_seq("IP5VSwitch")
        
        input("Any ket to terminate")
        
        # Create GUI
        
        # Enter event loop
        
        # Closedown
    
#-------------------------------------------------
# Start processing and wait for user to exit the application
def main():
    try:  
        app = AppMain()
        sys.exit(app.main())
        
    except Exception as e:
        print ('Exception from main code','Exception [%s][%s]' % (str(e), traceback.format_exc()))

#-------------------------------------------------
# Enter here when run as script        
if __name__ == '__main__':
    main()