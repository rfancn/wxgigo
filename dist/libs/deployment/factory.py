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
import importlib

class DeploymentFactory(object):
    def __init__(self):
        pass

    def get_server_role(self):
        server_role = self.config.defaults().get('server_role', None)
        if not server_role:
            server_role = "default"

        if server_role not in ("default", "weixin", "app", "db"):
            print "Invalid server_role in config!"
            return None

        return server_role

    def create(self):
        server_role = 'default'
        module_path = "libs.deployment.{0}".format(server_role)
        class_name = "{0}Deployment".format(server_role.title())
        try:
            mod = importlib.import_module(module_path)
            cls = getattr(mod, class_name)
            return cls()
        except Exception, e:
            print "DeploymentFactory.create() error: {0}!".format(e)
            raise e
