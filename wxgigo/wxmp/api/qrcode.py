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
from celery import shared_task, Task
from sdk.constants import WXMP_CONFIG, WXMP_ACCESS_TOKEN

@shared_task
def get_temp_ticket(scene_id, expire_seconds=180):
    # trick way to do sanity check against scene_id
    try:
        scene_id = int(scene_id)
        expire_seconds = int(expire_seconds)
    except:
        print "Invalid scene_id or expire_seconds, it must integer"
        return None

    if scene_id <= 0 or scene_id > 2147483647:
        print "Invalid scene_id, it must be in [1, 2147483647]"
        return None

    if expire_seconds <= 0 or expire_seconds > 2592000:
        print "Invalid expire_seconds, it must be in [1, 2592000]"
        return None

    access_token = Task.app.get_access_token()
    if not access_token:
        print "Failed to get access_token"
        return None

    data = {
        "expire_seconds": expire_seconds,
        "action_name": "QR_SCENE",
        "action_info": {
            "scene": {"scene_id": scene_id}
        }
    }
    url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={0}'.format(access_token)
    try:
        resp = requests.post(url, data).json()
    except Exception,e:
        print "Failed to get temporary QRCode ticket because of:{0}".format(e)
        return None

    if not isinstance(resp, dict):
        print "Invalid response format when get temporary QRCode ticket from Weixin server"
        return None

    if 'errcode' in resp.keys() and (resp['errcode'] != 0):
        print "Error response when get temporary QRCode ticket from Weixin server: {0}".format(resp['errmsg'])
        return None

    return resp['ticket']

@shared_task
def get_limit_str_ticket(scene_str):
    len_scene_str = len(scene_str)
    if len_scene_str < 1 or len_scene_str > 64:
        print "Invalid scene_str, it's length should be in [1, 64]"
        return None

    access_token = Task.app.get_access_token()
    if not access_token:
        print "Failed to get access_token"
        return None

    data = {
        "action_name": "QR_LIMIT_STR_SCENE",
        "action_info": {
            "scene": {"scene_str": scene_str}
        }
    }
    url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={0}'.format(access_token)
    try:
        resp = requests.post(url, json.dumps(data)).json()
    except Exception,e:
        print "Failed to get limit String QRCode ticket because of:{0}".format(e)
        return None

    if not isinstance(resp, dict):
        print "Invalid response format when get limit String QRCode ticket from Weixin server"
        return None

    if 'errcode' in resp.keys() and (resp['errcode'] != 0):
        print "Error response when get limit String QRCode ticket from Weixin server: {0}".format(resp['errmsg'])
        return None

    return resp['ticket']

@shared_task
def get_limit_ticket(scene_id):
    """
    @scene_id:   integer scene_id
    """
    try:
        scene_id = int(scene_id)
    except:
        print "Invalid scene_id or expire_seconds, it must integer"
        return None

    if scene_id <= 0 or scene_id > 100000:
        print "Invalid scene_id, it must be in [1, 100000]"
        return None

    access_token = Task.app.get_access_token()
    if not access_token:
        print "Failed to get access_token"
        return None

    data = {
        "action_name": "QR_LIMIT_SCENE",
        "action_info": {
            "scene": {"scene_id": scene_id}
        }
    }
    url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={0}'.format(access_token)
    try:
        resp = requests.post(url, data).json()
    except Exception,e:
        print "Failed to get limit QRCode ticket because of:{0}".format(e)
        return None

    if not isinstance(resp, dict):
        print "Invalid response format when get limit QRCode ticket from Weixin server"
        return None

    if 'errcode' in resp.keys() and (resp['errcode'] != 0):
        print "Error response when get limit QRCode ticket from Weixin server: {0}".format(resp['errmsg'])
        return None

    return resp['ticket']

