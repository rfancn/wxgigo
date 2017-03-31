#!/usr/bin/env python
# coding=utf-8
"""
The MIT License (MIT)

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
from django.core.management.base import BaseCommand, CommandError

from web.core.management.commands._baseproject import LEGACY_MODE, BaseProject

class ConsumerProject(BaseProject):
    def __init__(self, name, dir):
        self.type = "consumer"
        self.name = name
        self.dir = dir
        super(ConsumerProject, self).__init__()

class Command(BaseCommand):
    """
    If Django version <1.8, it use option_list to add additional options
    If Django version >=1.8, it use add_parse() function to add additional options
    """
    args = '[name] [optional destination directory]'
    help = "Create wcmb consumer project"

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
            dest='help_consumer',
            default=False,
            help='Help how to create celery consumer'
        )

    def handle(self, name="consumer", dir=None, **options):
        """
        To be compatible with Django>=1.8,
        It is encouraged to exclusively use **options for new commands.
        """
        # by default, project_dir is project_name
        if dir is None:
            top_dir = os.path.join(os.getcwd(), name)
        else:
            top_dir = os.path.abspath(os.path.expanduser(dir))
            if not os.path.exists(top_dir):
                raise CommandError("Destination directory '%s' does not "
                                   "exist, please create it first." % top_dir)


        #self.build_fs_structure(top_dir)

        # new consumer project
        proj = ConsumerProject(name, top_dir)
        proj.config()