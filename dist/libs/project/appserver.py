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
from libs.host import HostDesc, HostRole
from libs.project import BaseProject

class AppServerProject(BaseProject):
    def __init__(self, host, options):
        super(AppServerProject, self).__init__(host, options)
        self.project_name = 'appserver'

    @property
    def plugins_home(self):
        return os.path.join(self.home, 'plugins')

    def configure(self, options):
        dbhost_option = options.get(HostRole.DB, None)
        if not dbhost_option:
            print "Error get DB Host option while setup_celery_app()"
            sys.exit(1)

        celeryconfig_content = \
            cuisine.text_template(cuisine.file_local_read('conf/celery/celeryconfig.py'),
                                  dict(wxgigo_dbhost_ip=dbhost_option.ipaddr,
                                       wxgigo_appserver_plugins_home = self.plugins_home))
        # it need make sure the appserver home dir is created before write celeryconfig.py there
        cuisine.dir_ensure(self.home)
        celeryconfig_file = os.path.join(self.home, 'celeryconfig.py')
        cuisine.file_write(celeryconfig_file, celeryconfig_content)

        cuisine.run('chown -R {0}:{1} {2}'.format(self.host.option.deploy_user,
                                                      self.host.option.deploy_group,
                                                      self.home))