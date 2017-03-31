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
import urllib
from celery import shared_task, Task

from sdk.constants import *
from sdk.web.helper import WebHelper

class BaseWeb(Task):
    abstract = True
    web_helper = WebHelper(Task.app.db)
    app_id, app_key = Task.app.db.hmget(WXMP_CONFIG, 'APP_ID', 'APP_KEY')

#class get_access_token(BaseWeb):
#    def run(self, open_id):
#        return self.web_helper.get_access_token(open_id)

class auth(BaseWeb):
    """
    Authorization to obtain web access token

    @param:   code
    @return:  if succeed, returns openid
    """
    def run(self, code):
        if not self.app_id or not self.app_key:
            print "No app_id or app_key when doing web authentication"
            return None

        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?' \
              'appid={0}&secret={1}&code={2}&' \
              'grant_type=authorization_code'.format(self.app_id, self.app_key, code)

        try:
            resp = requests.get(url).json()
        except Exception,e:
            print "Failed to do web authentication because of:{0}".format(e)
            return None

        if not isinstance(resp, dict):
            print "Invalid response format when do web authentication"
            return None

        if 'errcode' in resp.keys() and (resp['errcode'] != 0):
            print "Error response when do web authentication: {0}".format(resp['errmsg'])
            return None

        if not self.web_helper.save_auth_info(resp):
            return None

        return resp['openid']

class get_auth_url(BaseWeb):
    def run(self, redirect_url, scope):
         if not self.app_id:
             print "Failed to get app_id in get_auth_url()"
             return None

         auth_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?' \
                    'appid={0}&redirect_uri={1}&response_type=code' \
                    '&scope={2}#wechat_redirect'.format(self.app_id, urllib.quote_plus(redirect_url), scope)

         return auth_url

class get_user_info(BaseWeb):
    def refresh_access_token(self, open_id):
        if not self.app_id:
            print "Failed to get app_id when refresh web access token"
            return None

        refresh_token = self.web_helper.get_refresh_token(open_id)
        if not refresh_token:
            return None

        url = 'https://api.weixin.qq.com/sns/oauth2/refresh_token?' \
            'appid={0}&grant_type=refresh_token&refresh_token={1}'.format(
            self.app_id, refresh_token
        )

        try:
            resp = requests.get(url).json()
        except Exception,e:
            print "Failed to get refresh web access token because of:{0}".format(e)
            return None

        if not isinstance(resp, dict):
            print "Invalid response format when refresh web access token"
            return None

        if 'errcode' in resp.keys() and (resp['errcode'] != 0):
            print "Error response when refresh web access token: {0}".format(resp['errmsg'])
            return None

        # resp is a authentication info dict contains following:
        #
        # {
        # "access_token":"ACCESS_TOKEN",
        # "expires_in":7200,
        # "refresh_token":"REFRESH_TOKEN",
        # "openid":"OPENID",
        # "scope":"SCOPE"
        # }
        if not self.web_helper.save_auth_info(resp):
            return None

        return resp['access_token']

    def run(self, open_id):
        access_token = self.web_helper.get_access_token(open_id)
        # first time check if we can get valid access_token from db
        if not access_token:
            # may be access_token expired, try refresh it
            print "Failed to get valid access_token from db, try to refresh it..."
            access_token = self.refresh_access_token(open_id)

        # second time check after refresh
        if not access_token:
            print "Failed to get access_token after refresh"
            return None

        url = 'https://api.weixin.qq.com/sns/userinfo?' \
              'access_token={0}&openid={1}&lang=zh_CN'.format(access_token, open_id)

        try:
            resp = requests.get(url)
            # Important: Must not use requests.response.json() method here
            # otherwise, requests will doing ascii encode against the unicode string
            resp = json.loads(resp.content)
        except Exception,e:
            print "Failed to get userinfo because of:{0}".format(e)
            return None

        if not isinstance(resp, dict):
            print "Invalid response format when get userinfo from Weixin server"
            return None

        if 'errcode' in resp.keys() and (resp['errcode'] != 0):
            print "Error response when get userinfo info from Weixin server: {0}".format(resp['errmsg'])
            return None

        return resp