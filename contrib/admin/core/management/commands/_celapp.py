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
import errno
from django.core.management.base import CommandError
from django.template import loader, Context

# common global definition
WCMB_DIR_CELAPP = "libs"
WCMB_FILE_CELAPP = "celery.py"
WCMB_FILE_CELCONFIG = "celeryconfig.py"
WCMB_FILE_PKGINIT = "__init__.py"

class BaseCeleryApp(object):
    def __init__(self, project):
        self.project = project

    def render_content(self, filename, context={}):
        if not isinstance(context, dict):
            return None

        # template path would be: <root>/wxmp/templates/consumer/celery.py.bak.tmpl
        template_path = os.path.join(self.project.type, "{0}.tmpl".format(filename))
        t = loader.get_template(template_path)
        c = Context(context)
        return t.render(c)

    def get_inputs(self):
        pass

    def get_fs_skeleton(self):
        raise NotImplementedError

    def save(self):
        fs_skeleton = self.get_fs_skeleton()
        try:
            for type, path, content in fs_skeleton:
                if type == "d":
                    os.makedirs(path)

                # else if type is file, write here to read clearly
                if type == "f" and content is not None:
                    with open(path, 'w') as f:
                        f.write(content)
        except OSError as e:
            if e.errno == errno.EEXIST:
                message = "'%s' already exists" % self.project.dir
            else:
                message = e
            raise CommandError(message)



