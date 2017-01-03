#!/bin/bash
##################################
# Stop WXMP Celery Server daemon #
##################################
celery multi stopwait worker --pidfile=/var/run/celery/%N.pid
