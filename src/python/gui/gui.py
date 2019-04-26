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
       
        ip5v_label = QLabel("IP 5v Switch")
        self.__ip5v_cb_on = QCheckBox("On")
        ip5v_cb_off = QCheckBox("Off")
        self.__ip5v_grp = QButtonGroup()
        self.__ip5v_btn = QPushButton("Set")
        self.__setup_func(grid, ip5v_label, self.__ip5v_cb_on, ip5v_cb_off, self.__ip5v_grp, self.__ip5v_btn, self.__ip5v_evnt, 0)
        
        camera_label = QLabel("Camera")
        self.__camera_cb_on = QCheckBox("On")
        camera_cb_off = QCheckBox("Off")
        self.__camera_grp = QButtonGroup()
        self.__camera_btn = QPushButton("Set")
        self.__setup_func(grid, camera_label, self.__camera_cb_on, camera_cb_off, self.__camera_grp, self.__camera_btn, self.__camera_evnt, 1)
        
        ant_sw_label = QLabel("Antenna Switch")
        self.__ant_sw_cb_on = QCheckBox("On")
        ant_sw_cb_off = QCheckBox("Off")
        self.__ant_sw_grp = QButtonGroup()
        self.__ant_sw_btn = QPushButton("Set")
        self.__setup_func(grid, ant_sw_label, self.__ant_sw_cb_on, ant_sw_cb_off, self.__ant_sw_grp, self.__ant_sw_btn, self.__ant_sw_evnt, 2)
        
        hpsdr_label = QLabel("HPSDR")
        self.__hpsdr_cb_on = QCheckBox("On")
        hpsdr_cb_off = QCheckBox("Off")
        self.__hpsdr_grp = QButtonGroup()
        self.__hpsdr_btn = QPushButton("Set")
        self.__setup_func(grid, hpsdr_label, self.__hpsdr_cb_on, hpsdr_cb_off, self.__hpsdr_grp, self.__hpsdr_btn, self.__hpsdr_evnt, 3)
        
        fcd_label = QLabel("FunCube Dongle Plus")
        self.__fcd_cb_on = QCheckBox("On")
        fcd_cb_off = QCheckBox("Off")
        self.__fcd_grp = QButtonGroup()
        self.__fcd_btn = QPushButton("Set")
        self.__setup_func(grid, fcd_label, self.__fcd_cb_on, fcd_cb_off, self.__fcd_grp, self.__fcd_btn, self.__fcd_evnt, 4)
    
    #-------------------------------------------------
    # Setup one function
    def __setup_func(self, grid, label, cb_on, cb_off, group, button, evnt, col):
        
        grid.addWidget(label, col, 0)
        grid.addWidget(cb_on, col, 1)
        cb_off.setChecked(True)
        grid.addWidget(cb_off, col, 2)
        group.setExclusive(True)
        group.addButton(cb_on)
        group.setId(cb_on, 0)
        group.addButton(cb_off)
        group.setId(cb_off, 1)
        button.clicked.connect(evnt)
        grid.addWidget(button, col, 3)
        self.__setStyle(label, cb_on, cb_off, button)
        
    #-------------------------------------------------
    # Setup style  
    def __setStyle(self, label, cb_on, cb_off, button):
        label.setStyleSheet("QLabel {color: rgb(199,199,199); font: bold 12px}")
        cb_on.setStyleSheet("QCheckBox {color: rgb(199,199,199); font: bold 12px}")
        cb_off.setStyleSheet("QCheckBox {color: rgb(199,199,199); font: bold 12px}")
        button.setStyleSheet("QPushButton {background-color: rgb(167,85,65); color: rgb(199,199,199); font: bold 12px}")
        
    #-------------------------------------------------
    # Event procs
    def __ip5v_evnt(self):
        if self.__ip5v_cb_on.isChecked() :
            self.__seq.execute_seq("IP5VSwitch.ON")
            device_config["IP5VSwitch"]["STATE"] = True
            self.__wait_completion()
        else:
            self.__seq.execute_seq("IP5VSwitch.OFF")
            device_config["IP5VSwitch"]["STATE"] = False
            self.__wait_completion()
        
    def __camera_evnt(self):
        if self.__camera_cb_on.isChecked() :
            self.__seq.execute_seq("Camera.ON")
            device_config["Camera"]["STATE"] = True
            self.__wait_completion()
        else:
            self.__seq.execute_seq("Camera.OFF")
            device_config["Camera"]["STATE"] = False
            self.__wait_completion()
        
    def __ant_sw_evnt(self):
        if self.__ant_sw_cb_on.isChecked() :
            self.__seq.execute_seq("AntennaSwitch.ON")
            device_config["AntennaSwitch"]["STATE"] = True
            self.__wait_completion()
        else:
            self.__seq.execute_seq("AntennaSwitch.OFF")
            device_config["AntennaSwitch"]["STATE"] = False
            self.__wait_completion()
        
    def __hpsdr_evnt(self):
        if self.__hpsdr_cb_on.isChecked() :
            self.__seq.execute_seq("HPSDR.ON")
            device_config["HPSDR"]["STATE"] = True
            self.__wait_completion()
        else:
            self.__seq.execute_seq("HPSDR.OFF")
            device_config["HPSDR"]["STATE"] = False
            self.__wait_completion()
        
    def __fcd_evnt(self):
        if self.__fcd_cb_on.isChecked() :
            self.__seq.execute_seq("FCDProPlus.ON")
            device_config["FCDProPlus"]["STATE"] = True
            self.__wait_completion()
        else:
            self.__seq.execute_seq("FCDProPlus.OFF")
            device_config["FCDProPlus"]["STATE"] = False
            self.__wait_completion()
        
    #-------------------------------------------------
    # Callback procs
    def __complete(self):
        self.__panel.setEnabled(True)
        
    #-------------------------------------------------
    # Helpers
    def __wait_completion(self):
        self.__panel.setEnabled(False)
        
    
    