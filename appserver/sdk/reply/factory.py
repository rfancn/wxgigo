# coding=utf-8

from sdk.utils import load_class
from sdk.reply import REPLY_CATEGORY, REPLY_PASSIVE_TYPE, REPLY_SERVICE_TYPE

class WXMPReplyFactory(object):
    def __init__(self, recv, category, type):
        self.recv = recv
        self.category = category
        self.type = type

    def get_class(self):
        module_path = "sdk.reply.{0}.{1}".format(self.category, self.type)
        class_name = "WXMP{0}Reply{1}".format(self.category.title(), self.type.title())
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


class WXMPReplyShortcut(object):
    def __init__(self, recv):
        self.recv = recv

    def get_factory(self, category, type):
        return WXMPReplyFactory(self.recv, category, type)

    def createPassiveText(self, content):
        kwargs = {'content': content}
        return self.get_factory(REPLY_CATEGORY.PASSIVE, REPLY_PASSIVE_TYPE.TEXT).create(**kwargs)

    def createPassiveImage(self, media_id):
        kwargs = {'media_id': media_id}
        return self.get_factory(REPLY_CATEGORY.PASSIVE, REPLY_PASSIVE_TYPE.IMAGE).create(**kwargs)

    def createPassiveMusic(self, media_id, title='', description='', music_url='#', hq_music_url=''):
        kwargs = {'media_id': media_id, 'title':title, 'description': description,
                  'music_url': music_url, 'hq_music_url': hq_music_url}
        return self.get_factory(REPLY_CATEGORY.PASSIVE, REPLY_PASSIVE_TYPE.MUSIC).create(**kwargs)

    def createPassiveVideo(self, media_id, title='', description=''):
        kwargs = {'media_id': media_id, 'title':title, 'description': description}
        return self.get_factory(REPLY_CATEGORY.PASSIVE, REPLY_PASSIVE_TYPE.VIDEO).create(**kwargs)

    def createPassiveVoice(self, media_id):
        kwargs = {'media_id': media_id}
        return self.get_factory(REPLY_CATEGORY.PASSIVE, REPLY_PASSIVE_TYPE.VOICE).create(**kwargs)

    def createPassiveNews(self, articles):
        kwargs = {'articles': articles}
        return self.get_factory(REPLY_CATEGORY.PASSIVE, REPLY_PASSIVE_TYPE.NEWS).create(**kwargs)

    def createServiceText(self, content):
        kwargs = {'content': content}
        return self.get_factory(REPLY_CATEGORY.SERVICE, REPLY_SERVICE_TYPE.TEXT).create(**kwargs)






