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
from django.template import loader, Context
from django.core.management.base import CommandError

class WXMPParams(object):
    def __init__(self, config):
        self.config = config

        self.token = None
        self.encoding_aes_key = None
        self.app_id = None
        self.app_secret = None

    def input_token(self):
        input = raw_input("Message encrypt token: ").strip()
        if input:
            self.token = input

    def input_encoding_aes_key(self):
        input = raw_input("Message encrypt encoding AES key: ").strip()
        if input:
            self.encoding_aes_key = input

    def input_app_id(self):
        input = raw_input("Weixin public account app id: ").strip()
        if input:
            self.app_id = input

    def input_app_secret(self):
        input = raw_input("Weixin public account app secret: ").strip()
        if input:
            self.app_secret = input

    def get_inputs(self):
        self.input_token()
        self.input_encoding_aes_key()
        self.input_app_id()
        self.input_app_secret()

    def render_content(self, filename, context={}):
        if not isinstance(context, dict):
            return None

        # template path would be: <root>/wxmp/templates/consumer/celery.py.bak.tmpl
        template_path = "{0}.tmpl".format(self.config.filename)
        t = loader.get_template(template_path)
        c = Context(context)
        return t.render(c)

    def save(self):
        fs_skeleton = (
            # (type, path, content): f indicates file, d indicates directory
            # web/wxmp_bak/config.py
            ('f',  os.path.join(self.config.top_dir, self.config.filename),
                   self.render_content(self.config.filename, context={"params": self.config.params})
            ),
        )

        try:
            for type, path, content in fs_skeleton:
                if type == "d":
                    os.makedirs(path)

                # else if type is file, write here to read clearly
                if type == "f" and content is not None:
                    with open(path, 'w') as f:
                        f.write(content)
        except OSError as e:
            import errno
            if e.errno == errno.EEXIST:
                pass
            else:
                message = e
            raise CommandError(message)
