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

from abc import ABCMeta, abstractmethod
from string import Template

class WXMPSend(object):
    """
    Base send message/event
    """
    __metaclass__ = ABCMeta

    def __init__(self, recv):
        super(WXMPSend, self).__init__()
        self.recv = recv

    def validate(self, kwargs):
        required_args = self.get_required_args()
        if not isinstance(required_args, list):
            print "Required arguments must be a list of keys!"
            return False

        if not set(required_args).issubset(set(kwargs.keys())):
            print "Passed in kwargs doesn't contains all required args!"
            return False

        return True

    def assembly(self, kwargs):
        template = Template(self.get_template())
        kwargs.update(self.get_common_args())

        self.content = template.safe_substitute(kwargs)

    @abstractmethod
    def get_required_args(self):
        """
        Get must inputted arguments for template
        """
        pass

    @abstractmethod
    def get_template(self):
        pass






class WXMPTemplateReply(WXMPReply):
    """
    Template reply
    """
    def __init__(self, recv):
        super(WXMPTemplateReply, self).__init__(recv)
        self.category = REPLY_CATEGORY.TEMPLATE

    def get_common_args(self):
        common_kwargs = { 'to_username': self.recv.from_username}
        return common_kwargs

    def get_template_type(self):
        return 'json'
