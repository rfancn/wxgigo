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

##############################################################
# PLUGINS
# 1. Meta information like name, pattern, desc, author, verison
# 2. Plugin private configuration
# 3. Active plugin name
###############################################################
WXMP_PLUGINS_META = "WXMP:PLUGINS:META"
WXMP_PLUGINS_CONF = "WXMP:PLUGINS:CONF"

# activated plugin list
WXMP_PLUGINS_ACTIVE = "WXMP:PLUGINS:ACTIVE"
WXMP_PLUGINS_DIR_NAME = "plugins"

# the main class name for each plugin in it's plugin.py
WXMP_PLUGIN_CLASS_NAME = "Plugin"
WXMP_PLUGIN_CONFIG_CLASS_NAME = "PluginConfig"

##############################################################
# Weixin Platform Developer configuration
###############################################################
WXMP_CONFIG = "WXMP:CONFIG"

WXMP_CONFIG_REQUIRED_KEYS = (
    'WX_ID',
    'WX_ORIGINAL_ID',
    'APP_ID',
    'APP_KEY',
    'TOKEN',
    'ENCODING_AES_KEY',
    'MSG_ENCRYPT_METHOD'
)

##############################################################
# Basic
###############################################################
WXMP_ACCESS_TOKEN = "WXMP:ACCESS_TOKEN"

##############################################################
# Web authentication
###############################################################
WXMP_WEB_ACCESS_TOKEN = "WXMP:WEB:ACCESS_TOKEN"

##############################################################
# Fans management
###############################################################
# fans team, all fans introduced by scan promotion qrcode will be in WXMP:FANS:TEAM
# {
# 'leader1's open_id': ('open_id1', 'open_id2'),
# 'leader2's open_id': ('open_id1', 'open_id2'),
# ...
# }
WXMP_FANS_TEAM = "WXMP:FANS:TEAM"
WXMP_FANS = "WXMP:FANS"