#!/usr/bin/bash

source $DIST_BASE_DIR/libs/functions

PIP_INDEX=https://pypi.douban.com/simple
SYS_PKGS="gcc openssl-devel python-devel epel-release python2-pip"
PYTHON_PKGS="fabric cuisine monitoring"

install_basic_sys_packages()
{
    #YUM_OPTS="-y -q"
    #case "$DEBUG" in
    #    'true') YUM_OPTS="-y";;
    #esac

    YUM_OPTS="-y"
    for pkg in $SYS_PKGS;do
        rpm -q $pkg > /dev/null
        if [ $? -ne 0 ]; then
            fn_action "* Install basic system package:" yum install $YUM_OPTS $pkg
            if [ $? -ne 0 ]; then
                exit 1
            fi
        fi
    done

}

upgrade_pip()
{
    # show pip version
    pip -V > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "No pip found, please install it!"
        exit 1
    fi

    PIP_UPGRADE_CMD="pip -q install --upgrade pip"
    if [ "$PIP_INDEX" != "" ]; then
        PIP_UPGRADE_CMD="pip -q install --upgrade pip -i $PIP_INDEX"
    fi
    fn_action "* Upgrade pip if needed: " $PIP_UPGRADE_CMD
    if [ $? -ne 0 ]; then
        echo "pip upgradation failed!"
        exit 1
    fi
}

install_basic_python_packages()
{
    PIP_INSTALL_CMD="pip install"
    if [ "$PIP_INDEX" != "" ]; then
        PIP_INSTALL_CMD="pip install -i $PIP_INDEX"
    fi

    PIP_OPTS=""
    #case "$DEBUG" in
    #    'true') PIP_OPTS="";;
    #esac

    fn_action "* Install basic python packages: " $PIP_INSTALL_CMD $PIP_OPTS $PYTHON_PKGS
}


install_basic_sys_packages
upgrade_pip
install_basic_python_packages

# execute main deploy routine
# fab deploy:dist_base_dir=$DIST_BASE_DIR