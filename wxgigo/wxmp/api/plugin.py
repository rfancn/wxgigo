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
from celery import Task

logger = logging.getLogger(__name__)

class BaseMeta(Task):
    abstract = True
    plugin_manager = Task.app.plugin_manager
    plugin_helper = Task.app.plugin_manager.plugin_helper

class save(BaseMeta):
    def get_settings_dict(self, settings_name, http_post):
        """
        As post data assembly setting values as format:
        { settings[wp_username] : xxxx },
        need extract all setting field and it's value and assembly as a dict

        @param settings_name is the POST settings value name
        @param http_post is http request post dict
        """
        settings = {}

        # prefix which indicate setting post key matched
        settings_prefix = settings_name + '['
        # Later will extract real key(xxx) from 'settings_name[xxx]',
        # e,g: if settings_name is 'settings',
        # then start extract start position would be len('settings[')
        start_pos = len(settings_prefix)
        for k in http_post.keys():
            if k.startswith(settings_prefix):
                # -1 means ignore the last ']'
                real_key = k[start_pos:-1]
                value = http_post.get(k, None)
                if not value:
                    settings[real_key] = None
                else:
                    settings[real_key] = value

        return settings

    def active_plugin(self, plugin_name):
        """
        when active plugin, it do following things:
        1. if plugin info not stores in db, save it's meta info into db
        2. add plugin's name to WXMP:PLUGINS:ACTIVE db table
        """
        print "Active plugin:{0}".format(plugin_name)

        db_meta_dict = self.plugin_helper.db_get_meta(plugin_name)
        # if no meta info for this plugin in db, store it
        if not db_meta_dict:
            print "It is the first time active plugin, store it to db."
            fs_meta_dict = self.plugin_helper.fs_get_meta(plugin_name)
            if not self.plugin_helper.db_save_meta(fs_meta_dict):
                print "Failed save basic meta info!"
                return False

        if not self.plugin_helper.db_save_active_name(plugin_name):
            print "Failed to save active plugin name into db"
            return False

        return self.plugin_manager.add_active_instance(plugin_name)

    def deactive_plugin(self, plugin_name):
        print "Deactive plugin:{0}".format(plugin_name)

        db_meta_dict = self.plugin_helper.db_get_meta(plugin_name)
        if not db_meta_dict:
            print "Something bad happend, no db meta info for: {0}".format(plugin_name)
            return self.plugin_helper.db_remove_inactive_name(plugin_name)

        print "Plugin meta info already in db, deactive it!"
        if not self.plugin_helper.db_remove_inactive_name(plugin_name):
            print "Failed to remove inactive plugin name from db"
            return False

        return self.plugin_manager.remove_active_instance(plugin_name)

    def config_plugin(self, plugin_name, settings):
        print "Config plugin:{0}".format(plugin_name)

        if not self.plugin_helper.db_save_config_settings(plugin_name, settings):
            print "Failed to save plugin config settingss to db"
            return False

        self.plugin_manager.reload_active_plugin_instance(plugin_name)

        return True

    def run(self, http_post):
        """
        Recv should be a dictionary with below format:
        {  'action': 'active', 'name': 'xxxx' }
        """
        if not isinstance(http_post, dict):
            print "Invalid receive format: it should be a dict"
            return False

        action = http_post.get('action', None)
        name = http_post.get('name', None)
        if not action or not name:
            print "Invalid receive format: no action or name"
            return False

        action = action.strip().lower()
        if action == 'active':
            return self.active_plugin(name)
        elif action == 'deactive':
            return self.deactive_plugin(name)
        elif action == 'config':
            settings = self.get_settings_dict('settings', http_post)
            return self.config_plugin(name, settings)

        return True

class load_meta(BaseMeta):
    def run(self):
        """
        WXMP Plugin Meta Info stored in db as hash type like below:
        'WXMP:PLUGINS:META'-> {
        '<name1>': {'name1': 'xxx1', 'version': 'yyy1'...},
        '<name2>': {'name2': 'xxx2', 'version': 'yyy2'...},
        ...
        }

        @return   [{'name1': 'xxx1', 'version': 'yyy1'...}, ...]
        """
        meta_dict_list = []

        fs_meta_list = self.plugin_helper.fs_get_meta_all()
        for meta_dict in fs_meta_list:
            plugin_name = meta_dict['name']
            meta_dict['enabled'] = self.plugin_helper.db_is_active(plugin_name)

            # as settings only works when plugin is enabled
            # so if the plugin name is not in active plugin instances dict keys
            # we don't need set the 'has_settings' meta info
            if plugin_name in self.plugin_manager.active_plugin_instances.keys():
                meta_dict['has_settings'] = self.plugin_manager.has_settings(plugin_name)

            meta_dict_list.append(meta_dict)

        return meta_dict_list

class load_config(BaseMeta):
    """
    WXMP:PLUGIN:CONFIG

    @returns:
    [
       'Group 1': [  filed1_dict, filed2_dict, ... ]
       'Group 2': [  filed1_dict, filed2_dict, ... ]
    ]
    """
    def run(self, plugin_name):
        plugin_instance  = self.plugin_manager.active_plugin_instances[plugin_name]
        if not plugin_instance:
            return []

        if not plugin_instance.config:
            return []

        return plugin_instance.config.dumps()