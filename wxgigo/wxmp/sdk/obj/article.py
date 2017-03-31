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
from string import Template

logger = logging.getLogger(__name__)

class WXMPArticle(object):
    def __init__(self, url, title="", description="", pic_url="#"):
        self.url = url
        self.title = title
        self.description = description
        self.pic_url = pic_url

    def to_xml(self):
        tmpl = "<item>" \
                "<Title><![CDATA[$title]]></Title>" \
                "<Description><![CDATA[$description]]></Description>" \
                "<PicUrl><![CDATA[$pic_url]]></PicUrl>" \
                "<Url><![CDATA[$url]]></Url>" \
                "</item>"

        xml_item = Template(tmpl).safe_substitute(title=self.title,
                                       description=self.description,
                                       pic_url = self.pic_url,
                                       url = self.url)

        return xml_item

    def to_dict(self):
        ret = {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "picurl": self.pic_url
         }

        return ret

