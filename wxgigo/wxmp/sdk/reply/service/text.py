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
import json

from sdk.reply.base import WXMPServiceReply
from sdk.reply import REPLY_SERVICE_TYPE

class WXMPServiceReplyText(WXMPServiceReply):
    def __init__(self, recv):
        super(WXMPServiceReplyText, self).__init__(recv)
        self.type = REPLY_SERVICE_TYPE.TEXT

    def get_template(self):
        tmpl_dict = {
            "touser":"$to_username",
            "msgtype":"text",
            "text":{
                "content":"$content"
            }
        }

        return json.dumps(tmpl_dict)

    def get_required_args(self):
        return ['content']




