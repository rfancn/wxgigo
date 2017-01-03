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

class WXMPRecvPicEvent(WXMPRecvEvent):
    def __init__(self, core):
        super(WXMPRecvPicEvent, self).__init__(core)

        self.event = self.meta.get('Event', None)
        if not self.event:
            raise Exception("Failed to initialize WXMPRecvPicEvent because Event doesn't exist!")

        if self.event == "pic_sysphoto":
            self.type = RECV_EVENT_TYPE.PIC_SYSPHOTO
        elif self.event == "pic_photo_or_album":
            self.type = RECV_EVENT_TYPE.PIC_PHOTO_OR_ALBUM
        elif self.event == "pic_weixin":
            self.type = RECV_EVENT_TYPE.PIC_WEIXIN

        self.event_key = self.meta.get('EventKey', None)
        if not self.event_key:
            raise Exception("Failed to initialize WXMPRecvPicEvent because EventKey doesn't exist!")

        # <SendPicsInfo>
        #      <Count>...</Count>
        #      <PicList>
        #          <item><PicMd5Sum>....</PicMd5Sum></item>
        #           ...
        #      </PicList>
        # </SendPicsInfo>
        sendpic_info = self.meta.get('SendPicsInfo', None)
        if not sendpic_info:
            raise Exception("Failed to initialize WXMPRecvPicEvent because SendPicsInfo doesn't exist!")

        self.count = sendpic_info.get('Count', None)
        if not self.count:
            raise Exception("Failed to initialize WXMPRecvPicEvent because Count not in SendPicsInfo !")

    def debug(self):
        print "{0}(Event:{1}, EventKey:{2}, PicCount:{3})".format(
            self.__class__.__name__,
            self.event, self.event_key, self.count)
