#!/bin/bash
#########################################
# Run WXMP Celery Server in daemon mode #
#########################################
celery multi start worker --verbose -c 3 -B -s /tmp/celerybeat-schedule -A celeryapp -l debug --pidfile=/var/run/celery/%N.pid --logfile=/var/log/celery/%N.log

