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
import pkgutil
from importlib import import_module

USAGE= """\
Type '{prog_name} help <COMMAND>' for help on a specific subcommand

Usage: {prog_name} COMMAND [options]

List of Commands:
{command_list}

Options:
  -h, --help            show this help message and exit
  --version             show Yum version and exit
"""

class CommandHelper(object):
    def __init__(self, prog_name, management_dir):
        self.prog_name = prog_name
        self.management_dir = management_dir
        self.commands = sorted(self.find_commands())

    def get_main_usage(self):
        """
        sub commands usage
        """
        usage_output = USAGE.format(prog_name=self.prog_name,
                                    command_list='\n'.join(self.commands))
        return usage_output

    def find_commands(self):
        """
        Given a path to a management directory, returns a list of all the command
        names that are available.

        Returns an empty list if no commands are defined.
        """
        commands = []
        sub_commands_dir = os.path.join(self.management_dir, "commands")
        sys.path_importer_cache.pop(sub_commands_dir, None)
        for module_loader, name, is_pkg in pkgutil.iter_modules([sub_commands_dir]):
            #if not is_pkg and not name.startswith('_'):
            if is_pkg: commands.append(name)

        return commands

    def load_command_class(self, name):
        """
        Given a command name and an application name, returns the Command
        class instance. All errors raised by the import process
        (ImportError, AttributeError) are allowed to propagate.
        """
        module_path = "wxgigo.management.commands.{0}".format(name)
        try:
            module = import_module(module_path)
        except Exception as e:
            raise

        return module.Command()

    def fetch_command(self, subcommand):
        """
        Tries to fetch the given subcommand, printing a message with the
        appropriate command called from the command line (usually
        "django-admin" or "manage.py") if it can't be found.
        """
        # Get commands outside of try block to prevent swallowing exceptions
        if subcommand not in self.commands:
            sys.stderr.write("Unknown command: %r\nType '%s help' for usage.\n" %
                (subcommand, self.prog_name))
            sys.exit(1)

        klass = self.load_command_class(subcommand)
        return klass
