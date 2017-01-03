# coding=utf-8
from __future__ import absolute_import

import hashlib
import requests
import threading

from celery import Task, shared_task

from sdk.plugin import PROCESSING_MODE
from sdk.recv.factory import WXMPRecvFactory
from sdk.reply.factory import WXMPReplyShortcut
from sdk.reply.base import WXMPReply

class BaseCoreTask(Task):
    abstract = True
    # Note: if token config changed,
    # it need restart celery server to make new setting take effect
    # here, for performance consideration, get token when task module loaded
    token = Task.app.get_token()

class main(BaseCoreTask):
    def __calculate_signature(self, timestamp, nonce, token):
        tmp_array = [token, timestamp, nonce]
        # if any element in above tmp_array is empty, just return empty signature
        # Note: only support after python2.5
        if not all(tmp_array):
            return None

        tmp_array.sort()
        return hashlib.sha1("".join(tmp_array)).hexdigest()

    def __validate_signature(self, http_get):
        timestamp = http_get.get('timestamp', None)
        nonce = http_get.get('nonce', None)
        signature = http_get.get('signature', None)

        if not all([timestamp, nonce, self.token, signature]):
            return False

        expected_signature = self.__calculate_signature(timestamp, nonce, self.token)
        return signature == expected_signature

    def run(self, http_get, http_post, http_body):
        """
        @param:http_get   dict of http request.get
        @param:http_post  dict of http request.post
        @param:http_body  string of http request.body
        """
        if not self.__validate_signature(http_get):
            return ""

        recv = WXMPRecvFactory(http_body).create()

        # find matched plugins
        plugin = self.app.plugin_manager.find_plugin(recv)
        if not plugin:
            return ""

        processing_mode = plugin.get_processing_mode()
        if processing_mode == PROCESSING_MODE.SYNC:
            reply = plugin.process(recv)
            if not reply or not isinstance(reply, WXMPReply):
                return ""

            return reply.content
        elif processing_mode == PROCESSING_MODE.ASYNC:
            w = threading.Thread(name='async_worker', target=plugin.process, args=(recv,))
            w.start()

            passive_text_reply = WXMPReplyShortcut(recv).createPassiveText(u'请求已收到，处理中...')
            return passive_text_reply.content

        return ""

@shared_task
def send_service_reply(reply_content):
    print "customer service reply"
    access_token = Task.app.get_access_token()
    url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}".format(access_token)
    resp = requests.post(url, data=reply_content)
    result = resp.json()
    if resp.status_code == 200 and result['errcode'] == 0:
        print "Send customer service reply succeed: {0}".format(resp.content)
    else:
        print "Failed to send customer service reply: {0}".format(resp.content)