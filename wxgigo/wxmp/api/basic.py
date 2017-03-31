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
import logging
logger = logging.getLogger(__name__)
import requests
import time

from celery import shared_task, Task
from sdk.constants import WXMP_CONFIG, WXMP_ACCESS_TOKEN

class update_access_token(Task):
    def __init__(self):
        # set expire threshold to be 10 minutes
        self.expire_threshold = 600
        self.db = self.app.db

    def __update_access_token(self):
        app_id, app_key = self.db.hmget(WXMP_CONFIG, 'APP_ID', 'APP_KEY')

        if not app_id or not app_key:
            print "No APP configuration!"
            return False

        url = "https://api.weixin.qq.com/cgi-bin/token" \
            "?grant_type=client_credential" \
            "&appid={APP_ID}&secret={APP_KEY}".format(APP_ID=app_id, APP_KEY=app_key)

        try:
            resp = requests.get(url).json()
        except Exception,e:
            print "Failed to get access token from Weixin server because of:{0}".format(e)
            return False

        if not isinstance(resp, dict):
            print "Invalid response format from Weixin server"
            return False

        if "access_token" not in resp.keys():
            print "Error response from Weixin server: {0}".format(resp)
            return False

        expire_timestamp = int(time.time()) + resp['expires_in']
        save_dict = {'access_token': resp['access_token'], 'expire_timestamp': expire_timestamp}
        self.db.hmset(WXMP_ACCESS_TOKEN, save_dict)
        self.db.save()
        return True

    def __is_access_token_expire_soon(self, expire_timestamp):
        # try convert it to integer anyway
        try:
            expire_timestamp = int(expire_timestamp)
        except:
            pass

        current_timestamp = int(time.time())
        if (expire_timestamp - current_timestamp) < self.expire_threshold:
            print "Access token will be expired in {0} seconds".format(expire_timestamp - current_timestamp)
            return True

        return False

    def run(self):
        """
        Centerilized access token update function
        """
        access_token, expire_timestamp = self.db.hmget(WXMP_ACCESS_TOKEN, 'access_token', 'expire_timestamp')
        if not expire_timestamp:
            # if no expire_timestamp, then it should be the first time update
            print "The First time access token updating..."
            if not self.__update_access_token():
                print "Failed to update access token"
                return False
            else:
                print "Successfully updated access token!"
                return True

        # else if exist expire_timestamp, check if it will be expired soon or not
        will_token_expire_soon = self.__is_access_token_expire_soon(expire_timestamp)
        if not will_token_expire_soon:
            print "Check access token is still valid, skip updating!"
            return True
        else:
            print "Detect access token will be expired soon, updating it..."
            if not self.__update_access_token():
                print "Failed to update access token"
                return False
            else:
                print "Successfully updated access token!"
                return True

@shared_task
def get_weixin_server_iplist():
    """
    Get valid weixin server ip list
    """
    access_token = Task.app.get_access_token()
    if not access_token:
        print "Failed to get access token"
        return None

    url = "https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token={access_token}".format(
        access_token = access_token
    )

    try:
        resp = requests.get(url).json()
    except Exception,e:
        print "Failed to get Weixin server IP because of:{0}".format(e)
        return False


    if not isinstance(resp, dict):
        print "Invalid response format from Weixin server"
        return False

    if "ip_list" not in resp.keys():
        print "Error response from Weixin server: {0}".format(resp)
        return False

    ip_list = resp['ip_list']
    return ip_list

@shared_task
def get_access_token():
    return  Task.app.get_access_token()