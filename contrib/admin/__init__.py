#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2016 Ryan Fan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""
from __future__ import absolute_import

import logging
from celery import Celery
from celery.exceptions import TimeoutError

logger = logging.getLogger(__name__)
CELERY_RESULT_TIMEOUT = 5

CELERY_APP = Celery()
CELERY_APP.config_from_object('django.conf:settings')

def celery_call(task_name, *args):
    try:
        async_result = CELERY_APP.send_task(task_name, *args, retry=False)
        logger.debug("Celery call:{0} send out".format(task_name))
        response = async_result.get(CELERY_RESULT_TIMEOUT)
    except TimeoutError:
        logger.error("Failed to get Celery result in {0} seconds".format(CELERY_RESULT_TIMEOUT))
        return None
    except Exception,e:
        logger.error("Failed to communicate with Celery: {0}".format(e))
        return None

    if isinstance(response, unicode):
        response = response.encode('utf8')

    logger.debug("Celery Server returns: {0}".format(response))
    return response

__all__ = [ celery_call ]

