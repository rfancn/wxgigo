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
import sys
import cuisine
from fabric.api import put

GIT_ARCHIVE_URL = 'https://github.com/rfancn/wxgigo/archive/master.zip'

class BaseProject(object):
    def __init__(self, host, options):
        self.host = host
        # here is deploy_options contains all other kind of host's configured options
        self.options = options

    @property
    def home(self):
        return os.path.join(self.host.option.wxgigo_home, self.project_name)

    def setup_source_files(self):
        """
        Copy latest project source files from Github

        :param sub_project:
        :return:
        """
        self.setup_source_files_from_local()

    def setup_source_files_from_local(self):
        wxgigo_src_dir = self.options.get('wxgigo_src_dir', None)
        if not wxgigo_src_dir:
            print "Error get wxgigo source dir"
            sys.exit(1)

        local_project_src_dir = os.path.join(wxgigo_src_dir, self.project_name)
        if not os.path.exists(local_project_src_dir):
            print 'Error get local project source dir: {0}'.format(local_project_src_dir)
            sys.exit(1)

        with cuisine.cd(wxgigo_src_dir):
            put(local_project_src_dir, self.host.option.wxgigo_home, use_sudo=True)

    def setup_source_files_from_git(self):
        """
        Copy latest project source files from Github

        :param sub_project:
        :return:
        """
        cuisine.package_ensure('unzip')

        temp_dir = cuisine.run('mktemp -d')
        cuisine.dir_ensure(temp_dir)
        cuisine.dir_ensure(self.host.option.wxgigo_home)

        with cuisine.cd(temp_dir):
            # download archive file
            cuisine.run('curl -OL {0}'.format(GIT_ARCHIVE_URL))
            # unzip it
            cuisine.run('unzip master.zip')
            # and copy source files
            cp_src = os.path.join('wxgigo-master', self.project_name)
            cuisine.run('cp -fr {0} {1}'.format(cp_src, self.host.option.wxgigo_home))

        cuisine.run('rm -fr {0}'.format(temp_dir))