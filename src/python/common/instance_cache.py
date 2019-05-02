#!/usr/bin/env python
#
# instance_cache.py
#
# Cache class instances to save passing these around
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

# Cache of {name : inst, name : inst}
instCache = {}

#-------------------------------------------------
# Add an instance to the cache
def addToCache(name, instance):
    """
    Add a class instance
    
    name        --  name of the instance
    instance    --  the created and initialise instance
    
    """
    
    instCache[name] = instance

#-------------------------------------------------
# Get an instance from the cache    
def getInstance(name):
    """
    Get the one and only class instance
    
    name    --  name of the instance
    
    """
    
    if name in instCache:
        return instCache[name]
    else:
        return None

#-------------------------------------------------
# Remove an instance from the cache    
def removeInstance(name):
    """
    Remove the one and only class instance
    
    name    --  name of the instance
    
    """
    
    if name in instCache:
        del instCache[name]
    