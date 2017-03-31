#!/bin/bash
######################################
# Run WXMP Celery Server in cli mode #
######################################
celery worker -c 1 -B -s /tmp/celerybeat-schedule -A celeryapp -l debug
