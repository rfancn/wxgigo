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

class WXMPRecvScancodeEvent(WXMPRecvEvent):
    def __init__(self, core):
        super(WXMPRecvScancodeEvent, self).__init__(core)

        self.event = self.meta.get('Event', None)
        if not self.event:
            raise Exception("Failed to initialize WXMPRecvScancodeEvent because Event doesn't exist!")


        if self.event == "scancode_push":
            self.type = RECV_EVENT_TYPE.SCANCODE_PUSH
        elif self.event == "scancode_waitmsg":
            self.type = RECV_EVENT_TYPE.SCANCODE_WAITMSG

        self.event_key = self.meta.get('EventKey', None)
        if not self.event_key:
            raise Exception("Failed to initialize WXMPRecvScancodeEvent because EventKey doesn't exist!")

        # <ScanCodeInfo>
        #      <ScanType>...</ScanType>
        #      <ScanResult>...</ScanResult>
        # </ScanCodeInfo>
        scancode_info = self.meta.get('ScanCodeInfo', None)
        if not scancode_info:
            raise Exception("Failed to initialize WXMPRecvScancodeEvent because ScanCodeInfo doesn't exist!")

        self.scan_type = scancode_info.get('ScanType', None)
        if not self.scan_type:
            raise Exception("Failed to initialize WXMPRecvScancodeEvent because ScanType not in ScanCodeInfo !")

        self.scan_result = scancode_info.get('ScanResult', None)
        if not self.scan_result:
            raise Exception("Failed to initialize WXMPRecvScancodeEvent because ScanResult not in ScanCodeInfo !")

    def debug(self):
        print "{0}(Event:{1}, EventKey:{1}, ScanType:{2}, ScanResult:{3})".format(
            self.__class__.__name__,
            self.event, self.event_key,
            self.scan_type, self.scan_result)
