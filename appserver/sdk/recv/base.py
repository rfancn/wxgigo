#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import
from datetime import datetime
from sdk.recv import RECV_CATEGORY, RECV_MSG_TYPES

############################################################
# Recv Object
############################################################
class WXMPRecvCore(object):
    def __init__(self, xml_dict):
        # meta info is a reply dict which parsed from Http Request
        self.meta = xml_dict
        self.init_common_parameters()

    def get_category(self, msg_type):
        category = RECV_CATEGORY.UNKNOWN

        if  msg_type.lower() == "event":
            category = RECV_CATEGORY.EVENT
        elif self.msg_type.lower()  in RECV_MSG_TYPES:
            category = RECV_CATEGORY.MESSAGE

        return category

    def init_common_parameters(self):
        # get common elements and validate them
        self.msg_type = self.meta.get("MsgType", None)
        if not self.msg_type:
           raise Exception("Failed to initialize WXMPRecvCore because MsgType doesn't exist!")

        self.to_username = self.meta.get("ToUserName", None)
        if not self.to_username:
            raise Exception("Failed to initialize WXMPRecvCore because ToUsername doesn't exist!")

        self.from_username = self.meta.get("FromUserName", None)
        if not self.from_username:
            raise Exception("Failed to initialize WXMPRecvCore because FromUsername doesn't exist!")

        create_time = self.meta.get("CreateTime", None)
        if not create_time:
            raise Exception("Failed to initialize WXMPRecvCore because CreateTime doesn't exist!")

        try:
            self.create_time = datetime.fromtimestamp(int(create_time))
        except Exception,e:
            raise Exception("Failed to initialize WXMPRecvCore because CreateTime is invalid!")

        self.category = self.get_category(self.msg_type)

class WXMPBaseRecv(object):
    def __init__(self, core):
        # copy all WXMPRecvCore variables
        for (k, v) in core.__dict__.items():
            if not k.startswith("__"):
                self.__dict__[k] = v

    def debug(self):
        raise NotImplementedError

class WXMPRecvMsg(WXMPBaseRecv):
    def __init__(self, core):
        self.msg_id = core.meta.get('MsgId', None)
        if not self.msg_id:
            raise Exception("Failed to initialize WXMPRecvMsg because MsgId doesn't exist!")

        super(WXMPRecvMsg, self).__init__(core)

class WXMPRecvEvent(WXMPBaseRecv):
    def __init__(self, core):
        super(WXMPRecvEvent, self).__init__(core)



