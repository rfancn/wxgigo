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
import sys
logger = logging.getLogger(__name__)

import xmltodict

from sdk.recv.base import WXMPRecvCore
from sdk.recv import RECV_CATEGORY, RECV_EVENT_TYPE
from sdk.utils import load_class

#############################################################
# Recv Message Factory Classes
#############################################################
class WXMPRecvMsgFactory(object):
    def __init__(self, core):
        self.core = core

    def create(self):
        module_path = "sdk.recv.msg.{0}".format(self.core.msg_type)
        class_name = "WXMPRecv{0}Msg".format(self.core.msg_type.title())
        try:
            cls = load_class(module_path, class_name)
        except Exception,e:
            logger.error("Failed to load class:%s from:%s" % (class_name, module_path), exc_info=1)
            return None

        return cls(self.core)

class WXMPRecvEventFactory(object):
    def __init__(self, core):
        self.core = core

    def get_event_type(self):
        event_type = None

        event = self.core.meta.get('Event', None).lower()
        event_key = self.core.meta.get("EventKey", None)
        if event == "subscribe":
            if event_key is None:
                event_type = "follow"
            else:
                event_type = "scan"
        elif event == "unsubscribe":
            event_type = "follow"
        elif event == "location":
            event_type = "location"
        elif event == "scan":
            event_type = "scan"
        elif event == "TEMPLATESENDJOBFINISH":
            event_type = "template"
        # http://mp.weixin.qq.com/wiki/10/0234e39a2025342c17a7d23595c6b40a.html
        # event triggered when click scancode_* type menu item
        elif event in ("click", "view"):
            event_type = "menu"
        elif event.startswith("scancode_"):
            event_type = "scancode"
        elif event == 'location_select':
            event_type = 'locationselect'
        elif event.startswith('pic_'):
            event_type = 'pic'

        return event_type

    def create(self):
        event_type =  self.get_event_type()
        if not event_type:
            raise Exception("Failed to get receive event's type!")

        module_path = "sdk.recv.event.{0}".format(event_type)
        class_name = "WXMPRecv{0}Event".format(event_type.title())
        try:
            cls = load_class(module_path, class_name)
        except Exception,e:
            raise Exception("Failed to load class:%s from:%s" % (class_name, module_path))

        return cls(self.core)

class WXMPRecvFactory(object):
    def __init__(self, body):
        try:
            self.recv_dict = xmltodict.parse(body)['xml']
        except Exception,e:
            raise Exception("Failed to initialize WXMPRecvManager while parsing http request: %s" % e)

        logger.debug(self.recv_dict)

    def create(self):
        recv_core = WXMPRecvCore(self.recv_dict)

        # create base recv object
        if recv_core.category == RECV_CATEGORY.UNKNOWN:
            raise Exception("Failed to create receive object because get UNKNOWN message type!")

        if recv_core.category == RECV_CATEGORY.MESSAGE:
            factory = WXMPRecvMsgFactory(recv_core)
        elif recv_core.category == RECV_CATEGORY.EVENT:
            factory = WXMPRecvEventFactory(recv_core)

        return factory.create()