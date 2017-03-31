import logging

from web.admin.plugin.models import WXMPPlugin

from celery_server.sdk.plugin.helper import PluginHelper

logger = logging.getLogger(__name__)

class PluginAction(object):
    def __init__(self, plugin_uuid):
        self.plugin_uuid = plugin_uuid
        self.name = None
        self.plugin_helper = PluginHelper()
        self.errmsg = None

    def db_action(self):
        raise NotImplementedError

    def get_result(self):
        result = {}

        if not self.errmsg:
            result['status'] = 'success'
            return result

        result['status'] = 'error'
        result['errmsg'] = self.errmsg
        return result

    def perform(self):
        self.db_action()

class ActivePluginAction(PluginAction):
    def __init__(self, plugin_uuid):
        super(ActivePluginAction, self).__init__(plugin_uuid)
        self.name = "active"

    def db_action(self):
        try:
            plugin = WXMPPlugin.objects.get(pk=self.plugin_uuid)
        except WXMPPlugin.DoesNotExist:
            plugin = None

        if plugin is None:
            found = self.plugin_helper.find_fs_plugin(self.plugin_uuid)
            if found is None:
                logger.error("Failed to find corresponding filesystem plugin")
                self.errmsg = "Failed to find corresponding filesystem plugin"
                return False

            # if found
            new_db_plugin = WXMPPlugin(found.uuid, found.name, found.pattern, found.version, True)
            new_db_plugin.save()
            return True

         # else we found it in db
        plugin.enabled = True
        plugin.save()
        return True

class DeactivePluginAction(PluginAction):
    def __init__(self, plugin_uuid):
        super(DeactivePluginAction, self).__init__(plugin_uuid)
        self.name = "deactive"

    def db_action(self):
        try:
            plugin = WXMPPlugin.objects.get(pk=self.plugin_uuid)
        except WXMPPlugin.DoesNotExist:
            plugin = None

        # do nothing if it is not in db
        if plugin is None:
            return True

        plugin.enabled = False
        plugin.save()
        return True

class ConfigPluginAction(PluginAction):
    def __init__(self, plugin_uuid):
        super(ConfigPluginAction, self).__init__(plugin_uuid)
        self.name = "config"

    def db_action(self):
        logger.debug("config: {0}".format(self.name))

class PluginActionFactory(object):
    def __init__(self, action_name, plugin_uuid):
        self.action_name = action_name
        self.plugin_uuid = plugin_uuid

    def create(self):
        if self.action_name == "active":
            return ActivePluginAction(self.plugin_uuid)
        elif self.action_name == "deactive":
            return DeactivePluginAction(self.plugin_uuid)
        elif self.action_name == "config":
            return ConfigPluginAction(self.plugin_uuid)
