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
import time
import json
from sdk.constants import *

class WebHelper(object):
    def __init__(self, db):
        self.db = db

    def save_auth_info(self, auth_info):
        if not auth_info or not isinstance(auth_info, dict):
            print "Invalid web authentication info"
            return False

        try:
            # add expire_timestamp here
            auth_info['expire_timestamp'] = int(time.time()) + auth_info['expires_in']
            self.db.hset(WXMP_WEB_ACCESS_TOKEN, auth_info['openid'], json.dumps(auth_info))
            self.db.save()
        except Exception,e:
            print "Failed to save web authentication info because of:{0}".format(e)
            return False

        print "Successfully save web authentication info"
        return True

    def get_auth_info(self, open_id):
        auth_info = self.db.hget(WXMP_WEB_ACCESS_TOKEN, open_id)
        if not auth_info:
            print "No web authentication info."
            return None

        return json.loads(auth_info)

    def get_access_token(self, open_id):
        auth_info = self.get_auth_info(open_id)

        try:
            access_token = auth_info['access_token']
            expire_timestamp = auth_info['expire_timestamp']
        except Exception,e:
            print "Failed to get access_token and expire_timestamp from db auth_info"
            return None

        # if access_token expired, return None
        current_timestamp = int(time.time())
        if expire_timestamp < current_timestamp:
            print "web access token expired, expire_timestamp:{0}, current_timestamp:{1}".format(
                expire_timestamp, current_timestamp
            )
            return None

        return access_token

    def get_api_scope(self, open_id):
        auth_info = self.get_auth_info(open_id)
        try:
            scope = auth_info['scope']
        except Exception,e:
            print "Failed to get Api scope from db auth_info"
            return None

        return scope

    def get_refresh_token(self, open_id):
        auth_info = self.get_auth_info(open_id)

        try:
            refresh_token = auth_info['refresh_token']
        except Exception,e:
            print "Failed to get web refresh token because of:{0}".format(e)
            return None

        return refresh_token



