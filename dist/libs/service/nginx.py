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

from libs.option import NginxServiceOption

WXGIGO_NGINX_CONF_FILENAME='wxgigo-nginx.conf'
NGINX_CONF_DIR='/etc/nginx/conf.d'

class NginxService(object):
    def __init__(self, host):
        puts(green("Collecting Nginx service information..."))

        self.host = host
        self.option = NginxServiceOption(host)

    def enable(self):
        # enable nginx service
        if self.host.dist_info.service_manage_method == 'systemctl':
            sudo('systemctl enable nginx')
        elif self.host.dist_info.service_manage_method == 'chkconfig':
            sudo('chkconfig --enable 23456 nginx')

    def configure(self):
        conf_file = os.path.join(self.host.option.wxgigo_home, WXGIGO_NGINX_CONF_FILENAME)
        conf_content = cuisine.text_template(cuisine.file_local_read('conf/nginx.conf'),
                                             dict(server_port=self.option.server_port,
                                                  server_name=self.option.server_name,
                                                  static_dir=self.option.static_dir))
        cuisine.file_write(conf_file, conf_content, owner='nginx', group='nginx')
        cuisine.dir_ensure(self.option.static_dir, owner='nginx', group='nginx')

        link_file = os.path.join(NGINX_CONF_DIR, WXGIGO_NGINX_CONF_FILENAME)
        if cuisine.file_exists(link_file):
            cuisine.run('rm {0}'.format(link_file))

        cuisine.file_link(conf_file, link_file)