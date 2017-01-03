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
import os

from fabric.api import prompt, sudo
from fabric.colors import green
from fabric.utils import puts
import cuisine

from libs.option import UwsgiServiceOption

class UwsgiService(object):
    def __init__(self, host):
        puts(green("Collecting uwsgi service information..."))

        self.host = host
        self.option = UwsgiServiceOption(host)

    def enable(self):
        # enable nginx service
        if self.host.dist_info.service_manage_method == 'systemctl':
            sudo('systemctl enable uwsgi')
        elif self.host.dist_info.service_manage_method == 'chkconfig':
            sudo('chkconfig --enable 23456 uwsgi')

    def configure(self):
        # uwsgi main config file
        uwsgi_ini_file = os.path.join('/etc/', 'uwsgi.ini')
        cuisine.file_upload(uwsgi_ini_file, 'conf/uwsgi/uwsgi.ini')

        # uwsgi vassals include file
        vassals_include_file = os.path.join('/etc/', 'uwsgi-vassals-default.ini')
        vassals_include_content = cuisine.text_template(
            cuisine.file_local_read('conf/uwsgi/uwsgi-vassals-default.ini'),
            dict(process_num=self.option.process_num,
                 thread_num=self.option.thread_num))
        cuisine.file_write(vassals_include_file, vassals_include_content)

        # wxgigo specific uwsgi config file
        conf_file = os.path.join(self.host.option.wxgigo_home, 'wxgigo-uwsgi.ini')
        conf_content = cuisine.text_template(
            cuisine.file_local_read('conf/uwsgi/wxgigo-uwsgi.ini'),
                                   dict(wxgigo_home=self.host.option.wxgigo_home))
        cuisine.file_write(conf_file, conf_content, owner='uwsgi', group='nginx')

        # link wxgigo specific uwsgi config file under uwsgi conf.d dir
        link_file = os.path.join('/etc/uwsgi.d/', 'wxgigo-uwsgi.ini')
        if cuisine.file_exists(link_file):
            cuisine.run('rm {0}'.format(link_file))

        cuisine.file_link(conf_file, link_file)

