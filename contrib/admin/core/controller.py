# coding=utf8

import logging
import hashlib
from django.views.decorators.csrf import csrf_exempt
from admin import celery_call

logger = logging.getLogger(__name__)

# Note: pls make sure there is only one mod_wsgi process there,
# otherwise, the variables will not be shared by different http requests
last_msg_md5sum = None


class DuplicateRequestException(Exception):
    pass

class WXMPController(object):
    """
    Main controller which controls how messages/event receives, assembly, dispatch

        1. build receive message or events from HttpRequest which comes from weixin server
        2. pass request.REQUEST + request.body -> celery worker
        3. celery worker returns weixin.result + weixin message
    """
    def __init__(self, request):
        self.request = request
        self.debug_http()

    def debug_http(self):
        http_referer = self.request.META.get('HTTP_REFERER', None)

        http_info_dict = {
            'METHOD' :   self.request.method,
            'PREV URL':  http_referer,
            'CURR URL':  self.request.path,
            'HTTP GET': self.request.GET,
            'HTTP POST': self.request.POST,
            'HTTP BODY': self.request.body
        }

        print_keys = ['METHOD', 'PREV URL', 'CURR URL', 'HTTP GET', 'HTTP POST', 'HTTP BODY']
        http_info = '\n=============\nHTTP INFO\n==========='
        for k in print_keys:
            if k == 'HTTP BODY':
                http_info += '\n{0:10}:\n{1}'.format(k, http_info_dict[k])
            else:
                http_info += '\n{0:10}:\t{1}'.format(k, http_info_dict[k])

        logger.debug(http_info)

    @csrf_exempt
    def is_duplicate_request(self):
        """
        Use md5sum to check if we receives duplicate requset post from Weixin celery_server
        """
        #last_msg_md5sum =  request.session.get('last_msg_md5sum', None)
        global last_msg_md5sum
        current_msg_md5sum = hashlib.md5(self.request.body).hexdigest()
        if last_msg_md5sum is None or current_msg_md5sum != last_msg_md5sum:
            logger.debug("last_msg_md5sum: %s, current_msg_md5sum: %s" % (last_msg_md5sum, current_msg_md5sum))
            last_msg_md5sum = current_msg_md5sum
            return False

        return True

    def server_echo(self):
        """
        Validate signature and return the echostr from Http get message
        It happens when we create or change any configuration in Official Weixin Media Platform,
        just echo what we received can pass the celery_server verification

        :param request:
        :return: empty if cannot find 'echostr'
        """
        echo_string = self.request.GET.get('echostr', None)
        if not echo_string:
            logger.error("Failed to get echostr")
            return ""

        return echo_string

    def dispatch(self):
        """
        Messages handling are in two modes here:

        1. our server(django application deployed) is passive, receives msg/events from Weixin server and reply to it
        2. our server(django application deployed) is active, send msg to  Weixin server

        Here dispatch() only focus on the first one, all received passive POST msg/events will be sent to Celery
        """
        # if receives GET request, then it is Weixin celery_server configure request
        if self.request.method == "GET":
            return self.server_echo()
        # if receives POST request, then it is Weixin message/events post from weixin server
        elif self.request.method == "POST":
            if self.is_duplicate_request():
                return ""

            response = celery_call('api.core.main', (self.request.GET, self.request.POST, self.request.body,))
            return response

        return ""
