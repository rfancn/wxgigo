import re

# regular pattern to get MsgId
MSGID_REGEX_PATTERN = re.compile("<MsgId>(\d+)</MsgId>")
# regular pattern to get FromUserName
FROMUSERNAME_REGEX_PATTERN = re.compile("<FromUserName>(\w+)</FromUserName>")
# regular pattern to get CreateTime
CREATETIME_REGEX_PATTERN = re.compile("<CreateTime>(\d+)</CreateTime>")

class WXMPRecv(object):
    def __init__(self, request):
        self.type = None

class WXMPRecvFactory(object):
    def __init__(self, request):
        self.request = request

    def get_MsgId(self):
        found = re.findall(MSGID_REGEX_PATTERN, self.request.body)
        if found:
            # in case there exist <MsgId>xxx</MsgId> in <Content> element
            return found[-1]

        return None

    def get_FromUserName(self):
        found = re.findall(FROMUSERNAME_REGEX_PATTERN, self.request.body)
        if found:
            # in case there exist <MsgId>xxx</MsgId> in <Content> element
            return found[-1]

        return None

    def get_CreateTime(self):
        found = re.findall(CREATETIME_REGEX_PATTERN, self.request.body)
        if found:
            # in case there exist <MsgId>xxx</MsgId> in <Content> element
            return found[-1]

        return None

    def get_unique_identifier(self):
        """
        If it is normal message: unique_identifier = MsgId
        If it is event:          unique_identifier = FromUserName + CreateTime
        """
        pass


    def create(self):
        pass
