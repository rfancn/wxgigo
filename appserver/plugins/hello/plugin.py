# coding=utf-8

from sdk.plugin.base import BasePlugin
from sdk.plugin import PROCESSING_MODE

from sdk.recv import RECV_CATEGORY, RECV_MSG_TYPE
from sdk.reply.factory import WXMPReplyShortcut
from sdk.obj.article import WXMPArticle

class Plugin(BasePlugin):
    NAME = "Hello"
    VERSION = "0.0.1"
    DESCRIPTION = "This is a hello world test"
    AUTHOR = "Ryan Fan"

    def is_matched(self, recv):
        if recv.category == RECV_CATEGORY.MESSAGE and recv.type == RECV_MSG_TYPE.TEXT:
            if "hello" in recv.content:
                print "Hello plugin matched!"
                return True

        return False

    def process(self, recv):
        print "in hello process"
        return self.test_text(recv)

    def get_processing_mode(self):
        return PROCESSING_MODE.SYNC

    def test_article(self, recv):
        article = WXMPArticle("#",  title="test_title", description="test_description",
                    pic_url="http://mmbiz.qpic.cn/mmbiz/wiagR9BxxI4IGtJWqX6gicFZyx1yrp9dWAjTqC1yMxIk8seyk3tmnUuF3F6YXofbPzxsbQPyfMehZ1xsVMc9ZIXw/0")

        articles = [ article ]
        return WXMPReplyShortcut(recv).createPassiveNews(articles)

    def test_text(self, recv):
        return WXMPReplyShortcut(recv).createPassiveText("servicetext")

    def test_video(self, recv):
        return WXMPReplyShortcut(recv).createPassiveVideo("CJEzG62SQFYGBpZjKPClpgzaFCoZjy0Rkw5y4anG1IcPlUBysyyNwKr6WQ9kUFIs")

    def test_music(self, recv):
        return WXMPReplyShortcut(recv).createPassiveMusic("aWrDDosvm-B6_QkKGnx19ToLcpSOImfzThu6IF1RyLzB8_yZvBOY5MNWoY56kct3",
                                                          music_url = "http://win.web.rf01.sycdn.kuwo.cn/184bb5acbaaf54bb644bba496160b8f7/575d979b/resource/n1/31/44/368155432.mp3")



