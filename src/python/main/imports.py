#!/usr/bin/env python
#
# imports.py
#
# Imports for Launcher application
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

#=====================================================
# System imports
import os,sys
import traceback
import pickle
from sys import platform
if platform == 'linux' or platform == 'linux2':
    from subprocess import Popen
else:
    from subprocess import Popen, CREATE_NEW_CONSOLE
import urllib
from urllib import request
import telnetlib
import threading
import socket
import queue
from time import sleep
import pprint
pp = pprint.PrettyPrinter(indent=4)

#=====================================================
# Lib imports
from PyQt5.QtCore import Qt, QCoreApplication, QTimer, QObject, QRect, QEvent, QMargins
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon, QPainter, QPixmap, QPen
from PyQt5.QtWidgets import QApplication, qApp, QMainWindow
from PyQt5.QtWidgets import QWidget, QToolTip, QStyle, QStatusBar, QMainWindow, QDialog, QAction, QMessageBox, QInputDialog, QDialogButtonBox
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QFrame, QLabel, QButtonGroup, QPushButton, QRadioButton, QComboBox, QCheckBox, QSpinBox, QTabWidget, QLineEdit, QPlainTextEdit, QTextEdit

#=====================================================
# Application imports
# Common
from config.config import *
from common.instance_cache import *
# IP Switches
from ip9258.ip9258 import *
from webrelay.webrelay import *
#Telnet
from telnet.wait_device import *
from telnet.telnet_base import *
from telnet.telnet_client import *
#UI
from gui.auto_gui import *
#Main
from main.sequencer import *