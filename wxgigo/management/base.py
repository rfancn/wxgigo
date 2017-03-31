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
import sys
import os

import wxgigo
from wxgigo.management.cmdparser import CommandParser, CommandError, SystemCheckError
#from wxgigo.utils.version import get_version

class BaseCommand(object):
    """
    Base Command
    """

    _called_from_command_line = False
    # Metadata about this command.
    option_list = ()
    help = ''
    args = ''

    def __init__(self):
        pass

    def get_version(self):
        """
        Return the wxgigo version, which should be correct for all
        built-in Django commands. User-supplied commands should
        override this method.
        """
        return wxgigo.get_version()

    @property
    def use_argparse(self):
        return not bool(self.option_list)

    def usage(self, subcommand):
        """
        Return a brief description of how to use this command, by
        default from the attribute ``self.help``.

        """
        return 'asdfojasodfi'

    def create_parser(self, prog_name, subcommand):
        """
        Create and return the ``ArgumentParser`` which will be used to
        parse the arguments to this command.

        """
        parser = CommandParser(self, prog="%s %s" % (os.path.basename(prog_name), subcommand),
            description=self.help or None)
        parser.add_argument('--version', action='version', version=self.get_version())
        if self.args:
            # Keep compatibility and always accept positional arguments, like optparse when args is set
            parser.add_argument('args', nargs='*')
        self.add_arguments(parser)
        return parser

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        pass

    def print_help(self, prog_name, subcommand):
        """
        Print the help message for this command, derived from
        ``self.usage()``.

        """
        parser = self.create_parser(prog_name, subcommand)
        parser.print_help()

    def run_from_argv(self, argv):
        """
        Set up any environment changes requested (e.g., Python path
        and Django settings), then run this command. If the
        command raises a ``CommandError``, intercept it and print it sensibly
        to stderr. If the ``--traceback`` option is present or the raised
        ``Exception`` is not ``CommandError``, raise it.
        """
        self._called_from_command_line = True
        parser = self.create_parser(argv[0], argv[1])

        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        # Move positional args out of options to mimic legacy optparse
        args = cmd_options.pop('args', ())
        try:
            self.handle(*args, **cmd_options)
        except Exception as e:
            if not isinstance(e, CommandError):
                raise

            self.stderr.write('%s: %s' % (e.__class__.__name__, e))
            sys.exit(1)

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement this method.

        """
        raise NotImplementedError('subclasses of BaseCommand must provide a handle() method')


