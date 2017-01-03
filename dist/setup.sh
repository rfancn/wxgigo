#!/usr/bin/bash

DEBUG=false
DIST_BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export DIST_BASE_DIR

source $DIST_BASE_DIR/libs/functions
fn_detect_dist_dir

sh $DIST_BASE_DIR/roles/default/$DIST_DIR/init_env.sh
cd $DIST_BASE_DIR && python deploy.py


