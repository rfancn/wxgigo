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
def get():
    url = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token={0}".format(
        Task.app.get_access_token()
    )

    try:
        resp = requests.get(url).json()
    except Exception,e:
        print "Failed to get menu info from Weixin server because of:{0}".format(e)
        return {}

    if not isinstance(resp, dict):
        print "Invalid response format when get menu info from Weixin server"
        return {}

    if 'errcode' in resp.keys() and (resp['errcode'] != 0):
        print "Error response when get menu info from Weixin server: {0}".format(resp['errmsg'])
        return {}

    return resp

@shared_task
def delete():
    url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token={0}".format(
        Task.app.get_access_token()
    )

    try:
        resp = requests.post(url).json()
    except Exception,e:
        print "Failed to delete menu in Weixin server because of:{0}".format(e)
        return False

    if not isinstance(resp, dict):
        print "Invalid response format when delete menu in Weixin server"
        return False

    if resp['errcode'] != 0:
        print "Error response when delete menu in Weixin server: {0}".format(resp['errmsg'])
        return False

    return True


@shared_task
def create(menu_config):
    """
    @menu_config:  dict of menu configuration
    """
    if not isinstance(menu_config, dict) and 'button' not in menu_config.keys():
        print "Invalid menu information when create menu in Weixin server"
        return False

    url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token={0}".format(
        Task.app.get_access_token()
    )

    try:
        # If there does exist Chinese text in menu_info, it need dumps as following:
        # json.dumps(menu_info, ensure_ascii=False).encode('utf8')
        data = json.dumps(menu_config, ensure_ascii=False).encode('utf8')
        resp = requests.post(url, data=data).json()
    except Exception,e:
        print "Failed to create menu in Weixin server because of:{0}".format(e)
        return False

    if not isinstance(resp, dict):
        print "Invalid response format when create menu in Weixin server"
        return False

    if resp['errcode'] != 0:
        print "Error response when create menu in Weixin server: {0}".format(resp['errmsg'])
        return False

    return True