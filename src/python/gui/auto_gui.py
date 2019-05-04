#!/usr/bin/env python
#
# auto_gui.py
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

IDLE_TICKER = 100
LABEL = 0
CB_ON = 1
CB_OFF = 2
CB_GRP = 3
BUTTON = 4
EVNT_CLS = 5

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
        # Add a box layout
        main_box = QVBoxLayout()
        self.__panel.setLayout(main_box)
        sub_panel = QWidget()
        main_box.addWidget(sub_panel)
        main_grid = QGridLayout()
        sub_panel.setLayout(main_grid)
        
        #-------------------------------------------------
        # Get sequencer instance
        self.__seq = getInstance("Sequencer")
        self.__seq.set_msg_callback(self.__message)
        
        #-------------------------------------------------
        # Populate
        self.__widgets = {}
        self.__setup_ui(self.__seq, sub_panel, main_grid)
        
        # Add a logging area
        self.__log = QTextEdit()
        main_box.addWidget(self.__log)
        self.__log.insertPlainText("Launcher initialised\n")
        
        # Dispatch worker threads to the main thread
        # Create a q for communication
        self.__q = queue.Queue()
        QTimer.singleShot(IDLE_TICKER, self.timer_evnt)
         
    
    #-------------------------------------------------
    # Setup the UI
    def __setup_ui(self, seq, panel, grid):
       
        # Setup is dynamic from the device list
        line = 0
        for dev in device_config:
            if device_config[dev]["UI"]:
                # Needs a UI entry
                self.__widgets[dev] = []               
                self.__widgets[dev].append (QLabel(device_config[dev]["LABEL"]))
                self.__widgets[dev].append (QCheckBox("On"))   
                self.__widgets[dev].append (QCheckBox("Off"))
                self.__widgets[dev].append (QButtonGroup())
                self.__widgets[dev].append (QPushButton("Set"))
                self.__widgets[dev].append (EventCls(seq, panel, dev, self.__widgets[dev]))
                self.__setup_func(grid, self.__widgets[dev], line)
                line += 1              
        
    #-------------------------------------------------
    # Setup one function
    def __setup_func(self, grid, widgets, line):
        
        grid.addWidget(widgets[LABEL], line, 0)
        grid.addWidget(widgets[CB_ON], line, 1)
        widgets[CB_OFF].setChecked(True)
        grid.addWidget(widgets[CB_OFF], line, 2)
        widgets[CB_GRP].setExclusive(True)
        widgets[CB_GRP].addButton(widgets[CB_ON])
        widgets[CB_GRP].setId(widgets[CB_ON], 0)
        widgets[CB_GRP].addButton(widgets[CB_OFF])
        widgets[CB_GRP].setId(widgets[CB_OFF], 1)
        widgets[BUTTON].clicked.connect(widgets[EVNT_CLS].event_proc)
        grid.addWidget(widgets[BUTTON], line, 3)
        self.__setStyle(widgets[LABEL], widgets[CB_ON], widgets[CB_OFF], widgets[BUTTON])
        
    #-------------------------------------------------
    # Setup style  
    def __setStyle(self, label, cb_on, cb_off, button):
        label.setStyleSheet("QLabel {color: rgb(199,199,199); font: bold 12px}")
        cb_on.setStyleSheet("QCheckBox {color: rgb(199,199,199); font: bold 12px}")
        cb_off.setStyleSheet("QCheckBox {color: rgb(199,199,199); font: bold 12px}")
        button.setStyleSheet("QPushButton {background-color: rgb(167,85,65); color: rgb(199,199,199); font: bold 12px}")
    
    #-------------------------------------------------
    # Event procs
    # Timer event
    def timer_evnt(self):
        # Process any messages
        # These have writen from the main thread
        try:
            while True:
                msg = self.__q.get_nowait()
                self.__log.insertPlainText(msg)
                self.__log.ensureCursorVisible()
        except:
            pass
        
        # Next kick
        QTimer.singleShot(IDLE_TICKER, self.timer_evnt)
    
    #-------------------------------------------------
    # Callback procs
    # Message output
    def __message (self, message):
        # Just add to the q for processing in the timer event
        self.__q.put(message + "\n")

#-------------------------------------------------
# Each required event creates an instance of this class
# such that the whole UI is dynamic
class EventCls:
    
    def __init__(self, seq, panel, dev_name, widgets):
        # The sequencer instance
        self.__seq = seq
        # The main panel
        self.__panel = panel
        # The device name
        self.__dev_name = dev_name
        # The set of widgets for this device
        self.__widgets = widgets
        # Last state, True = On, False = Off
        self.__lastState = None
    
    #-------------------------------------------------
    # Event proc called from target button click   
    def event_proc(self):
        
        # Set the callback to us
        self.__seq.set_complete_callback(self.__complete)
        
        # Run the sequence
        if self.__widgets[CB_ON].isChecked() :
            self.__seq.execute_seq(self.__dev_name + ".ON")
            device_config[self.__dev_name]["STATE"] = True
            self.__wait_completion()
            self.__lastState = True
        else:
            self.__seq.execute_seq(self.__dev_name + ".OFF")
            device_config[self.__dev_name]["STATE"] = False
            self.__wait_completion()
            self.__lastState = False
            
    #-------------------------------------------------
    # Callback procs
    # Sequence complete
    def __complete(self, result):
        if result == False:
            # The sequence failed so we need to adjust the UI
            state = self.__last_state
            if state:
                # We were trying to turn the device on so we fail to the off state
                self.__widgets[CB_OFF].setChecked(True)
            else:
                # We were trying to turn the device off so we fail to the on state
                self.__widgets[CB_ON].setChecked(True)
        self.__panel.setEnabled(True)
    
    #-------------------------------------------------
    # Helpers
    def __wait_completion(self):
        self.__panel.setEnabled(False)
        
    
    