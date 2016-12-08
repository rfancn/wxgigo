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

from fabric.api import prompt, sudo
from fabric.colors import green
from fabric.utils import puts
import cuisine

from libs.option import CeleryServiceOption

class CeleryService(object):
    def __init__(self, host, wxgigo_appserver_home):
        puts(green("Collecting Celery service information..."))
        self.host = host
        self.wxgigo_appserver_home = wxgigo_appserver_home
        self.option = CeleryServiceOption(host)

    def enable(self):
        # enable nginx service
        if self.host.dist_info.service_manage_method == 'systemctl':
            sudo('systemctl enable celery')
        elif self.host.dist_info.service_manage_method == 'chkconfig':
            sudo('chkconfig --enable 23456 celeryd')

    def configure_tmpfiles(self):
        """
        celery service will create pid file and log files in /run and /var/log dir,
        such dir need to be created and set correct permission before it starts.

        Systemd provide a systemd-tmpfiles service to achive such target,
        just create celery.conf file in /usr/lib/tmpfiles.d/ dir and
        contains definition of dir which need to be created.

        :return:
        """
        TMPFILES_DIR = '/usr/lib/tmpfiles.d/'
        TMPFILES_CONF_FILENAME = 'celery.conf'

        if not os.path.exists(TMPFILES_DIR):
            print "Error configure celery tmpfiles: no {0}".format(TMPFILES_DIR)
            sys.exit(1)

        remote_file = os.path.join(TMPFILES_DIR, TMPFILES_CONF_FILENAME)
        cuisine.file_upload(remote_file, 'conf/celery/celery.tmpfiles')

    def configure_systemd_unit(self, conf_file):
        SYSTEMD_DIR = '/usr/lib/systemd/system/'
        SYSTEMD_CELERY_FILENAME = 'celery.service'

        if not os.path.exists(SYSTEMD_DIR):
            print "Error configure celery systemd unit: no {0}".format(SYSTEMD_DIR)
            sys.exit(1)

        # replace and put service unit file into /usr/lib/systemd/system
        unit_file = os.path.join(SYSTEMD_DIR, SYSTEMD_CELERY_FILENAME)
        unit_content = \
            cuisine.text_template(cuisine.file_local_read('conf/celery/celery.service'),
                                  dict(celery_conf_file=conf_file,
                                       wxgigo_appserver_home=self.wxgigo_appserver_home))
        cuisine.file_write(unit_file, unit_content)

    def configure(self):
        if self.host.dist_info.major_distname in ('centos7', 'redhat7', 'fedora7', 'oracle7'):
            self.configure_for_redhat7()

    def configure_for_redhat7(self):
        cuisine.user_ensure('celery')

        CELERY_CONF_DIR = '/etc/default/'
        CELERY_CONF_FILENAME = 'celeryd'
        if not os.path.exists(CELERY_CONF_DIR):
            print "Error configure celery service: no {0}".format(CELERY_CONF_DIR)
            sys.exit(1)

        conf_content = \
            cuisine.text_template(cuisine.file_local_read('conf/celery/celeryd.conf'), {})
        conf_file = os.path.join(CELERY_CONF_DIR, CELERY_CONF_FILENAME)
        cuisine.file_write(conf_file, conf_content)

        self.configure_tmpfiles()
        self.configure_systemd_unit(conf_file)

    def configure_for_redhat6(self):
        SYSV_DIR = '/etc/init.d/'
        SYSV_CELERY_FILENAME = 'celeryd'

