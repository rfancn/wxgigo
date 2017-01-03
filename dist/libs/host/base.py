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
import ConfigParser

import fabric
from fabric.api import local, prompt, settings, prefix
from fabric.utils import puts
from fabric.colors import green
import cuisine

from libs.option import HostOption
from libs.host.dist import DistInfo

class HostRole:
    DB = 'db'
    APP = 'app'
    WEIXIN = 'weixin'

class HostDesc:
    DB = 'DB Host'
    APP = 'App Host'
    WEIXIN = 'Weixin Host'

class BaseHost(object):
    def __init__(self):
        self.config = self.load_config()
        self.option = None

    def load_config(self):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read("config.ini")

        config = {}
        for section in config_parser.sections():
            option = {}
            for k, v in config_parser.items(section):
                option[k] = v
            config[section] = option

        return config

    def invoke(self, cmd):
        invoke_cmd = local
        if self.is_remote:
            invoke_cmd =  cuisine.run

        return invoke_cmd(cmd)

    def get_package_list(self, is_python_pkg = False):
        pkg_list_filename = 'syspkgs.txt'
        if is_python_pkg:
            pkg_list_filename = 'pypkgs.txt'
        pkg_list_file = os.path.join("roles", self.role, self.dist_info.distname,  pkg_list_filename)

        if not os.path.exists(pkg_list_file):
            return []

        pkg_list = []
        with open(pkg_list_file, "r") as f:
            # remove '\r' '\n' if they exist
            pkg_list = [ line.replace("\r","").replace("\n", "") for line in f.readlines() ]
            # to make pip command supports 'django<1.9,>=1.8' format,
            # add "" for all package name
            pkg_list = [ '\"{0}\"'.format(pkg) for pkg in pkg_list ]

        return pkg_list

    def setup_cuisine(self):
        # setup basic cuisine options
        cuisine.host(self.option.ssh_hoststr)
        cuisine.user(self.option.ssh_user)
        if self.option.ssh_password:
            fabric.api.env.password = self.option.ssh_password

        self.dist_info = DistInfo(self)
        cuisine.select_package(self.dist_info.pkg_manage_method)

        cuisine.mode_sudo()

    def setup_sys_packages(self):
        puts(green('Setup system packages for {0}'.format(self.desc)))

        for pkg in self.get_package_list():
            cuisine.package_ensure(pkg)

    def setup_python_packages(self):
        puts(green('Setup python packages for {0}'.format(self.desc)))

        # select choose pip and make sure it is at the latest version
        cuisine.select_python_package('pip')

        # use China pip repository to speed up installation process
        with prefix('export PIP_INDEX_URL=https://pypi.douban.com/simple'):
            cuisine.python_package_upgrade('pip')

            for pkg in self.get_package_list(is_python_pkg=True):
                cuisine.python_package_ensure(package=pkg)

    def setup_os_env(self):
        # execute all commands defined in os.txt
        os_command_file = os.path.join("roles", self.role, self.dist_info.distname, 'os.txt')
        if os.path.exists(os_command_file):
           with open(os_command_file, "r") as f:
                # remove '\r' '\n' if they exist
                cmd_list = [ line.replace("\r","").replace("\n", "") for line in f.readlines() ]
                for cmd in cmd_list:
                    cuisine.run(cmd)

    def pre_deploy(self):
        # setup env
        self.setup_cuisine()
        self.setup_sys_packages()
        self.setup_python_packages()
        self.setup_os_env()

    def post_deploy(self):
        # add iptables allow host
        pass

    def deploy(self, options):
        puts(green("=== Deploy {0} ===".format(self.desc)))
        self.pre_deploy()
        self.setup(options)
        self.post_deploy()


