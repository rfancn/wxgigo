#!/usr/bin/env python
# coding=utf-8
from sdk.recv.base import WXMPRecvMsg
from sdk.recv import RECV_MSG_TYPE

class WXMPRecvVoiceMsg(WXMPRecvMsg):
    def __init__(self, core):
        super(WXMPRecvVoiceMsg, self).__init__(core)
        self.type = RECV_MSG_TYPE.VOICE

        self.format = self.meta.get('Format', None)
        if not self.format:
            raise Exception("Failed to initialize WXMPRecvVoiceMsg because PicUrl doesn't exist!")

        self.media_id = self.meta.get('MediaId', None)
        if not self.media_id:
            raise Exception("Failed to initialize WXMPRecvVoiceMsg because MediaId doesn't exist!")

        # recognition only exist when Voice Recognition function was enabled
        self.recognition = self.meta.get('Recognition', None)

    def debug(self):
        print "{0}(Format:{1}, MediaId:{2}, Recognition:{3})".format(
            self.__class__.__name__,
            self.format,
            self.media_id,
            self.recognition.encode("utf8"))



