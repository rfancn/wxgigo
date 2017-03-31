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
from string import Template

from sdk.reply.base import WXMPPassiveReply
from sdk.obj.article import WXMPArticle
from sdk.reply import REPLY_PASSIVE_TYPE


XML_TEMPLATE = """
<xml>
<ToUserName><![CDATA[$to_username]]></ToUserName>
<FromUserName><![CDATA[$from_username]]></FromUserName>
<CreateTime>$create_time</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>$article_count</ArticleCount>
<Articles>$articles<</Articles>
</xml>
"""


class WXMPPassiveReplyNews(WXMPPassiveReply):
    def __init__(self, recv):
        super(WXMPPassiveReplyNews, self).__init__(recv)
        self.type = REPLY_PASSIVE_TYPE.NEWS

    def get_template(self):
        return XML_TEMPLATE

    def get_required_args(self):
        return ['articles']

    def assembly(self, kwargs):
        articles = kwargs['articles']
        if not isinstance(articles, list):
            raise Exception("Passed in articles is not a list!")

        xml_articles = ""
        for item in articles:
            if not isinstance(item, WXMPArticle):
                raise Exception("Item in articles list is not an instance of WXAMPArticle!")

            xml_articles += item.to_xml()

        template = Template(self.get_template())
        kwargs.update(self.get_common_args())
        kwargs.update({'articles': xml_articles, 'article_count': len(articles)})
        self.content = template.safe_substitute(kwargs)