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
import cuisine

SUPPORTED_DIST_NAME = ('redhat', 'centos', 'debian')
SUPPORTED_PKG_MANAGEMENT_METHODS = {
    'redhat': 'yum',
    'centos': 'yum',
    'debian': 'apt'
}
SUPPORTED_SERVICE_MANAGEMENT_METHODS = {
    'redhat7': 'systemctl',
    'redhat6': 'chkconfig',
    'centos7': 'systemctl',
    'centos6': 'chkconfig'
}

class DistInfo(object):
    def __init__(self, dist_info):
        dist_info = cuisine.run('python -c "import platform;print platform.dist()"')
        distname, version, core = eval(dist_info)
        if distname not in SUPPORTED_DIST_NAME:
            return None

        self.distname = distname
        self.version = version
        self.major_version = version.split(".")[0]
        self.minor_version = version.split(".")[1]
        self.core = core
        self.pkg_manage_method = SUPPORTED_PKG_MANAGEMENT_METHODS[distname]
        self.major_distname = "{0}{1}".format(self.distname, self.major_version)
        self.service_manage_method = SUPPORTED_SERVICE_MANAGEMENT_METHODS[self.major_distname]