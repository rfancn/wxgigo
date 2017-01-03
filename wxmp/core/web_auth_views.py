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
import json
from urllib import urlencode, quote_plus
from urlparse import parse_qs, urlsplit, urlunsplit

from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic import View

logger = logging.getLogger(__name__)

from wxmp import celery_call

def web_user_info(request):
    """
    There are two way to get basic userinfo:
    1. via web access_token
    2. via system access_token

    This function will use web access_token, and call API: api.web.get_user_info
    """
    open_id = request.GET.get('open_id', None)
    if not open_id:
        logger.debug('Failed to get open_id from request in sns_user_info()')
        return HttpResponseBadRequest('Failed to find open_id in http request')

    user_info_dict = celery_call('api.web.get_user_info', (open_id,))
    return HttpResponse(json.dumps(user_info_dict), content_type="application/json")

def sys_user_info(request):
    """
    There are two way to get basic userinfo:
    1. via web access_token
    2. via system access_token

    This function will use system access_token, and call API: api.user.get_basic_info
    """
    open_id = request.GET.get('open_id', None)
    if not open_id:
        logger.debug('Failed to get open_id from request in sys_user_info()')
        return HttpResponseBadRequest('Failed to find open_id in http request')

    user_info_dict = celery_call('api.user.get_basic_info', (open_id,))
    return HttpResponse(json.dumps(user_info_dict), content_type="application/json")

class BaseWebView(View):
    def update_url_query_params(self, url, params_dict):
        """Given a URL, set or replace a query parameter and return the modified URL.

        e,g: set_query_parameter('http://example.com?foo=bar&biz=baz', 'foo', 'stuff')
        'http://example.com?foo=stuff&biz=baz'
        """
        scheme, netloc, path, query_string, fragment = urlsplit(url)
        query_params = parse_qs(query_string)

        query_params.update(params_dict)
        new_query_string = urlencode(query_params, doseq=True)

        return urlunsplit((scheme, netloc, path, new_query_string, fragment))

    def is_weixin_callback(self, request):
        """
        Check if this is the request comes from Weixin Servers callback
        """
        #if code and state are all in GET keys, then it is the callback of redirect_url
        if all(x in request.GET.keys() for x in ['code', 'state']):
            return True

        return False

    def get_next_url(self, request):
        """
        NOT USED BECAUSE OF:
        Fatal error here, it seems weixin browser turned off http_referer function,
        the way to use http_referer to get invoker's url doesn't work here.
        """
        next_url = request.GET.get('next_url', None)
        if not next_url:
            # if not explicitly specify next_url after authorization,use invoker's url
            next_url = request.META.get('HTTP_REFERER', None)
            logger.debug("Not explicitly specify next_url, use invoker's url: {0}".format(next_url))
            logger.debug('{0}'.format(request.META))

        return next_url

    def get_success_url(self, request, open_id):
        """
        Get the success url which need redirect to after authorization succeed
        """
        next_url = request.GET.get('next_url', None)
        if not next_url:
            return None

        success_url = self.update_url_query_params(next_url, {'open_id': open_id})
        return success_url

    def get_auth_url(self, request, scope):
        """
        Web authorization step1,
        check if next_url explicitly specified then get web authorization url
        next_url:   the url finally redirect to after web authorization succeed
        auth_url:   the web authorization url

        @return auth_url
        """
        # before issuing web authorization procedure,
        # make sure the next_url was passed by caller
        next_url = request.GET.get('next_url', None)
        if not next_url:
            logger.error("Failed to get next_url when start call Web Authorization")
            return None

        if scope not in ('snsapi_base', 'snsapi_userinfo'):
            logger.error("Invalid scope when call Web Authorization")
            return None

        redirect_url = request.build_absolute_uri()
        auth_url = celery_call('api.webauth.get_auth_url', (redirect_url,scope,))

        return auth_url

    def web_authorize(self, request):
        code = request.GET.get('code', None)
        if not code:
            logger.error("Failed to get code when doing Web Authorization!")
            return None

        open_id = celery_call('api.webauth.auth', (code,))
        if not open_id:
            logger.error("Failed to do Web Authorization.")
            return None

        return open_id

    def web_authorize_step1(self, request, scope):
        """
        Authorize step1 get an authorize url like:
        https://open.weixin.qq.com/connect/oauth2/authorize?
        appid=, redirect_uri=, response_type=code, scope=, state=, #wechat_redirect

        Now, we only get authorization url here in step1, no other operations
        """
        return self.get_auth_url(request, scope)

    def web_authorize_step2(self, request):
        """
        After step1, weixin server will callback redirect_url with (code, state) parameters
        """
        open_id = self.web_authorize(request)
        if not open_id:
            return None

        logger.debug("Web authorization succeed, open_id: {0}".format(open_id))
        return self.get_success_url(request, open_id)

class SnsBaseWebView(BaseWebView):
    def get(self, request, *args, **kwargs):
        logger.debug("in core.auth.sns_base")
        logger.debug("path is: {0}, get is:{1}".format(request.path, request.GET))

        # Step2: if code and state are all in GET keys, then it goes to step2
        if self.is_weixin_callback(request):
            success_url = self.web_authorize_step2(request)
            if not success_url:
                return HttpResponseBadRequest()

            logger.debug("After authorization, finally redirect to: {0}".format(success_url))
            return HttpResponseRedirect(success_url)

        # Step1: get authentication url and redirect to weixin server
        auth_url = self.web_authorize_step1(request, 'snsapi_base')
        if not auth_url:
            return HttpResponseBadRequest()

        return HttpResponseRedirect(auth_url)


class SnsUserinfoWebView(BaseWebView):
     def get(self, request, *args, **kwargs):
        """
        1. the first time enter WebAuth procedure,, save next_url
        2. then issue web auth step1, retrieve auth_url, and redirect to it
        3. weixin server will call redirect_url, here it is itself again with code, which triggers  web_auth_step2
        4. web_auth_step2 will get access_token if succeed, or return HttpResponseBadRequest
        5. finally, go to next_url with access_token
        """
        logger.debug("in core.auth.sns_userinfo")
        logger.debug("path is: {0}, get is:{1}".format(request.path, request.GET))

        # Step2: if code and state are all in GET keys, then it goes to step2
        if self.is_weixin_callback(request):
            success_url = self.web_authorize_step2(request)
            if not success_url:
                return HttpResponseBadRequest()

            logger.debug("After authorization, finally redirect to: {0}".format(success_url))
            return HttpResponseRedirect(success_url)

        # Step1: get authentication url and redirect to weixin server
        auth_url = self.web_authorize_step1(request, 'snsapi_userinfo')
        if not auth_url:
            return HttpResponseBadRequest()

        return HttpResponseRedirect(auth_url)

