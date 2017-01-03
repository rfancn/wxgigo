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
import os, io
import urlparse
from lxml import html,etree
from string import Template
import re

from plugins.forward2wp.wxbase import WXBaseElement
from plugins.forward2wp.wximage import WXImage

WXHTML_TEMPLATE = u"""
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=0" />
<title>$article_title</title>
<link rel="stylesheet" type="text/css" href="http://res.wx.qq.com/mmbizwap/zh_CN/htmledition/style/page/appmsg/page_mp_article_improve2d1390.css">
<!--[if lt IE 9]>
<link rel="stylesheet" type="text/css" href="http://res.wx.qq.com/mmbizwap/zh_CN/htmledition/style/page/appmsg/page_mp_article_improve_pc2c9cd6.css">
<![endif]-->
</head>

<body id="activity-detail" class="zh_CN mm_appmsg" ontouchstart="">
    <div id="js_article" class="rich_media">
        <div class="rich_media_inner">
            <div id="page-content">
                <div id="img-content" class="rich_media_area_primary">
                    <div id="js_content" class="rich_media_content">
                        $google_adsense
                        $article_content
                    </div><!-- js_content -->
                    <link rel="stylesheet" type="text/css" href="http://res.wx.qq.com/mmbizwap/zh_CN/htmledition/style/page/appmsg/page_mp_article_improve_combo2e4987.css">
                </div> <!-- img-content -->
           </div><!-- page-content -->
        </div><!-- rich_media_inner -->
   </div><!-- js_article -->
</body>
</html>
"""

DEBUG = True

class WXHtml(WXBaseElement):
    def __init__(self, title, url):
        super(WXHtml, self).__init__()

        self.title = title
        self.url = url

        self.dir = self.get_dir()
        self.filename = self.get_filename()
        if not self.filename:
            raise Exception("Failed to build WXHtml filename from: {0}".format(url))

        # root dir for all kinds of internal objects
        self.internal_root = os.path.splitext(self.filename)[0]
        self.internal_objects = []

        # get raw content via http
        self.raw_content = self.get_content()
        if not self.raw_content:
            raise Exception("Failed to get WXHtml content from: {0}".format(url))

        if DEBUG:
            with io.open("/tmp/{0}".format(self.filename), 'w', encoding='utf8') as f:
                f.write(self.raw_content)

        # we only focus on the meaningful part of main content in html
        self.main_content = self.get_main_content(self.raw_content)
        if not self.main_content:
            raise Exception("Failed to extract main content from html")

        # next, we will process main content in process()
        self.final_content = ""

        # as some article doesn't input the correct description in recv.description
        # try extract excerpt from main content
        self.excerpt = ""

    def get_dir(self):
        return self.root_dir

    def get_url(self):
        return self.url

    def get_filename(self):
        """
        Extract unique 'sn' as the name when article saved in filesystem
        """
        params_dict = urlparse.parse_qs(urlparse.urlparse(self.url).query)
        try:
            filename_without_ext = params_dict['sn'][0]
        except:
            return None

        # in case there is a '#rd', remove it
        filename_without_ext.replace('#rd', '')
        return "{0}.{1}".format(filename_without_ext, 'html')

    def handle_images(self, root_elem, content):
        """
        It seems lxml does some changes to html stuff while parsing html which make html looks abnormal in browser,
        so discard the way to process html by lxml,
        only try extract image element info by lxml,
        then use regex to replace the <img data-src="..."...> to <img src="..."> in main content

        Here content is inner html between <div class="rich_media_content " id="js_content">...</div>
        """
        # find img html elements and append to internal objects list
        img_list = root_elem.xpath("//img")
        for img_elem in img_list:
            try:
                wximage = WXImage(self.internal_root, img_elem)
            except Exception,e:
                print "Failed to create WXImage object because of: {0}".format(e)
                continue

            self.internal_objects.append(wximage)

        # use regex to replace all <img data-src="..." ...> to <img src="..."> in html
        for obj in self.internal_objects:
            if isinstance(obj, WXImage):
                filename_without_ext = obj.filename.split(".")[0]
                # IMPORTANT: here non-greedy regex mode need to be used ".*?"
                match_pattern = r'(data-src="http://mmbiz.qpic.cn/mmbiz/{0}.*?")'.format(filename_without_ext)
                new_img_src = 'src="{0}"'.format(os.path.join(self.internal_root, obj.filename))
                content = re.sub(match_pattern, new_img_src, content)

        return content

    def parse_excerpt(self, root_elem):
        """
        try extract description all text in html page
        """
        all_text = ""
        text_list = root_elem.xpath("//text()")
        for t in text_list:
            t.replace('\n', '')
            t.replace('\r', '')
            all_text += t.strip()

        return (all_text[:120] + u'……')

    def get_main_content(self, raw_content):
        """
        main content is inner html of "<div class="rich_media_content " id="js_content">...</div>"
        """
        js_content_pattern = re.compile(r'<div.*id="js_content".*?>(.*?)</div>.*?<script', re.DOTALL)
        found = js_content_pattern.search(raw_content)
        if found:
            main_content = found.groups()[0]
            return main_content

        return None

    def process_content(self, root_elem):
        """
        It will process img elements in this version,
        other kinds of elements will be handled in the future, like video, music
        """
        processed_content = self.handle_images(root_elem, self.main_content)
        return processed_content

    def get_meta(self):
        """
        Sometimes we need check original url,
        so save meta info in it's internal root dir, filename is '.meta'
        """
        meta = {
            'dir': os.path.join(self.dir, self.internal_root),
            'filename': '.meta',
            'content': 'url={0}'.format(self.url)
        }

        return meta

    def process(self):
        root_elem  = html.fromstring(self.main_content)

        processed_main_content = self.process_content(root_elem)
        self.final_content = Template(WXHTML_TEMPLATE).substitute(
            # all other strings are <str> type, it need keeps make unicode title as the same type,
            # otherwise, UnicodeDecodeError will thrown out
            article_title = self.title,
            google_adsense = '',
            article_content = processed_main_content
        )

        self.excerpt = self.parse_excerpt(root_elem)