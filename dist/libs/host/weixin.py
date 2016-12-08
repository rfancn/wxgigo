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
import sys
import os

import cuisine
from fabric.colors import green
from fabric.utils import puts

from libs.host.base import BaseHost, HostDesc, HostRole
from libs.service import NginxService, UwsgiService
from libs.option import WeixinHostOption
from libs.project import WXMPProject

class WeixinHost(BaseHost):
    def __init__(self):
        super(WeixinHost, self).__init__()
        self.desc = HostDesc.WEIXIN
        self.role = HostRole.WEIXIN
        self.option = WeixinHostOption(self)

    def setup_service_nginx(self):
        puts(green("Setup nginx service"))
        # make sure nginx package installed
        cuisine.package_ensure('nginx')

        self.nginx_service = NginxService(self)
        if not self.nginx_service:
            print 'Failed to setup nginx because of invalid info'
            sys.exit(1)

        self.nginx_service.configure()
        self.nginx_service.enable()

    def setup_service_uwsgi(self):
        puts(green("Setup uwsgi service"))
        # make sure nginx package installed
        cuisine.package_ensure('uwsgi')
        cuisine.package_ensure('uwsgi-plugin-python')

        self.uwsgi_service = UwsgiService(self)
        if not self.uwsgi_service:
            print 'Failed to setup uwsgi because of invalid info'
            sys.exit(1)

        self.uwsgi_service.configure()
        self.uwsgi_service.enable()

    def setup_project_wxmp(self, options):
        """
        Copy wxmp frontend sub project source files from Github

        :return:
        """
        puts(green("Setup wxmp project"))

        project = WXMPProject(self, options)
        project.setup_source_files()
        project.configure()

    def setup(self, options):
        self.setup_service_nginx()
        self.setup_service_uwsgi()
        self.setup_project_wxmp(options)





