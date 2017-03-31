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

from wxgigo.utils.misc import AttributeDict, get_current_user, prompt, prompt_yes_no

class DuplicateHostException(Exception):
    pass

class BaseHost(AttributeDict):
    """
    Host is a subclass of AttributeDict

    """
    def __init__(self):
        super(BaseHost, self).__init__()
        self.role_list = [self.role]
        self.hostname = 'localhost'
        self.port = '22'
        self.user = get_current_user()

    def prompts_input_config(self, cached_hosts):
        sys.stdout.write("\n")

        self.hostname = prompt("Please input %s's ip or hostname?" % self.role, default=self.hostname)

        # if we found this host has been defined before
        if self.hostname  in cached_hosts.keys():
            existed_host = cached_hosts[self.hostname]
            # For the same host role, it can only exist one host in inventory.hosts
            # e,g: existed host =
            #          host:  localhost
            #          role_list: ['agent', 'db']
            #  it should skip add the new host if new host =
            #          host = localhost
            #          role = 'agent'
            if self.role in existed_host.role_list:
                raise DuplicateHostException(
                    "Duplicate {}:[{}] found, skip it...".format(self.role, self.hostname)
                )
            else:
                # check if we need add another role for this already existed host
                answer = prompt_yes_no("Are you sure add additional role '{}' for '{}'?".format(self.role, self.hostname), default='yes')
                # only update if the answer is yes
                if answer is True:
                    self.role_list += existed_host.role_list
                    self.user = existed_host.user
                    self.port = existed_host.port
        else:
            self.user = prompt("Please input %s's SSH user" % self.role,  default=self.user)
            self.port = prompt("Please input %s's SSH port" % self.role, default=self.port, validate='[0-9].*')

class AgentHost(BaseHost):
    def __init__(self):
        self.role = HOST_ROLE.AGENT
        super(AgentHost, self).__init__()

class AppHost(BaseHost):
    def __init__(self):
        self.role = HOST_ROLE.APP
        super(AppHost, self).__init__()

class DBHost(BaseHost):
    def __init__(self):
        self.role = HOST_ROLE.DB
        super(DBHost, self).__init__()

class BrokerHost(BaseHost):
    def __init__(self):
        self.role =  HOST_ROLE.BROKER
        super(BrokerHost, self).__init__()


class HOST_ROLE:
    AGENT = "AGENT_HOST"
    APP = "APP_HOST"
    DB = "DB_HOST"
    BROKER = "BROKER_HOST"

# Available host arguments dict which will be displayed in
#  $ wxgigo-admin deploy -r
HOST_ROLE_ARGUMENTS = {
    "agent":     HOST_ROLE.AGENT,
    "app":       HOST_ROLE.APP,
    "db":        HOST_ROLE.DB,
    "broker":   HOST_ROLE.BROKER,
}

HOST_ROLE_CLASSES = {
    HOST_ROLE.AGENT: AgentHost,
    HOST_ROLE.APP: AppHost,
    HOST_ROLE.DB: DBHost,
    HOST_ROLE.BROKER: BrokerHost,
}
