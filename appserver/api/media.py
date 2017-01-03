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
import requests
from celery import shared_task, Task

@shared_task
def get_perm_count():
    """
    Get permanent media count
    """
    url = "https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token={0}".format(
        Task.app.get_access_token()
    )

    try:
        resp = requests.get(url).json()
    except Exception,e:
        print "Failed to get permanent media count from Weixin server because of:{0}".format(e)
        return False

    if not isinstance(resp, dict):
        print "Invalid response format when get permanent media count from Weixin server"
        return False

    if 'errcode' in resp.keys() and (resp['errcode'] != 0):
        print "Error response when get permanent media count from Weixin server: {0}".format(resp['errmsg'])
        return False

    return resp

@shared_task
def get_perm_list(type, offset, count):
    """
    Get permanent media list
    """
    url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={0}".format(
        Task.app.get_access_token()
    )

    allowed_types = ('image', 'video', 'voice', 'news')
    if type not in allowed_types:
        print "Invalid type, it must be one of {0}".format(allowed_types)
        return None

    count = int(count)
    if count < 1 and count >20:
        print "Invalid count, it must be in scope:[1,20], set to be 20."
        count = 20

    offset = int(offset)
    if offset < 0:
        print "Invalid offset, it must be larger than 0, set to be 0"
        offset = 0

    data = json.dumps({'type': type, 'offset': offset, 'count': count})
    try:
        resp = requests.post(url, data=data).json()
    except Exception,e:
        print "Failed to get permanent media list from Weixin server because of:{0}".format(e)
        return False

    if not isinstance(resp, dict):
        print "Invalid response format when get permanent media list from Weixin server"
        return False

    if resp['errcode'] != 0:
        print "Error response when get permanent media list from Weixin server: {0}".format(resp['errmsg'])
        return False

    return True
