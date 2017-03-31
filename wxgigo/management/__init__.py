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
import os

from wxgigo.management.cmdparser import CommandParser, CommandError
from wxgigo.management.cmdhelper import CommandHelper

__VERSION__ = "0.0.1"

class ManagementUtility(object):
    """
    Encapsulates the logic of the wxgigo-admin features.

    A ManagementUtility has a number of commands, which can be manipulated
    by editing the self.commands dictionary.
    """
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        self.management_dir = __path__[0]

    def execute(self):
        """
        Given the command-line arguments, this figures out which subcommand is
        being run, creates a parser appropriate to that command, and runs it.
        """
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help'  # Display help if no arguments were given.

        # Preprocess options to extract --settings and --pythonpath.
        # These options could affect the commands that are available, so they
        # must be processed early.
        parser = CommandParser(None, usage="%(prog)s COMMAND [options] [args]", add_help=False)

        # Add default arguments
        parser.add_argument('args', nargs='*')  # catch-all
        try:
            options, args = parser.parse_known_args(self.argv[2:])
        except CommandError:
            pass  # Ignore any option errors at this point.

        cmd_helper = CommandHelper(self.prog_name, self.management_dir)
        if subcommand == 'help':
            if len(options.args) < 1:
                sys.stdout.write(cmd_helper.get_main_usage())
            else:
                # print specific subcommand help
                cmd_helper.fetch_command(options.args[0]).print_help(self.prog_name, options.args[0])
        # print version info
        elif self.argv[1:] in(['--version'], ['-v']):
            sys.stdout.write(__VERSION__ + '\n')
        # print main uaage
        elif self.argv[1:] in (['--help'], ['-h']):
            sys.stdout.write(cmd_helper.get_main_usage())
        else:
            cmd_helper.fetch_command(subcommand).run_from_argv(self.argv)

def execute_from_command_line(argv=None):
    """
    A simple method that runs a ManagementUtility.
    """
    utility = ManagementUtility(argv)
    utility.execute()

