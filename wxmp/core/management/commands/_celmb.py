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
class BaseMB(object):
    def __init__(self):
        self.type = None
        self.location = "127.0.0.1"
        self.port = None
        self.username = "guest"
        self.password = None

    def get_broker_url(self):
        url_template = "{0}://{1}@{2}:{3}//"
        secret_url_template = "{0}://{1}:{2}@{3}:{4}//"

        if self.password:
            return secret_url_template.format(
                self.type,
                self.username,
                self.password,
                self.location,
                self.port,
            )

        return url_template.format(
            self.type,
            self.username,
            self.location,
            self.port,
        )

    def get_result_backend(self):
        raise NotImplementedError

    def input_location(self):
        input = raw_input("Message broker hostname or IP[{0}]: ".format(self.location)).strip()
        if input:
            self.location = input

    def input_port(self):
        input = raw_input("Message broker port[{0}]: ".format(self.port)).strip()
        if input:
            self.port = input

    def input_username(self):
        input = raw_input("Message broker username[{0}]: ".format(self.username)).strip()
        if input:
            self.username = input

    def input_password(self):
        input = raw_input("Message broker password[{0}]: ".format(self.password)).strip()
        if input:
            self.password = input

    def get_inputs(self):
        self.input_location()
        self.input_port()
        self.input_username()
        self.input_password()

    def proceed(self):
        self.broker_url = self.get_broker_url()
        self.result_backend = self.get_result_backend()

class MBRedis(BaseMB):
    def __init__(self):
        super(MBRedis, self).__init__()
        self.type = "redis"
        self.port = "6379"
        self.dbname = '0'

    def input_dbname(self):
        input = raw_input("Result backend DB name[{0}]: ".format(self.dbname)).strip()
        if input:
            self.dbname = input

    def get_inputs(self):
        super(MBRedis, self).get_inputs()
        self.input_dbname()

    def get_result_backend(self):
        """
        'redis://:password@host:port/db'
        """
        result_backend = "redis://{0}:{1}/{2}"
        secret_result_backend = "redis://:{0}@{1}:{2}/{3}"

        if self.password:
            return secret_result_backend.format(
                self.password,
                self.location,
                self.port,
                self.dbname,
            )

        return result_backend.format(
                self.location,
                self.port,
                self.dbname,
        )

class MBRabbitMQ(BaseMB):
    def __init__(self):
        super(MBRabbitMQ, self).__init__()
        self.type = "amqp"
        self.port = "5672"

    def get_result_backend(self):
        """
        'redis://:password@host:port/db'
        """
        return "amqp"


MESSAGE_BROKER_CLASSES = {
    'redis': MBRedis,
    'rabbitmq': MBRabbitMQ,
}
class CeleryMBFactory(object):
    """
    Message Broker(MB) Config Factory class
    """
    def __init__(self, project):
        self.project = project

    def create(self):
        mb = None
        try:
            type = self.project.mb_type.strip().lower()
            mb = MESSAGE_BROKER_CLASSES[type]()
        except:
            pass

        return mb

