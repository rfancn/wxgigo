from __future__ import absolute_import

import redis
import os
import glob
import ConfigParser
from celery import Celery

import celeryconfig
from sdk.plugin.manager import PluginManager
from sdk.utils import load_module
from sdk.constants import WXMP_ACCESS_TOKEN, WXMP_CONFIG, WXMP_PLUGINS_DIR_NAME

class WXMPCeleryAppConfig(object):
    WXMP_CELERY_APP_CONFIG_FILE = "celeryapp.ini"

    def __init__(self):
        self.appserver_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.plugins_dir = celeryconfig.PLUGINS_HOME
        if not self.plugins_dir:
            raise Exception("Failed to get plugins dir")

class WXMPCeleryApp(Celery):
    def on_init(self):
        """
        Override Celery class's on_init() method
        :return:
        """
        super(WXMPCeleryApp, self).on_init()

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

# Initialize celery app
app = WXMPCeleryApp()
# Initialize other stuff
app.load()