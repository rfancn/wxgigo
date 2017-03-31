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
import os
import sys
import logging

logger = logging.getLogger(__name__)

from sdk.constants import *
from sdk.utils import load_class
from sdk.plugin.base import BasePlugin
from sdk.plugin.config import BasePluginConfig

class FSPluginHelper(object):
    """
    Filesystem Plugin helper functions
    """
    def __init__(self, app):
        super(FSPluginHelper, self).__init__()
        self.plugins_dir = app.config.plugins_dir
        # make sure plugins dir is in python search path
        sys.path.insert(1, self.plugins_dir)

    def __is_valid_plugin_module(self, plugin_name):
        # check if "plugin.py" under plugin package
        PLUGIN_FILE = os.path.join(self.plugins_dir, "{0}".format(plugin_name.lower()), "plugin.py")
        if not os.path.exists(PLUGIN_FILE):
            print "no plugin.py file under {0} plugin package".format(plugin_name)
            return False

        return True

    def fs_get_plugin_class(self, plugin_name):
        """
        Dynamically retrieve plugin class from filesystem

        @param plugin_name:   plugin name, it is a package name under plugins base directory
        @return cls:          valid Plugin class name
        """
        #if not self.__is_valid_plugin_module(plugin_name):
        #    print "Invalid plugin module: {0}".format(plugin_name)
        #    return None

        try:
            # here must convert plugin name to lowercased one
            module_path =  "{0}.plugin".format(plugin_name.lower())
            cls = load_class(module_path, WXMP_PLUGIN_CLASS_NAME)
            if not issubclass(cls, BasePlugin):
                print "Object: {0} is not a subclass of BasePlugin".format(cls)
                return None
        except Exception,e:
            raise e

        return cls

    def fs_get_plugin_config_class(self, plugin_name):
        """
        Dynamically retrieve plugin class from filesystem

        @param plugin_name:   plugin name, it is a package name under plugins base directory
        @return cls:          valid Plugin class name
        """
        if not self.__is_valid_plugin_module(plugin_name):
            print "Invalid plugin module: {0}".format(plugin_name)
            return None

        try:
            # here must convert plugin name to lowercased one
            module_path =  "{0}.plugin".format(plugin_name.lower())
            cls = load_class(module_path, WXMP_PLUGIN_CONFIG_CLASS_NAME)
            if not issubclass(cls, BasePluginConfig):
                print "Object: {0} is not a subclass of BasePluginConfig".format(cls)
                return None
        except Exception,e:
            print "Warning: No {0} plugin config class because of: {1}".format(plugin_name, e)
            return None

        return cls

    def __build_meta_dict(self, plugin_instance):
        """
        Build meta dict from plugin instance as below:
        { 'name':'x','version': '0.1', ...}

        @param:   plugin instance
        @return:  meta dict
        """
        meta_dict = {}
        for k in BasePlugin.meta_keys:
            meta_dict[k] = plugin_instance.__class__.__dict__[k]

        return meta_dict

    def fs_get_meta_all(self):
        """
        Get all plugins meta list from filesystem
        """
        meta_list = []

        all_plugin_instances = self.fs_get_plugin_instances_all()
        for pinstance in all_plugin_instances:
            d = self.__build_meta_dict(pinstance)
            meta_list.append(d)

        return meta_list

    def fs_get_meta(self, plugin_name):
        """
        Get specific plugin's meta dict by plugin name
        """
        plugin_instance = self.fs_get_plugin_instance(plugin_name)
        if not plugin_instance:
            return {}

        return self.__build_meta_dict(plugin_instance)

    def fs_get_plugin_instance(self, plugin_name):
        plugin_class = self.fs_get_plugin_class(plugin_name)
        if not plugin_class:
            return None

        try:
            plugin_instance = plugin_class()
        except Exception,e:
            raise e

        return plugin_instance

    def fs_get_plugin_instances_all(self):
        """
        Probe plugin package deployed in filesystem and try to initialize plugin instances

        @return: the list of plugin instance
        """
        # get the top-level dir under plugin parent dir

        plugin_instance_list = []
        plugin_name_list = os.walk(self.plugins_dir).next()[1]
        for plugin_name in plugin_name_list:
            plugin_instance = self.fs_get_plugin_instance(plugin_name)
            if plugin_instance:
                plugin_instance_list.append(plugin_instance)

        return plugin_instance_list
