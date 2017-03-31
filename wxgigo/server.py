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

from celery import Celery

class WxgigoServer(Celery):
    def on_init(self):
        """
        Override Celery class's on_init() method
        :return:
        """
        super(WxgigoServer, self).on_init()

        self.config_from_object(celeryconfig)
        self.config = WXMPCeleryAppConfig()
        self.db = self.get_db()

    def get_db(self):
        # if doesnt' define result backend, which means we may not be able to persistent configuration
        if not getattr(celeryconfig, 'CELERY_RESULT_BACKEND'):
            return None

        try:
            # 'redis://127.0.0.1:6379/0'
            tmp_list = celeryconfig.CELERY_RESULT_BACKEND.split("//")[-1].split("/")
            hoststr = tmp_list[0]
            db = tmp_list[1]
            host = hoststr.split(":")[0]
            port = hoststr.split(":")[1]
        except Exception,e:
            print "{0}{1}{2}".format(host, port, db)
            raise e

        return redis.Redis(host=host, port=port, db=db)

    def get_token(self):
        return self.db.hget(WXMP_CONFIG, 'TOKEN')

    def get_access_token(self):
        return self.db.hget(WXMP_ACCESS_TOKEN, 'access_token')

    def load(self):
        """
        Assign helper and other useful instance to app

        :param app:
        :return:
        """
        self.plugin_manager = PluginManager(self)
        #app.web_helper = WebHelper(app.db)

        # import all celery tasks as API
        self.load_apis()

    def load_apis(self):
        """
        Load all celery tasks

        :param api_base_dir:
        :return:
        """
        API_DIR = "api"
        api_files = os.path.join(API_DIR, "*.py")
        for filepath in glob.glob(api_files):
            if "__init__.py" in filepath:
                continue

            try:
                # convert "api/menu.py" filepath to "api.menu" module format
                api_module = ".".join(os.path.split(filepath))[:-len(".py")]
                print "Try to load {0}".format(api_module)
                load_module(api_module)
            except Exception, e:
                print e

def main():
    print "wxgigo server"
