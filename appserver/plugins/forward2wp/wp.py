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
import xmlrpclib
from slugify import slugify

class WordPress(object):
    def __init__(self, config):
        # config is a PluginConfig object
        self.config = config

        self.post_status = {'draft': 0, 'published':1 }
        try:
            self.server = xmlrpclib.ServerProxy(self.config.wp_xmlrpc_url)
        except Exception,e:
            raise e

    def new_post(self, title, excerpt, content, draft=False):
        data = {'title': title, 'description': content, 'wp_slug': slugify(title)}
        if len(excerpt) > 10:
            data.update({'mt_excerpt': excerpt})

        post_status = self.post_status['published']
        if draft:
            post_status = self.post_status['draft']
        try:
            post_id = self.server.metaWeblog.newPost("", self.config.wp_username, self.config.wp_password, data, post_status)
        except Exception,e:
            raise e

        return post_id

