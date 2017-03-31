#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

from sdk.recv.base import WXMPRecvMsg
from sdk.recv import RECV_MSG_TYPE

class WXMPRecvTextMsg(WXMPRecvMsg):
    def __init__(self, core):
        super(WXMPRecvTextMsg, self).__init__(core)
        self.type = RECV_MSG_TYPE.TEXT
        self.content = self.meta.get('Content', None)
        if not self.content:
            raise Exception("Failed to initialize WXMPRecvTextMsg because <Content> doesn't exist!")

    def debug(self):
        print "{0}(Content:{1})".format(
            self.__class__.__name__,
            self.content.encode("utf8"))


