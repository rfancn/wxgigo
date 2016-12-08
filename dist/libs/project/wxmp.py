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
import cuisine

from libs.project import BaseProject

class WXMPProject(BaseProject):
    def __init__(self, host, options):
        super(WXMPProject, self).__init__(host, options)
        self.project_name = 'wxmp'



    def configure(self):
        # wxgigo specific uwsgi config file
        settings_file = os.path.join(self.home, 'settings.py')
        settings_content = cuisine.text_template(
            cuisine.file_local_read('conf/wxmp/settings.py'),
            dict(static_root=self.host.nginx_service.option.static_root)
        )
        cuisine.file_write(settings_file, settings_content)

        # set the correct permission of django debug file
        cuisine.file_ensure('/tmp/wxgigo-wxmp.log', owner='uwsgi', group='nginx')

        # upload sqlite3 db file
        remote_db_file = os.path.join(self.host.option.wxgigo_home, 'db.sqlite3')
        cuisine.file_upload(remote_db_file, 'db.sqlite3')
        cuisine.file_ensure(remote_db_file, owner='uwsgi', group='nginx')

        # upload django manage.py file
        remote_manage_file = os.path.join(self.host.option.wxgigo_home, 'manage.py')
        cuisine.file_upload(remote_manage_file, 'manage.py')

        cuisine.run('chown -R {0}:{1} {2}'.format(self.host.option.deploy_user,
                                                      self.host.option.deploy_group,
                                                      self.home))