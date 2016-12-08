#!/usr/bin/bash

DEBUG=false
DIST_BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export DIST_BASE_DIR

source $DIST_BASE_DIR/libs/functions
fn_detect_dist_dir

sh $DIST_BASE_DIR/roles/default/$DIST_DIR/init_env.sh
if [ $? -ne 0 ]; then
    echo "Error setup deployment env!"
    exit 1
fi
cd $DIST_BASE_DIR && python deploy.py


