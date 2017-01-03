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

class BasePluginConfig(object):
    def loads(self, settings):
        """
        Read config stuff from db and set to attributes
        """
        if not settings:
            return

        for k,v in self.__class__.__dict__.items():
            if not k.startswith('__') and not callable(v) and not type(v) is staticmethod:
                # try to set attribute of plugin_config to what we get from db
                try:
                    self.__dict__[k] = settings[k]
                except:
                    self.__dict__[k] = None

    def dumps(self):
        """
        Dump sorted and grouped field list
        """
        # build a field dict, like 'username' -> { 'label': 'xxx', 'help_text': 'yyy', ...}
        field_dict = {}
        # find normal (field_name, field attributes) in class's __dict__
        for k, v in self.__class__.__dict__.items():
            # only below matched are normal field
            if not k.startswith('__') and not callable(v) and not type(v) is staticmethod:
                field_attributes = v.to_dict()
                # IMPORTANT: we add 'value' attribute here
                # as loads() function already executed when plugin initialize in plugin_helper
                # which means plugin_config.field_name already set the value loads from db
                # self.__dict__[k] = self.__dict__[field_name], e,g: it equals to plugin_config.wp_username
                try:
                    field_attributes['value'] = self.__dict__[k]
                except:
                    field_attributes['value'] = None

                field_dict[k] = field_attributes

        config_list = []
        # if concrete plugin_config instance not implement get_layout() function, returns
        # [
        #   '': [ field1, filed2, ... ]
        # ]
        # here, filed1 is a dict { field name : filed attributes }
        layout =  self.get_layout()
        if not layout:
            group_name = ''
            field_list = []
            for k,v in field_dict.items():
                field_list.append({k:v})
            config_list.append({group_name: field_list})
            return config_list

        # if get_layout() has been implemented in concrete plugin_config instance
        # need sort the
        for group_dict in layout:
            for group_name, field_name_list in group_dict.items():
                field_list = []
                for field_name in field_name_list:
                    field_list.append({field_name:field_dict[field_name]})
                config_list.append({group_name: field_list})
        return config_list

    def get_layout(self):
        """
        Returns layout which shows in plugin->settings in admin GUI
        """
        print 'in parent'
        return None

class Field(object):
    def __init__(self, *args, **kwargs):
        self.required = True

    def to_dict(self):
        return self.__dict__.copy()

class CharField(Field):
    def __init__(self, label, default=None, help_text=None, secure = False, *args, **kwargs):
        super(CharField, self).__init__(*args, **kwargs)
        self.type = "text"

        self.label = label
        self.default = None
        self.help_text = help_text
        # if input box shows as password style or not
        self.secure = secure

class ChoiceField(Field):
    def __init__(self, label, choices, default, help_text=None, *args, **kwargs):
        super(ChoiceField, self).__init__(*args, **kwargs)
        self.type = "choice"

        self.label = label
        self.choices = choices
        self.default = None
        self.help_text = help_text




