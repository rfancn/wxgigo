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

from libs.host import BaseHost, HostDesc, HostRole
from libs.option import AppHostOption
from libs.service import CeleryService

class AppHost(BaseHost):
    def __init__(self):
        super(AppHost, self).__init__()
        self.desc = HostDesc.APP
        self.role =  HostRole.APP
        self.option = AppHostOption(self)

    def setup_celery_service(self):
        puts(green("Setup celery service"))

        cuisine.python_package_ensure('celery')

        celery_service = CeleryService(self)
        if not celery_service:
            print 'Failed to setup celery service'
            sys.exit(1)

        celery_service.configure()
        celery_service.enable()

    def setup_celeryapp(self, options):
        dbhost_option = options.get(HostRole.DB, None)
        if not dbhost_option:
            print "Error get DB Host option while setup_celery_app()"
            sys.exit(1)

        celeryconfig_content = \
            cuisine.text_template(cuisine.file_local_read('conf/celery/celeryconfig.py'),
                                  dict(wxgigo_dbhost_ip=dbhost_option.ipaddr,
                                       wxgigo_plugins_home = self.option.wxgigo_plugins_home))
        cuisine.file_write(self.option.celeryconfig_file, celeryconfig_content)

    def setup(self, options):
        self.setup_celeryapp(options)
        self.setup_celery_service()



