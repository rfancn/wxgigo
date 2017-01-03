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
import os
import urlparse

from plugins.forward2wp.wxbase import WXBaseElement


class WXImage(WXBaseElement):
    def __init__(self, parent_dir, element):
        super(WXImage, self).__init__()

        # To easy identify media files belong to which html,
        # stores media files under a dir which has the same name with html file's basename
        self.parent_dir = parent_dir
        # here element is a lxml.etree element object
        self.element = element

        self.url = self.get_url()
        if not self.url:
            raise Exception("Failed to get html image element's url.")

        self.dir = self.get_dir()
        #IMPORTANT: filename need to be built after self.url has been set
        self.filename = self.get_filename()
        if not self.filename:
            raise Exception("Failed to build image element's filename.")

    def get_dir(self):
        return os.path.join(self.root_dir, self.parent_dir)

    def get_filename(self):
        try:
            type = self.element.attrib['data-type']
        except:
            # set default type to be jpeg
            type = 'jpeg'

        try:
            basename = urlparse.urlparse(self.url).path.split("/")[2]
        except:
            return None

        return "{0}.{1}".format(basename, type)

    def get_url(self):
        try:
            url = self.element.attrib['data-src']
        except:
            print self.img_elem.attrib
            return None

        return url



