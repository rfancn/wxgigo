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
import logging

from django.http import HttpResponse
from django.views.generic import View, TemplateView

from contrib.admin import celery_call

logger = logging.getLogger(__name__)

class WXMPPluginActionView(View):
    EMPTY_RESULT = HttpResponse(json.dumps(None), content_type="application/json")

    def get_meta(self):
        plugins_meta_list = celery_call('api.plugin.load_meta')
        if not isinstance(plugins_meta_list, list):
            logger.debug(plugins_meta_list)
            raise Exception("Failed to load plugin meta list!")

        return HttpResponse(json.dumps(plugins_meta_list), content_type="application/json")

    def get_config(self, plugin_name):
        config_list = celery_call('api.plugin.load_config', (plugin_name,))
        if not isinstance(config_list, list):
            logger.debug(config_list)
            raise Exception("Failed to load plugin config list!")

        return HttpResponse(json.dumps(config_list), content_type="application/json")

    def get(self, request):
        """
        Handle get requests
        """
        if request.path.endswith('load_meta/'):
            return self.get_meta()
        elif request.path.endswith('load_config/'):
            plugin_name = request.GET.get('name')
            if not plugin_name:
                return self.EMPTY_RESULT

            return self.get_config(plugin_name)

        return self.EMPTY_RESULT

    def post(self, request):
        """
        Save plugin meta or config
        """
        http_post = request.POST
        logger.debug(type(http_post))
        if not isinstance(http_post, dict):
            raise Exception("Invalid plugin meta info!")

        response = celery_call('api.plugin.save', (http_post,))
        return HttpResponse(json.dumps(response), content_type="application/json")

class PluginListView(TemplateView):
    template_name = "plugin_list.html"

