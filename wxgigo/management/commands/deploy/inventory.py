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
from __future__ import unicode_literals
import os
import tempfile

from wxgigo.management.commands.deploy.host import HOST_ROLE_CLASSES, DuplicateHostException, HOST_ROLE_ARGUMENTS
from wxgigo.utils.net import is_localhost
from wxgigo.utils.misc import prompt_yes_no

class Inventory(object):
    def __init__(self, arg_host_role):
        self.host_role = self.get_host_role(arg_host_role)
        self.hosts = {}
        self.dir = None
        self.file = "hosts"

    def get_host_role(self, arg_host_role):
        if arg_host_role is None:
            return None

        return HOST_ROLE_ARGUMENTS[arg_host_role]

    def add_new_host(self, host_role):
        """ New Host instance(dict) for specific role and add to inventory.hsots"""
        try:
            new_host = HOST_ROLE_CLASSES[host_role]()
            new_host.prompts_input_config(self.hosts)
        except DuplicateHostException as e:
            print "\n{}\n".format(e.message)

        # before update global hosts, no need to keep host.role attribute
        new_host.pop('role')
        self.hosts[new_host.hostname] = new_host

    def configur_for_role(self, host_role):
        """ Configure host for specific role"""
        self.add_new_host(host_role)

        continue_add = True
        while continue_add:
            continue_add = prompt_yes_no("Continue add another?".format(self.host_role),
                                         default='no')
            if continue_add:
                self.add_new_host(host_role)

    def print_hosts(self):
            for host_name, host_defs in self.hosts.items():
                print host_name + ":"
                host_defs = self.hosts[host_name]
                for k,v in host_defs.items():
                    print "\t{}--->{}".format(k,v)

    def configure_for_all(self):
        # if we dont' specify server role, then we need ask to get all Host Info
        for host_role, host_class in HOST_ROLE_CLASSES.items():
            print
            print "### Input Configuration for {} ###".format(host_role)
            print
            self.configur_for_role(host_role)

    def configure(self):
        print "##################################"
        print "# Input Deployment Configuration #"
        print "##################################"
        if self.host_role is None:
            self.configure_for_all()
        else:
            self.configur_for_role(self.host_role)


    def build_host_text(self, host):
        text_host = "{0}:{1} ansible_user={2}".format(host.hostname, host.port, host.user)
        if is_localhost(host.hostname):
            text_host = "{0}:{1} ansible_user={2} ansible_connection=local".format(host.hostname, host.port, host.user)

        return text_host

    def build_group_text(self, group_name):
        text_group = "[{0}]".format(group_name)
        return text_group

    def get_groups(self):
        """
         Convert hosts dict to group dict
            # From:
            # self.hosts = {
            #      "hostname1": { "hostname1": "xxx", "port": "22" , "role_list": "APP_SERVER, DB_SERVER"...}
            #      "hostname2": { "hostname2": "yyy", "port": "22" ,"role_list": "APP_SERVER"... }
            #       ...
            # }
            # To:
            # groups = {
            #      "APP_SERVER" : [
            #          { "hostname1": "xxx", "port":"22"...}
            #          { "hostname2": "yyy", "port":"22"...}
            #      "DB_SERVER" : [
            #        { "hostname1": "xxx", "port":"22"...}
        """
        groups = {}
        for role in HOST_ROLE_CLASSES.keys():
            host_list = []
            for hostname, host in self.hosts.items():
                if role in host.role_list:
                    host_list.append(host)
                groups[role] = host_list

        return groups


    def generate(self):
        print
        print "#################################"
        print "# Generate Deployment Inventory #"
        print "#################################"
        self.print_hosts()

        answer = prompt_yes_no("Please confirm above deployment configuration is fine or not?")
        if answer is True:
            groups = self.get_groups()
            try:
                self.dir = tempfile.mkdtemp()
                self.file = os.path.join(self.dir, self.file)
                # write inventory file with format
                # [APP_SERVER]
                #  www.test.com:22 ansible_connection=...
                #  localhost:22 ansible_connection=
                # [DB_SERVER]
                #  localhost:22 ansible_connection=
                with open(self.file, 'w') as f:
                    for group_name, host_list in groups.items():
                        f.write(self.build_group_text(group_name) + "\n")
                        for h in host_list:
                            f.write(self.build_host_text(h) + "\n")
                        f.write("\n")
                    f.write("\n")
            except:
                raise





