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
from libs.project import AppServerProject

class AppHost(BaseHost):
    def __init__(self):
        super(AppHost, self).__init__()
        self.desc = HostDesc.APP
        self.role =  HostRole.APP
        self.option = AppHostOption(self)

    def setup_service_celery(self):
        puts(green("Setup celery service"))

        cuisine.python_package_ensure('celery')

        celery_service = CeleryService(self)
        if not celery_service:
            print 'Failed to setup celery service'
            sys.exit(1)

        celery_service.configure()
        celery_service.enable()

    def setup_project_appserver(self, options):
        """
        Copy app server backend sub project source files from Github

        :return:
        """
        puts(green("Setup app server project"))

        proj = AppServerProject(self)
        proj.setup_source_files()
        proj.configure(options)

    def setup(self, options):
        self.setup_service_celery()
        self.setup_project_appserver(options)

    def post_deploy(self):
        super(AppHost, self).post_deploy()
        cuisine.run('chown -R {0}:{1} {2}' \
                    .format(self.option.deploy_user, self.option.deploy_group,
                            self.option.wxgigo_appserver_home))





