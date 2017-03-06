#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2016 Ryan Fan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""
import requests
from django.views.generic import TemplateView

import logging
import re
from lxml import html
logger = logging.getLogger(__name__)

class QueryView(TemplateView):
    template_name = 'apps/wywxjj/query.html'

    def first_access(self):
        url = "http://szjw.changsha.gov.cn/index.php/home/index/searchdata/"
        s = requests.session()
        resp = s.get(url)
        cookies = s.cookies.get_dict()
        logger.debug(cookies)
        self.request.session['PHPSESSID'] = cookies.get('PHPSESSID', None)

        found = re.findall(r'name="xzyj" value="(.*)"', resp.content)
        if found:
            self.request.session['xzyj'] = found[0]

        found = re.findall(r'name="__hash__" value="(.*)"', resp.content)
        if found:
            self.request.session['__hash__'] = found[0]

    def refresh_vcode_image(self):
        url = "http://szjw.changsha.gov.cn/index.php/home/common/verifycode.html"
        s = requests.session()
        resp = s.get(url, cookies={'PHPSESSID': self.request.session['PHPSESSID']})
        with open('/opt/wxgigo/static/wywxjj/query_vcode.jpg', 'w') as f:
            f.write(resp.content)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        # get PHPSESSID when first time to access
        self.first_access()
        # get vcode
        #self.refresh_vcode_image()
        return self.render_to_response(context)

    def parse_xq(self, xq_info):
        rows = []
        root = html.fromstring(xq_info)
        tr_list = root.xpath("///tr[position()>1]")
        for tr in tr_list:
            row = []
            td_list =  tr.getchildren()
            for td in td_list:
                row.append(td.text)
            rows.append(row)
        return rows

def query_szjw(request):
    logger.debug(request.POST)
    url = "http://szjw.changsha.gov.cn/index.php/home/Searchdata/maintenancefund"
    s = requests.session()
    data = {
        'search8_idcard':request.POST.get('search8_idcard', None),
        'search8_name': request.POST.get('search8_name', None),
        'search8_room': request.POST.get('search8_room', None),
        'search8_verify_code': request.POST.get('search8_verify_code', None),
        'xzyj': request.session['xzyj'],
        '__hash__': request.session['__hash__']
    }
    logger.debug(request.session['PHPSESSID'])
    resp = s.get(url, data=data, cookies={'PHPSESSID': request.session['PHPSESSID']})
    logger.debug(resp.content)






