#!/usr/bin/env python
# coding=utf-8
"""
 Copyright (C) 2010-2013, Ryan Fan <ryan.fan@oracle.com>

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Library General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
"""
from __future__ import absolute_import
import paramiko
import os

###################################################
# To bypass cross domain iframe auto height issue,
# transfer the static html file to wordpress site
###################################################
class Transfer(object):
    def __init__(self, config):
        self.config = config
        self.remote_root = "/var/www/html/wordpress/pages"
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.config.ssh_host, port=int(self.config.ssh_port),
                             username=self.config.ssh_username, password= self.config.ssh_password)
            # to increase performance
            self.ssh.get_transport().window_size = 3 * 1024 * 1024
            self.sftp = self.ssh.open_sftp()
        except Exception,e:
            raise e

    def mkdir_p(self, remote_directory):
        """Change to this directory, recursively making new folders if needed.
        Returns True if any folders were created."""
        if remote_directory == '/':
            # absolute path so change directory to root
            self.sftp.chdir('/')
            return
        if remote_directory == '':
            # top-level relative directory must exist
            return
        try:
            self.sftp.chdir(remote_directory) # sub-directory exists
        except IOError:
            dirname, basename = os.path.split(remote_directory.rstrip('/'))
            self.mkdir_p(dirname) # make parent directories
            self.sftp.mkdir(basename) # sub-directory missing, so created it
            self.sftp.chdir(basename)
            return True

    def save_content(self, dir, filename, content):
        save_dir = os.path.join(self.config.static_root, dir)
        self.mkdir_p(save_dir)

        if self.sftp.getcwd() != save_dir:
            raise Exception("Failed to switch to save dir: {0}".format(save_dir))

        remote_file = None
        try:
            remote_file = self.sftp.open(filename, 'w')
            remote_file.write(content)
        except Exception,e:
            print "Failed to save content to remote server because of: {0}".format(e)
            return
        finally:
            if remote_file:
                remote_file.close()

    def close(self):
        self.ssh.close()

