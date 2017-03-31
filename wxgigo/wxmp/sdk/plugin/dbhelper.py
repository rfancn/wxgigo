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
import json

logger = logging.getLogger(__name__)

from sdk.constants import *

class DBPluginHelper(object):
    def __init__(self, app):
        super(DBPluginHelper, self).__init__(app)
        self.db = app.db

    def __save_meta_value(self, key, meta_value):
        """
        Save meta info into key hash
        """
        if not isinstance(meta_value, dict):
            print "Invalid meta value, it should be a dict"
            return False

        if 'name' not in meta_value.keys():
            print "Invalid meta value, it must contains name key"
            return False

        try:
            plugin_name = meta_value['name']
            self.db.hset(key, plugin_name, json.dumps(meta_value))
            self.db.save()
        except Exception,e:
            print "Failed to save plugin meta because of:{0}".format(e)
            return False

        return True

    def db_is_active(self, plugin_name):
        """
        Check if a plugin is activated or not, if it is activated,
        then it's name should be in "WXMP:PLUGINS:ACTIVE" hash table
        """
        return self.db.sismember(WXMP_PLUGINS_ACTIVE, plugin_name)

    def db_get_meta(self, plugin_name):
        """
        meta value is json serialized dict
        """
        stored = self.db.hget(WXMP_PLUGINS_META, plugin_name)
        if not stored:
            return None

        return json.loads(stored)

    def db_get_meta_keys(self):
        return self.db.hkeys(WXMP_PLUGINS_META)

    def db_get_meta_all(self):
        kv_list = self.db.hgetall(WXMP_PLUGINS_META)

        meta_list = []
        for k,v in kv_list.items():
            meta_list.append(json.loads(v))

        return meta_list

    def db_save_meta(self, meta_value):
        """
        Save meta information into db to avoid importing modules from filesystem time by time
        """
        return self.__save_meta_value(WXMP_PLUGINS_META, meta_value)

    def db_save_active_name(self, plugin_name):
        """
        Save all activated plugins's name into WXMP:PLUGINS:ACTIVATED table
        """
        try:
            self.db.sadd(WXMP_PLUGINS_ACTIVE, plugin_name)
        except Exception,e:
            print "Faild save activated plugin's name into db"
            return False

        return True

    def db_remove_inactive_name(self, plugin_name):
        """
        Remove deactivated plugins's name from WXMP:PLUGINS:ACTIVE table
        """
        try:
            self.db.srem(WXMP_PLUGINS_ACTIVE, plugin_name)
        except Exception,e:
            print "Faild save activated plugin's name into db"
            return False

        return True

    def db_get_active_plugin_names(self):
        return self.db.smembers(WXMP_PLUGINS_ACTIVE)


    def db_get_config_settings(self, plugin_name):
        settings = self.db.hget(WXMP_PLUGINS_CONF, plugin_name)
        if not settings:
            return None

        return json.loads(settings)

    def db_save_config_settings(self, plugin_name, settings):
        try:
            self.db.hset(WXMP_PLUGINS_CONF, plugin_name, json.dumps(settings))
            self.db.save()
        except Exception,e:
            print "Failed to save plugin config settings because of:{0}".format(e)
            return False

        return True

