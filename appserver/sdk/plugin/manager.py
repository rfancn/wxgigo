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
import logging
import multiprocessing
import signal

from sdk.plugin.helper import PluginHelper
from sdk.plugin.dummy import DummyPlugin

logger = logging.getLogger(__name__)

class PluginManager(object):
    def __init__(self, app):
        #signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.plugin_helper = PluginHelper(app)

        # { 'name' -> plugin instance, ...}
        self.active_plugin_instances = self.load_active_plugin_instances()

        #self.plugin_change_event = multiprocessing.Event()
        #self.shutdown_event = multiprocessing.Event()
        #plugin_monitor = multiprocessing.Process(name='block', target=self.wait_for_event)
        #plugin_monitor.start()

    #def plugin_changed(self):
    #    self.plugin_change_event.set()

    #def shutdown_monitor(self):
    #    print "shutdown plugin monitor"
    #    self.shutdown_event.set()
    #    self.plugin_change_event.set()

    #def wait_for_event(self):
    #    """Wait for the event to be set before doing anything"""
    #    print 'plugin monitor started!'
    #
    #    while not self.shutdown_event.is_set():
    #        print "in wait loop"
    #        self.plugin_change_event.wait()
    #
    #        print "plugin change event received, will handle soon!"
    #        self.reload_active_plugin_instances()
    #        self.plugin_change_event.clear()
    #
    #    print 'go to the end'

    def load_active_plugin_instances(self):
        plugin_instances = multiprocessing.Manager().dict()

        active_name_list = self.plugin_helper.db_get_active_plugin_names()
        for plugin_name in active_name_list:
            plugin_instance = self.plugin_helper.new_plugin_instance(plugin_name)
            if plugin_instance:
                plugin_instances.update({plugin_name:plugin_instance})

        return plugin_instances

    def reload_active_plugin_instance(self, plugin_name):
        """
        Reload active plugin instance
        """
        self.remove_active_instance(plugin_name)
        self.add_active_instance(plugin_name)

    def add_active_instance(self, plugin_name):
        if plugin_name in self.active_plugin_instances.keys():
            print "Plugin instance: {0} already in memory!".format(plugin_name)
            return True

        plugin_instance = self.plugin_helper.new_plugin_instance(plugin_name)
        if not plugin_instance:
            print "Failed to get Plugin: {0} instance!".format(plugin_name)
            return False

        self.active_plugin_instances.update({plugin_name:plugin_instance})
        return True

    def remove_active_instance(self, plugin_name):
        if plugin_name not in self.active_plugin_instances.keys():
            print "Not found active instance: {0}".format(plugin_name)
            return True

        del self.active_plugin_instances[plugin_name]
        return True

    def find_plugin(self, recv):
        """
        Find the first matched active plugin, if all not matched, returns DummyPlugin
        """
        if not self.active_plugin_instances:
            return DummyPlugin()

        for plugin_instance in self.active_plugin_instances.values():
            if plugin_instance.is_matched(recv):
                return plugin_instance

        return DummyPlugin()

    def has_settings(self, plugin_name):
        plugin_instance = self.active_plugin_instances[plugin_name]
        if not plugin_instance:
            return False

        if not plugin_instance.config:
            return False

        return True

