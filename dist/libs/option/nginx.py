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

from libs.option import ServiceOption

class NginxServiceOption(ServiceOption):
    def __init__(self, host):
        super(NginxServiceOption, self).__init__(host, 'nginx')

        self.server_name = self.get_option('server_name',
                                           'Please input http server name for {0}'.format(host.desc),
                                            default=host.option.ssh_host)

        self.server_port = self.get_option('server_port',
                                           "Please input http server port for {0}".format(host.desc),
                                           default=80, validate=int)

        self.static_root = self.get_option('static_root',
                                          "Please input static dir for {0}".format(host.desc),
                                          default=os.path.join(host.option.wxgigo_home, 'static'))