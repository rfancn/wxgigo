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

class MENU_TYPE:
    CLICK = 'click'
    VIEW = 'view'
    SCANCODE_PUSH = 'scancode_push'
    SCANCODE_WAITMSG = 'scancode_waitmsg'
    PIC_SYSPHOTO = 'pic_sysphoto'
    PIC_PHOTO_OR_ALBUM = 'pic_photo_or_album'
    PIC_WEIXIN = 'pic_weixin'
    LOCATION_SELECT = 'location_select'
    MEDIA_ID = 'media_id'
    VIEW_LIMITED = 'view_limited'


class BaseMenu(object):
    def validate(self):
        raise NotImplementedError

    def to_dict(self):
        raise NotImplementedError

class MenuItem(BaseMenu):
    def __init__(self, name, type, **kwargs):
        self.name = name
        self.type = type

        for k,v in kwargs.items():
            self.__dict__[k] = v

    def validate(self):
        if len(self.name) > 40:
            print 'Menu name cannot exceeds 40'
            return False

        if self.type == MENU_TYPE.VIEW:
            if 'url' not in self.__dict__.keys():
                return False
            elif len(self.__dict__['url']) > 1024:
                return False
        elif self.type in (MENU_TYPE.MEDIA_ID, MENU_TYPE.VIEW_LIMITED):
            if 'media_id' not in self.__dict__.keys():
                return False
        else:
            if 'key' not in self.__dict__.keys():
                return False
            # key value cannot larger than 128
            elif len(self.__dict__['key']) > 128:
                return False

        return True

    def to_dict(self):
        d = {}
        for k,v in self.__dict__.items():
            if not k.startswith('__') and not callable(v) and not type(v) is staticmethod:
                d[k] = v

        return d

class SubMenu(BaseMenu):
    def __init__(self, name, menu_item_list=None):
        self.name = name

        self.menu_item_list = menu_item_list
        if not menu_item_list:
            self.menu_item_list = []

    def add(self, *args):
        for m in args:
            if not isinstance(m, MenuItem):
                raise Exception('Only MenuItem can be added.')
            self.menu_item_list.append(m)

    def validate(self):
        if len(self.name) > 16:
            print 'Menu name cannot exceeds 16'
            return False

        if len(self.menu_item_list) > 5:
            print 'More than 5 menu item in sub menu.'
            return False

        return True

    def to_dict(self):
        submenu_dict = {'name': self.name, 'sub_button': []}
        for m in self.menu_item_list:
            submenu_dict['sub_button'].append(m.to_dict())
        return submenu_dict

class MenuConfig(object):
    def __init__(self):
        self.config = []

    def add(self, *args):
        if len(args) > 3:
            raise Exception("No more than 3 top menu allowed")

        for m in args:
            if not m.validate():
                raise Exception("Invalid menu or menuitem.")

            self.config.append(m)

    def to_dict(self):
        config_dict = {'button': []}
        for m in self.config:
            config_dict['button'].append(m.to_dict())
        return config_dict
