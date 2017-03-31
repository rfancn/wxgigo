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
from sdk.recv.base import WXMPRecvMsg
from sdk.recv import RECV_MSG_TYPE

class WXMPRecvLocationMsg(WXMPRecvMsg):
    def __init__(self, core):
        super(WXMPRecvLocationMsg, self).__init__(core)
        self.type = RECV_MSG_TYPE.LOCATION

        self.location_x = self.meta.get('Location_X', None)
        if not self.location_x:
            raise Exception("Failed to initialize WXMPRecvLocationMsg because Location_X doesn't exist!")

        self.location_y = self.meta.get('Location_Y', None)
        if not self.location_y:
            raise Exception("Failed to initialize WXMPRecvLocationMsg because Location_Y doesn't exist!")

        self.scale = self.meta.get('Scale', None)
        if not self.scale:
            raise Exception("Failed to initialize WXMPRecvLocationMsg because Scale doesn't exist!")

        self.label = self.meta.get('Label', None)
        if not self.scale:
            raise Exception("Failed to initialize WXMPRecvLocationMsg because Label doesn't exist!")

    def debug(self):
        print "{0}(Location_X:{1}, Location_Y:{2}, Scale:{3}, Label:{4})".format(
            self.__class__.__name__,
            self.location_x,
            self.location_y,
            self.scale,
            self.label.encode("utf8"))