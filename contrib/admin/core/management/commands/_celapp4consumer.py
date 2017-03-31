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

from web.core.management.commands._celapp import BaseCeleryApp
from web.core.management.commands._celapp import WCMB_DIR_CELAPP, WCMB_FILE_CELAPP, WCMB_FILE_CELCONFIG, WCMB_FILE_PKGINIT

# addtional files for consumer project
WCMB_FILE_C_SCRIPT = "runworker.sh"
WCMB_DIR_C_EXAMPLE = "helloworld"
WCMB_FILE_C_EXAMPLE_TASKS = "tasks.py"

class CeleryConsumerApp(BaseCeleryApp):
    def __init__(self, project):
        super(CeleryConsumerApp, self).__init__(project)

    def get_fs_skeleton(self):
        """
        Build consumer project filesystem skeleton, like:
        <consumer dir>
        |- runworker.sh
        |- libs
             |- __init__.py
             |-  celery.py.bak
             |-  celeryconfig.py
        """
        celeryapp_dir = os.path.join(self.project.dir, WCMB_DIR_CELAPP)
        example_dir = os.path.join(self.project.dir, WCMB_DIR_C_EXAMPLE)
        fs_skeleton = (
            # (type, path, content): f indicates file, d indicates directory
            # <consumer dir>/celerapp/
            ('d', celeryapp_dir, None),
            # libs/__init__.py
            ('f', os.path.join(celeryapp_dir,WCMB_FILE_PKGINIT), ""),
            # libs/celery.py.bak
            ('f', os.path.join(celeryapp_dir,WCMB_FILE_CELAPP), self.render_content(WCMB_FILE_CELAPP)),
            # libs/celeryconfig.py
            ('f', os.path.join(celeryapp_dir,WCMB_FILE_CELCONFIG),
                  self.render_content(WCMB_FILE_CELCONFIG, context={'mb': self.project.mb})
            ),
            # <root>/runworker.sh
            ('f', os.path.join(self.project.dir,WCMB_FILE_C_SCRIPT), self.render_content(WCMB_FILE_C_SCRIPT)),
            # generate helloworld tasks template
            ('d', example_dir, None),
            ('f', os.path.join(example_dir, WCMB_FILE_PKGINIT), ""),
            ('f', os.path.join(example_dir, WCMB_FILE_C_EXAMPLE_TASKS), self.render_content(WCMB_FILE_C_EXAMPLE_TASKS)),
        )
        return fs_skeleton