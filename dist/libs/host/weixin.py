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

class WeixinHost(BaseHost):
    def __init__(self):
        super(WeixinHost, self).__init__()
        self.desc = HostDesc.WEIXIN
        self.role = HostRole.WEIXIN
        self.option = WeixinHostOption(self)

    def setup_nginx(self):
        puts(green("Setup nginx service"))
        # make sure nginx package installed
        cuisine.package_ensure('nginx')

        nginx_service = NginxService(self)
        if not nginx_service:
            print 'Failed to setup nginx because of invalid info'
            sys.exit(1)

        nginx_service.configure()
        nginx_service.enable()

    def setup_uwsgi(self):
        puts(green("Setup uwsgi service"))
        # make sure nginx package installed
        cuisine.package_ensure('uwsgi')
        cuisine.package_ensure('uwsgi-plugin-python')

        uwsgi_service = UwsgiService(self)
        if not uwsgi_service:
            print 'Failed to setup uwsgi because of invalid info'
            sys.exit(1)

        uwsgi_service.configure()
        uwsgi_service.enable()

    def setup_weixin_django_project(self):
        puts(green("Setup wxmp django project"))

        cuisine.package_ensure('unzip')

        temp_dir = cuisine.run('mktemp -d')
        if os.path.exists(temp_dir):
            with cuisine.cd(temp_dir):
                #  github zip file URL
                GIT_ARCHIVE_URL = 'https://github.com/rfancn/wxgigo/archive/master.zip'
                # download archive file
                cuisine.run('curl -sOL {0}'.format(GIT_ARCHIVE_URL))
                # unzip it
                cuisine.run('unzip master.zip')
                # and copy wxmp source files
                cuisine.run('cp -fr wxgigo-master/wxmp {0}'.format(self.option.wxgigo_home))

            cuisine.run('rm -fr {0}'.format(temp_dir))

    def setup_deploy_user(self):
        puts(green('Setup deploy user for {0}'.format(self.desc)))
        cuisine.user_ensure(self.option.deploy_user)

    def setup_deploy_dir(self):
        puts(green('Setup deploy dir for {0}'.format(self.desc)))

        cuisine.dir_ensure(self.option.wxgigo_home,
                           owner=self.option.deploy_user, group=self.option.deploy_group)

    def setup(self, options):
        self.setup_deploy_user()
        self.setup_deploy_dir()
        self.setup_nginx()
        self.setup_uwsgi()
        #self.setup_weixin_django_project()



