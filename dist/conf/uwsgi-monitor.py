#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) <2015-2016> <Ryan Fan>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
__version__ = "0.0.1"

import signal
import pyinotify
import sys
import os
import pwd
import ConfigParser

UWSGI_GLOBAL_CONFIG_FILE = "/etc/uwsgi.ini"

# global pid filename and log filename
g_pid_file = None
g_log_file = None

def handleExit(signum, stack):
    try:
        os.remove(g_pid_file)
        os.remove(g_log_file)
    except:
        sys.exit(1)

    sys.exit(0)

class TouchEventHandler(pyinotify.ProcessEvent):
    def my_init(self, target):
        self.target = target

    def __pflush(self, str):
        sys.stdout.write(str+"\n")
        sys.stdout.flush()

    def __touch_target(self):
        try:
            if os.path.exists(self.target):
                os.utime(self.target, None)
                self.__pflush("Successfully touch existed target:%s!" % self.target)
            else:
                open(self.target, 'a').close()
                self.__pflush("Successfully touch new target:%s!" % self.target)
        except Exception,e:
            self.__pflush("Failed to touch target because of:%s!" % self.target)
            return False

        return True

    def process_default(self, event):
        self.__pflush("event: %s" % event)
        if not event.name.endswith(".py"):
           return

        self.__touch_target()


def get_monitor_base_filename(monitor_dir):
    """
    Generate base filename which used to generate g_pid_file and g_log_file for monitor daemon
    :param monitor_dir:
    :return:
    """
    abs_monitor_dir = os.path.abspath(monitor_dir)
    filename = os.path.basename(abs_monitor_dir)
    if not filename:
        filename = os.getpid()

    return filename

def watch(monitor_dir):
    if not os.path.exists(monitor_dir):
        print "Monitor directory: %s doens't exist!" % monitor_dir
        sys.exit(1)

    signal.signal(signal.SIGINT, handleExit)
    signal.signal(signal.SIGQUIT, handleExit)
    signal.signal(signal.SIGTERM, handleExit)

    event_handler = TouchEventHandler(target=monitor_dir)
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, default_proc_fun=event_handler)


    flags = pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_MODIFY | pyinotify.IN_MOVED_TO
    wm.add_watch(monitor_dir, flags, rec=True, auto_add=True)

    try:
        notifier.loop(daemonize=True, pid_file=g_pid_file, stdout=g_log_file)
    except pyinotify.NotifierError, err:
        raise err

def validate_uwsgi_ini_file(monitor_dir):
    if not os.path.exists(monitor_dir):
        print "uWSGI monitor dir: '%s' doesn't exist!" % monitor_dir
        return False

    # check if we have uwsgi config file in /etc/uwsgi.d/ dir
    uwsgi_global_config = ConfigParser.ConfigParser()
    uwsgi_global_config.read(UWSGI_GLOBAL_CONFIG_FILE)
    if not uwsgi_global_config:
        print "Failed to find uwsgi global config file in %s" % UWSGI_GLOBAL_CONFIG_FILE
        return False

    emperor_dir = None
    for sec in uwsgi_global_config.sections():
        for k,v in uwsgi_global_config.items(sec):
            if k.lowercase().strip() == 'emperor':
                emperor_dir = uwsgi_global_config.get(sec, k)
                break

    if not emperor_dir:
        print "Failed to find uwsgi emperor dir in uwsgi global config file"
        return False

    uwsgi_project_config_file = None
    uwsgi_project_config = ConfigParser.ConfigParser()
    try:
        for fname in os.listdir(emperor_dir):
            fname_with_realpath = os.path.realpath(fname)
            if os.path.isfile(fname_with_realpath):
                uwsgi_project_config.read(fname_with_realpath)

    except:
        pass


    if not uwsgi_ini_file:
        print "Failed to find uwsgi config file"
        return False

    # check if we have setup touch-reload
    found_touch_reload = False
    with open(uwsgi_ini_file, 'r') as f:
        for line in f.readlines():
            if line.strip().startswith('touch-reload'):
                found_touch_reload = True
                break

    if not found_touch_reload:
        print "Failed to locate 'touch-reload' option in uwsgi config file"
        return False

    return True
re
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
    It must be "yes" (the default), "no" or None (meaning an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n]: "
    elif default == "yes":
        prompt = " [Y/n]: "
    elif default == "no":
        prompt = " [y/N]: "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")

def get_monitor_dir():
    if len(sys.argv) < 2:
        print "You don't specify MONITOR_DIR!"
        guess_monitor_dir = os.getcwd()
        answer = query_yes_no("Are you intend to check for changes under dir: '%s'?" % guess_monitor_dir)
        if answer is False:
            return None

        return guess_monitor_dir
    elif len(sys.argv) == 2:
        return os.path.abspath(sys.argv[1])

    return None

if __name__ == "__main__":
    monitor_dir = get_monitor_dir()
    if not monitor_dir:
        print ""
        print "Invalid option, please use below syntax:\n$ python %s [MONITOR_DIR]\n" % __file__
        sys.exit(1)

    validate_ok = validate_uwsgi_ini_file(monitor_dir)
    if not validate_ok:
        sys.exit(1)

    # setup pid filename and log filename
    base_monitor_filename = get_monitor_base_filename(monitor_dir) + "-monitor"
    g_pid_file = os.path.join("/tmp", base_monitor_filename + ".pid")
    g_log_file = os.path.join("/tmp", base_monitor_filename + ".log")

    print "uWSGI Monitor started, all changes under: '%s' will cause uWSGI reload!" % monitor_dir
    watch(monitor_dir)


