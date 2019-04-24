#!/usr/bin/env python
#
# gui.py
#
# GUI module for the launcher application
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

class AppWindow(QMainWindow):
    
    #-------------------------------------------------
    # Constructor
    def __init__(self):
        
        super(AppWindow, self).__init__()
        
        #-------------------------------------------------
        # Set title
        self.setWindowTitle("RPi Launcher Application")
        # Set the back colour
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(59,59,59,255))
        self.setPalette(palette)
        
        #-------------------------------------------------
        # Set main panel and grid
        self.__panel = QWidget()
        self.setCentralWidget(self.__panel)
        main_grid = QGridLayout()
        self.__panel.setLayout(main_grid)
        
        #-------------------------------------------------
        # Get sequencer instance
        self.__seq = getInstance("Sequencer")
        self.__seq.set_callback(self.__complete)
        
        #-------------------------------------------------
        # Populate
        self.__setup_ui(main_grid)
         
    #-------------------------------------------------
    # Setup the UI
    def __setup_ui(self, grid):
       
        self.__ip5v = QCheckBox("IP 5v Switch")
        self.__ip5v.clicked.connect(self.__ip5v_evnt)
        grid.addWidget(self.__ip5v, 0, 0)
        self.__setStyle(self.__ip5v)
        
        self.__camera = QCheckBox("Camera + Lights")
        self.__camera.clicked.connect(self.__camera_evnt)
        grid.addWidget(self.__camera, 1, 0)
        self.__setStyle(self.__camera)
        
        self.__ant_sw = QCheckBox("Antenna Switch")
        self.__ant_sw.clicked.connect(self.__ant_sw_evnt)
        grid.addWidget(self.__ant_sw, 2, 0)
        self.__setStyle(self.__ant_sw)
        
        self.__hpsdr = QCheckBox("HPSDR")
        self.__hpsdr.clicked.connect(self.__hpsdr_evnt)
        grid.addWidget(self.__hpsdr, 3, 0)
        self.__setStyle(self.__hpsdr)
        
        self.__fcd = QCheckBox("FunCube Dongle Plus")
        self.__fcd.clicked.connect(self.__fcd_evnt)
        grid.addWidget(self.__fcd, 4, 0)
        self.__setStyle(self.__fcd)
    
    def __setStyle(self, widget):
        widget.setStyleSheet("QCheckBox {color: rgb(148,148,148); font: bold 12px}")
        
    #-------------------------------------------------
    # Event procs
    def __ip5v_evnt(self):
        self.__seq.execute_seq("IP5VSwitch")
        device_config["IP5VSwitch"]["STATE"] = True
        self.__wait_completion()
        
    def __camera_evnt(self):
        self.__seq.execute_seq("Camera")
        self.__wait_completion()
        
    def __ant_sw_evnt(self):
        self.__seq.execute_seq("AntennaSwitch")
        self.__wait_completion()
        
    def __hpsdr_evnt(self):
        self.__seq.execute_seq("HPSDR")
        self.__wait_completion()
        
    def __fcd_evnt(self):
        self.__seq.execute_seq("FCDProPlus")
        self.__wait_completion()
        
    #-------------------------------------------------
    # Callback procs
    def __complete(self):
        self.__panel.enabled(True)
        
    #-------------------------------------------------
    # Helpers
    def __wait_completion(self):
        self.__panel.enabled(False)
        
    
    