#!/usr/bin/env python
# coding=utf-8
"""
Copyright (c) 2010-2015, Ryan Fan <reg_info@126.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import os
from distutils.version import LooseVersion
import django
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from web.core.management.commands._params import WXMPParams

LEGACY_MODE = LooseVersion(django.get_version()) < LooseVersion("1.8")

WXMP_CONFIG_FILE = "wxconfig.py"

class WXMPConfig(object):
    def __init__(self, top_dir):
        self.top_dir = top_dir
        self.filename = WXMP_CONFIG_FILE
        self.params = WXMPParams(self)

    def proceed(self):
        self.params.get_inputs()

    def save(self):
        self.params.save()

class Command(BaseCommand):
    """
    If Django version <1.8, it use option_list to add additional options
    If Django version >=1.8, it use add_parse() function to add additional options
    """
    help = "Configure Weixin public account"
    args = '[optional destination directory]'

    if LEGACY_MODE:
        from optparse import make_option
        option_list = BaseCommand.option_list + (
            #make_option(),
        )

    # only useful for Django version >= 1.8
    def add_arguments(self, parser):
        # Positional arguments
        # parser.add_argument('id', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '-h',
            '--help',
            action='store_true',
            dest='help_config',
            default=False,
            help='Help how to configure Weixin public account'
        )

    def validate_top_dir(self, top_dir):
        """
        Try to locate where is the WXMP app's dir
        """
        if not os.path.exists(top_dir):
            raise CommandError("Target directory '%s' does not exist,"
                                "please create it: django-admin.py startapp wxmp_bak." % top_dir)

        if not os.access(top_dir, os.W_OK|os.X_OK):
            raise CommandError("Target directory '%s' must writable by current user,"
                                "please correct permission." % top_dir)

    def handle(self, dir=None, **options):
        if dir is None:
            top_dir = os.getcwd()
        else:
            top_dir = os.path.abspath(os.path.expanduser(dir))

        self.validate_top_dir(top_dir)

        config = WXMPConfig(top_dir)
        config.proceed()
        config.save()

        self.stdout.write("")
        self.stdout.write("Successfully save wxmp_bak config file:{0}".format(os.path.join(top_dir, WXMP_CONFIG_FILE)))
        self.stdout.write("You need put it under '<consumer dir>/wxmp_bak/' subdirectory.")



