#!/usr/bin/env python
# coding=utf-8
from sdk.recv.base import WXMPRecvMsg
from sdk.recv import RECV_MSG_TYPE

class WXMPRecvVideoMsg(WXMPRecvMsg):
    def __init__(self, core):
        super(WXMPRecvVideoMsg, self).__init__(core)
        self.type = RECV_MSG_TYPE.VIDEO

        self.thumb_media_id = self.meta.get('ThumbMediaId', None)
        if not self.thumb_media_id:
            raise Exception("Failed to initialize WXMPRecvVideoMsg because ThumbMediaId doesn't exist!")

        self.media_id = self.meta.get('MediaId', None)
        if not self.media_id:
            raise Exception("Failed to initialize WXMPRecvVideoMsg because MediaId doesn't exist!")

    def debug(self):
        print "{0}(MediaId:{1}, ThumbMediaId:{2})".format(
            self.__class__.__name__,
            self.media_id,
            self.thumb_media_id)


