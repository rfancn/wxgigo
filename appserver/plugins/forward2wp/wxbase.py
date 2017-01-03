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
from abc import ABCMeta, abstractmethod
from datetime import datetime
import requests

class WXBaseElement(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.root_dir = datetime.today().strftime("%Y/%m/%d")

    def get_content(self):
        if not self.url:
            return None

        try:
            response = requests.get(self.url)
        except Exception,e:
            print "Failed to get element's content because of: {0}".format(e)
            return None

        if response.status_code != 200:
            print "Failed to get element's content because of http code: {0}".format(response.status_code)
            return None

        # according to requests document,
        # response.text is a decoded response.content
        # if we can get encoding from HTTP headers
        if response.encoding:
            return response.text

        return response.content

    @abstractmethod
    def get_dir(self):
        pass

    @abstractmethod
    def get_filename(self):
        pass

    @abstractmethod
    def get_url(self):
        pass
