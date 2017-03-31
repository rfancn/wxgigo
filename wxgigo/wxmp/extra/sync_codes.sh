#!/bin/bash
#######################################################
# Update WXMP Celery Server codes from remote dev env #
#######################################################
SSH_USER = test
SSH_PORT = 22
REMOTE_DEV_DIR = /opt/wxgigo/
REMOTE_DEV_HOST = x.x.x.x

rsync -auvzh --delete -e 'ssh -p $SSH_PORT' $SSH_USER@REMOTE_DEV_HOST:$REMOTE_DEV_DIR/* .
find . -name "*" -exec dos2unix {} \;
