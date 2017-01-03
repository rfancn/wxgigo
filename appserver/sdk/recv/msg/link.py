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

class WXMPRecvLinkMsg(WXMPRecvMsg):
    def __init__(self, core):
        super(WXMPRecvLinkMsg, self).__init__(core)
        self.type = RECV_MSG_TYPE.LINK

        self.title = self.meta.get('Title', None)
        if not self.title:
            raise Exception("Failed to initialize WXMPRecvLinkMsg because Title doesn't exist!")

        self.description = self.meta.get('Description', None)
        if not self.description:
            raise Exception("Failed to initialize WXMPRecvLinkMsg because Description doesn't exist!")

        self.url = self.meta.get('Url', None)
        if not self.url:
            raise Exception("Failed to initialize WXMPRecvLinkMsg because Url doesn't exist!")

    def debug(self):
        print "{0}(Title:{1}, Description:{2}, Url:{3})".format(
            self.__class__.__name__,
            self.title.encode("utf8"),
            self.description.encode("utf8"),
            self.url)
