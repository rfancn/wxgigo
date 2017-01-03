#!/usr/bin/env python
# coding=utf-8

from sdk.recv.base import WXMPRecvMsg
from sdk.recv import RECV_MSG_TYPE

class WXMPRecvImageMsg(WXMPRecvMsg):
    def __init__(self, core):
        super(WXMPRecvImageMsg, self).__init__(core)
        self.type = RECV_MSG_TYPE.IMAGE

        self.pic_url = self.meta.get('PicUrl', None)
        if not self.pic_url:
            raise Exception("Failed to initialize WXMPRecvImageMsg because PicUrl doesn't exist!")

        self.media_id = self.meta.get('MediaId', None)
        if not self.media_id:
            raise Exception("Failed to initialize WXMPRecvImageMsg because MediaId doesn't exist!")

    def debug(self):
        print "{0}(PicUrl:{1}, MediaId:{2})".format(
            self.__class__.__name__,
            self.pic_url,
            self.media_id)
