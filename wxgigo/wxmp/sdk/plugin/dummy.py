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
import logging

logger = logging.getLogger(__name__)

from sdk.plugin.base import BasePlugin
from sdk.plugin import PROCESSING_MODE

class DummyPlugin(BasePlugin):
    NAME = "DummyPlugin"
    VERSION = "0.0.1"
    DESCRIPTION = "Do nothing but output debug information"
    AUTHOR = "Ryan Fan"

    def is_matched(self, recv):
        return True

    def process(self, recv):
        recv.debug()
        return ""

    def get_processing_mode(self):
        return PROCESSING_MODE.SYNC