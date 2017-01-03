#!/usr/bin/env python
#-*- encoding:utf-8 -*-
"""
Copyright (c) 2010-2015, Ryan Fan <reg_info@126.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
class REPLY_CATEGORY:
    """
    ASYNC:    async reply which will provide a link to client,
              progress status will show up in another page when click this link,
              it will be used when server side need more than 5 seconds to handle task
    PASSIVE:  Weixin standard auto reply which automatically reply to recv in 5 seconds
    SERVICE:  Weixin standard customer service reply
    GROUP:    Weixin standard group reply
    TEMPLATE: Weixin standard template reply for business
    """
    ASYNC = 'async'
    PASSIVE = 'passive'
    SERVICE = 'service'

class REPLY_PASSIVE_TYPE:
    TEXT = "text"
    IMAGE = 'image'
    VOICE = 'voice'
    VIDEO = 'video'
    MUSIC = 'music'
    NEWS = 'news'

class REPLY_SERVICE_TYPE:
    TEXT = "text"
    IMAGE = 'image'
    VIDEO = 'video'
    MUSIC = 'music'
    NEWS = 'news'