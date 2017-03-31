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
import os
import shutil

from wxgigo.management.base import BaseCommand, CommandError
from wxgigo.utils.misc import run
from wxgigo.management.commands.deploy.inventory import Inventory
from wxgigo.management.commands.deploy.host import HOST_ROLE_ARGUMENTS


class Command(BaseCommand):
    help = "Deploy running environment for different server roles"

    def add_arguments(self, parser):
        host_role_arguments = ", ".join(HOST_ROLE_ARGUMENTS.keys())
        parser.add_argument('-r', '--host-role', help='server role can be one of: {0}'.format(host_role_arguments ))
        parser.add_argument('-i', '--inventory-file', help="specify inventory host path")

    def get_playbook(self):
        playbook = os.path.join(__path__[0], "site.yaml")
        return playbook

    def get_inventory_info(self, options):
        inventory = None
        inventory_file = options.get('inventory_file')
        if not inventory_file:
            arg_host_role = options.get('host_role')
            inventory = Inventory(arg_host_role)
            inventory.configure()
            inventory.generate()
            inventory_file = inventory.file

        return inventory, inventory_file

    def handle(self, *args, **options):
        try:
            inventory, inventory_file = self.get_inventory_info(options)
            ansible_command = "ansible-playbook -vi {0} {1}".format(
                inventory_file, self.get_playbook()
            )
            run(ansible_command)
        except:
            raise
        finally:
            if inventory:
                shutil.rmtree(inventory.dir)


