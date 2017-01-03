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
import socket
from fabric.api import prompt

class BaseOption(object):
    def __init__(self, host):
        self.host = host

    def get_option_value(self, option_name):
        service_config_options = self.host.config.get(self.section)
        if not service_config_options:
            return None

        return service_config_options.get(option_name, None)

    def get_option(self, option_name, prompt_msg, default=None, validate=None):
        option_value = self.get_option_value(option_name)
        if not option_value:
            option_value = prompt(prompt_msg, default=default, validate=validate)

        return option_value

class ServiceOption(BaseOption):
    def __init__(self, host, name):
        super(ServiceOption, self).__init__(host)
        self.section = 'SERVICE_{0}'.format(name.upper())

class HostOption(BaseOption):
    def __init__(self, host):
        super(HostOption, self).__init__(host)
        self.section = 'HOST_{0}'.format(host.role.upper())

        self.ssh_host = \
            self.get_option('ssh_host',
                            "* What's SSH hostname/IP for {0}?".format(host.desc),
                            default='localhost')

        # try to resolve IP address for SSH host
        try:
            self.ipaddr = socket.gethostbyname(self.ssh_host)
        except socket.gaierror:
            print 'Error resolve IP address for SSH host:{0}'.format(self.ssh_host)
            sys.exit(1)

        self.ssh_port = \
            int(self.get_option('ssh_port',
                                "* What's SSH port for {0}?".format(self.host.desc),
                                default=22, validate=int))

        self.ssh_user = self.get_option('ssh_user',
                                        "* What's SSH user for {0}?".format(self.host.desc),
                                        default=self.get_current_user())

        self.ssh_hoststr = "{0}@{1}:{2}".format(self.ssh_user, self.ssh_host, self.ssh_port)

        # try to get ssh password and if no such value set, just ignore it
        self.ssh_password = self.get_option_value('ssh_password')

        self.wxgigo_home = \
            self.get_option('wxgigo_home',
                            "* What's wxgigo home for {0}?".format(self.host.desc),
                            default="/opt/wxgigo")

        self.deploy_group = self.deploy_user = \
            self.get_option('deploy_user',
                            "* What's deploy user for {0}?".format(self.host.desc),
                            default='wxgigo')


    def get_current_user(self):
        current_user = os.environ['USER']
        if os.environ.has_key('SUDO_USER'):
            current_user = os.environ['SUDO_USER']

        return current_user

