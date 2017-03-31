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
from sdk.recv.base import WXMPRecvEvent
from sdk.recv import RECV_EVENT_TYPE

class WXMPRecvScanEvent(WXMPRecvEvent):
    def __init__(self, core):
        super(WXMPRecvScanEvent, self).__init__(core)
        self.type = RECV_EVENT_TYPE.SCAN

        self.event = self.meta.get('Event', None)
        if not self.event:
            raise Exception("Failed to initialize WXMPRecvScanEvent because Event doesn't exist!")

        self.event_key = self.meta.get('EventKey', None)
        if not self.event_key:
            raise Exception("Failed to initialize WXMPRecvScanEvent because EventKey doesn't exist!")

        self.ticket = self.meta.get('Ticket', None)
        if not self.ticket:
            raise Exception("Failed to initialize WXMPRecvScanEvent because Ticket doesn't exist!")

    def debug(self):
        print "{0}(Event:{1}, EventKey:{2}, Ticket:{3})".format(
            self.__class__.__name__,
            self.event,
            self.event_key,
            self.ticket)
