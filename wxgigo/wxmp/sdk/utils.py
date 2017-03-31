#!/usr/bin/env python
# coding=utf-8
"""
 Copyright (C) 2010-2013, Ryan Fan <ryan.fan@oracle.com>

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Library General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
"""
from __future__ import absolute_import
import importlib
import logging

logger = logging.getLogger(__name__)

def load_class(module_path, class_name):
    try:
        mod = importlib.import_module(module_path)
        cls = getattr(mod, class_name)
    except ImportError:
        raise ValueError("Module '%s' could not be imported" % (module_path,))

    return cls

def load_module(module_path):
    try:
        mod = importlib.import_module(module_path)
    except ImportError:
        raise ValueError("Error: Module '%s' could not be imported" % (module_path,))

    return mod



#def load_class(module_path, class_name):
#    try:
#        module = __import__(module_path, fromlist=[class_name])
#    except ImportError:
#        raise ValueError("Module '%s' could not be imported" % (module_path,))

#    try:
#        cls = getattr(module, class_name)
#    except AttributeError:
#        raise ValueError("Module '%s' has no class '%s'" % (module_path, class_name,))

#    return cls

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)
