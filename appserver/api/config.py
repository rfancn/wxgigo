from __future__ import absolute_import

from celery import shared_task, Task

from sdk.constants import *

@shared_task
def save(recv):
    if not isinstance(recv, dict):
        print "%s\n%s" % (type(recv), recv)
        print "Invalid Weixin MediaPlatform configuration."
        return False

    recv_keys = recv.keys()
    valid_keys = [ k for k in recv_keys if k in WXMP_CONFIG_REQUIRED_KEYS ]
    if len(valid_keys) != len(WXMP_CONFIG_REQUIRED_KEYS):
        print "Not all required configuration items received"
        print "recv keys: %s" % recv_keys
        print "valid keys: %s" % valid_keys
        return False

    redis_db = Task.app.db
    redis_db.hmset(WXMP_CONFIG, recv)
    redis_db.save()
    return True

@shared_task
def load():
    reply = Task.app.db.hgetall(WXMP_CONFIG)
    return reply

