#!/bin/bash
######################################
# Run WXMP Celery Server in cli mode #
######################################
celery worker -c 1 -B -A celeryapp -l debug
