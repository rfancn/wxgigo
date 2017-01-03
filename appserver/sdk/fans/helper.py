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
import requests
import json
from sdk.constants import WXMP_ACCESS_TOKEN, WXMP_FANS, WXMP_FANS_TEAM

class FansHelper(object):
    def __init__(self, db):
        self.db = db

    def get_fans_basic_info(self, open_id):
        access_token = self.db.hget(WXMP_ACCESS_TOKEN, 'access_token')
        if not access_token or not open_id:
            print "Failed to get access_token or open_id when in get_basic_info()"
            return None

        url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token={0}&openid={1}&lang=zh_CN".format(
            access_token, open_id
        )
        try:
            resp = requests.get(url)
            resp = json.loads(resp.content)
        except Exception,e:
            print "Failed to get basic user info because of: {0}".format(e)
            return None

        if not isinstance(resp, dict):
            print "Invalid response format when get basic user info from Weixin server"
            return None

        if 'errcode' in resp.keys() and (resp['errcode'] != 0):
            print "Error response when get basic user info from Weixin server: {0}".format(resp['errmsg'])
            return None

        return resp

    def save_fans(self, open_id):
        pass

