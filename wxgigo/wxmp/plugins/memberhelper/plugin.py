# coding=utf-8
import redis

from sdk.plugin.base import BasePlugin
from sdk.plugin import PROCESSING_MODE

from sdk.recv import RECV_CATEGORY, RECV_EVENT_TYPE
from sdk.reply.factory import WXMPReplyShortcut
from sdk.constants import WXMP_FANS_TEAM
from sdk.fans.helper import FansHelper

from celery import Celery

class Plugin(BasePlugin):
    NAME = "MemberHelper"
    VERSION = "0.0.1"
    DESCRIPTION = "This is the plugin to support Member application"
    AUTHOR = "Ryan Fan"

    def is_matched(self, recv):
        if recv.category == RECV_CATEGORY.EVENT and recv.type == RECV_EVENT_TYPE.SCAN:
            return True

        return False

    def join_team(self, my_open_id, promoter_open_id):
        """
        If user joined team before, is it ok to unsubscribe and join to other team?
        so far, this logic doesn't allow this.
        """
        print "{0} join promotion team for: {1}".format(my_open_id, promoter_open_id)

        # get myself's userinfo
        redis_db = redis.Redis(host='localhost')
        fans_helper = FansHelper(redis_db)
        basic_info_dict = fans_helper.get_fans_basic_info(my_open_id)
        print 'user info: {0}'.format(basic_info_dict)

        #redis_db.sadd(WXMP_FANS_TEAM, )

    def process(self, recv):
        """
        1. user now is fans: WXMPRecvScanEvent(Event:SCAN, EventKey: promoter's open_id, Ticket:)
        2. user is not fans, he follow MP before: WXMPRecvScanEvent(Event:subscribe, EventKey:qrscene_promoter's open_id, Ticket:)
        3. user is not fans, he never follow MP before:
        """
        print "in member helper process, from:{0}".format(recv.from_username)
        print "Event:{0}, EventKey:{1}, Ticket:{2}".format(recv.event, recv.event_key, recv.ticket)
        # ignore the scene1 that user who scan promotion QRcode already is fans
        if recv.event == 'SCAN':
            print "[memberhelper.plugin.process()] User:{0} is already fans".format(recv.from_username)
            return
        elif recv.event == 'subscribe':
            promoter_open_id = recv.event_key[len('qrscene_'):]
            self.join_team(recv.from_username, promoter_open_id)

    def get_processing_mode(self):
        return PROCESSING_MODE.ASYNC
