# coding=utf-8

from sdk.utils import load_class
from sdk.reply import REPLY_CATEGORY, REPLY_PASSIVE_TYPE, REPLY_SERVICE_TYPE

class WXMPSendFactory(object):
    def __init__(self, recv, category, type):
        self.recv = recv
        self.category = category
        self.type = type

    def get_class(self):
        module_path = "sdk.send.{0}.{1}".format(self.category, self.type)
        class_name = "WXMP{0}Send{1}".format(self.category.title(), self.type.title())
        try:
            cls = load_class(module_path, class_name)
        except Exception,e:
            raise Exception("Failed to load class:%s from:%s" % (class_name, module_path))

        return cls

    def create(self, **kwargs):
        klass = self.get_class()
        instance = klass(self.recv)
        if not instance.validate(kwargs):
            return ""

        instance.assembly(kwargs)
        return instance


class WXMPSendShortcut(object):
    def __init__(self, recv):
        self.recv = recv

    def get_factory(self, category, type):
        return WXMPSendFactory(self.recv, category, type)

    def createServiceText(self, content):
        kwargs = {'content': content}
        return self.get_factory(REPLY_CATEGORY.PASSIVE, REPLY_PASSIVE_TYPE.TEXT).create(**kwargs)

    def createServiceImage(self, media_id):
        kwargs = {'media_id': media_id}
        return self.get_factory(REPLY_CATEGORY.PASSIVE, REPLY_PASSIVE_TYPE.IMAGE).create(**kwargs)
