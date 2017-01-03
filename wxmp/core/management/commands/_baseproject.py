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
from distutils.version import LooseVersion
import django
from django.core.management.base import CommandError


from web.core.management.commands._celmb import CeleryMBFactory
from web.core.management.commands._celapp4consumer import CeleryConsumerApp
from web.core.management.commands._celapp4producer import CeleryProducerApp

LEGACY_MODE = LooseVersion(django.get_version()) < LooseVersion("1.8")

DEFAULT_BROKER_TYPE = "redis"
SUPPORTED_BROKER_TYPES = ["redis", "rabbitmq"]
APP_CLASSES = {
    "consumer": CeleryConsumerApp,
    "producer": CeleryProducerApp,
}
class BaseProject(object):
    def __init__(self):
        self.mb_type = self.get_mb_type()
        self.mb = CeleryMBFactory(self).create()
        self.app = APP_CLASSES[self.type](self)

    def get_mb_type(self):
        mb_type = DEFAULT_BROKER_TYPE
        input = raw_input("Message broker type[{0}]: ".format(mb_type)).strip()
        if input:
            mb_type = input

        if mb_type not in SUPPORTED_BROKER_TYPES:
            raise CommandError("Unsupported message broker type!")

        return mb_type

    def get_inputs(self):
        self.mb.get_inputs()
        self.app.get_inputs()

    def proceed(self):
        """
        Proceed inputs according to requirements
        """
        self.mb.initialize()

    def save(self):
        #self.mb.save()
        self.app.save()

    def config(self):
        self.get_inputs()
        self.proceed()
        self.save()

    def test(self):
        print self.mb.get_broker_url()







