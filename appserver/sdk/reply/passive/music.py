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

from sdk.reply.base import WXMPPassiveReply
from sdk.reply import REPLY_PASSIVE_TYPE

XML_TEMPLATE = """
<xml>
<ToUserName><![CDATA[$to_username]]></ToUserName>
<FromUserName><![CDATA[$from_username]]></FromUserName>
<CreateTime>$create_time</CreateTime>
<MsgType><![CDATA[music]]></MsgType>
<Music>
<Title><![CDATA[$title]]></Title>
<Description><![CDATA[$description]]></Description>
<MusicUrl><![CDATA[$music_url]]></MusicUrl>
<HQMusicUrl><![CDATA[$hq_music_url]]></HQMusicUrl>
<ThumbMediaId><![CDATA[$media_id]]></ThumbMediaId>
</Music>
</xml>
"""
class WXMPPassiveReplyMusic(WXMPPassiveReply):
    def __init__(self, recv):
        super(WXMPPassiveReplyMusic, self).__init__(recv)
        self.type = REPLY_PASSIVE_TYPE.MUSIC

    def get_template(self):
        return XML_TEMPLATE

    def get_required_args(self):
        return ['media_id']



