import logging
logger = logging.getLogger(__name__)

from sdk.plugin.dbhelper import DBPluginHelper
from sdk.plugin.fshelper import FSPluginHelper

class PluginHelper(DBPluginHelper, FSPluginHelper):
    def __init__(self, app):
        super(PluginHelper, self).__init__(app)

    def new_plugin_instance(self, plugin_name):
        plugin_class = self.fs_get_plugin_class(plugin_name)
        if not plugin_class:
            return None

        try:
            # if we can find plugin_config, try new it
            plugin_config = None
            plugin_config_class = self.fs_get_plugin_config_class(plugin_name)
            if plugin_config_class:
                plugin_config = plugin_config_class()
                settings = self.db_get_config_settings(plugin_name)
                plugin_config.loads(settings)

            plugin_instance = plugin_class(config=plugin_config)
        except Exception,e:
            raise e

        return plugin_instance