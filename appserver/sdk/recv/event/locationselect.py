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

class WXMPRecvLocationselectEvent(WXMPRecvEvent):
    def __init__(self, core):
        super(WXMPRecvLocationselectEvent, self).__init__(core)
        self.type = RECV_EVENT_TYPE.LOCATION_SELECT

        self.event = self.meta.get('Event', None)
        if not self.event:
            raise Exception("Failed to initialize WXMPRecvLocationselectEvent because Event doesn't exist!")

        self.event_key = self.meta.get('EventKey', None)
        if not self.event_key:
            raise Exception("Failed to initialize WXMPRecvLocationselectEvent because EventKey doesn't exist!")

        # <SendLocationInfo>
        #      <Location_X>...</Location_X>
        #      <Location_Y>...</Location_Y>
        #      <Scale>...</Scale>
        #      <Label>...</Label>
        #      <Poiname>...</Poiname>
        # <//SendLocationInfo>
        sendlocation_info = self.meta.get('SendLocationInfo', None)
        if not sendlocation_info:
            raise Exception("Failed to initialize WXMPRecvLocationselectEvent because SendLocationInfo doesn't exist!")

        self.location_x = sendlocation_info.get('Location_X', None)
        if not self.location_x:
            raise Exception("Failed to initialize WXMPRecvLocationselectEvent because Location_X not in SendLocationInfo!")

        self.location_y = sendlocation_info.get('Location_Y', None)
        if not self.location_y:
            raise Exception("Failed to initialize WXMPRecvLocationselectEvent because Location_Y not in SendLocationInfo!")

        self.scale = sendlocation_info.get('Scale', None)
        if not self.scale:
            raise Exception("Failed to initialize WXMPRecvLocationselectEvent because Scale not in SendLocationInfo!")

        self.label = sendlocation_info.get('Label', None)
        if not self.label:
            raise Exception("Failed to initialize WXMPRecvLocationselectEvent because Label not in SendLocationInfo!")

        self.poiname = sendlocation_info.get('Poiname', None)
        if not self.poiname:
            raise Exception("Failed to initialize WXMPRecvLocationselectEvent because Poiname not in SendLocationInfo!")


    def debug(self):
        label = self.label
        if isinstance(label, unicode):
            label = label.encode('utf8')

        poiname = self.poiname
        if isinstance(poiname, unicode):
            poiname = poiname.encode('utf8')

        print "{0}(Event:{1}, EventKey:{2}, Location_X:{3}, Location_Y:{4}, Scale:{5}, Label:{6}, Poiname:{7})".format(
            self.__class__.__name__,  self.event, self.event_key,
            self.location_x, self.location_y, self.scale, label, poiname
        )

