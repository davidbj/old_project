#!/usr/bin/python
#-*- coding:utf-8 -*-

import urllib
import os
import sys
from subprocess import Popen, PIPE, check_call
import shutil
import time
import datetime
from os import path
from optparse import OptionParser
import signal

DIRNAME = path.dirname(__file__)
OPSTOOLS_DIR = path.abspath(DIRNAME)
sys.path.append(OPSTOOLS_DIR)
from daemonize import daemonize

LASTVERSION = 'http://133.96.7.120/lastver'
RUNVERSION = 'http://133.96.7.120/livever'
LOCALVERSION = '/opt/data/apache2/deploy/lastver'
LOCALTMP = '/opt/data/apache2/deploy/tmp'

def getVersion():
    url = urllib.urlopen(LASTVERSION)
    version = url.readline().split('\n')[0]
    return version

def getRunVersion():
    url = urllib.urlopen(RUNVERSION)
    rs = url.readlines()[0].split('\n')[0]
    return rs    

def parserVersion():
    """
     stat = 1    # The file already exit.
     stat = 0    # The file not exit.
    """
    package = 'tran-%s.tgz' % getVersion()
    down = 'http://133.96.7.120/%s/%s' % (getVersion(), package)
    cmd = 'wget -P %s %s' % (LOCALTMP, down)
    stat = 1
    if package not in os.listdir(LOCALTMP):
        stat = 0
        try:
            with open(os.devnull,'w') as fd:
                check_call([cmd], shell=True, stdout=fd, stderr=fd)
        except Exception as e:
            print e
            exit(1)
        return stat
    return stat

def parserLastVersion():
    while True:
        rs = getRunVersion()
        ls = getVersion()
        d = datetime.datetime.now()
        now = d.strftime('%Y-%m-%d %H:%M:%S')
        if rs != ls:
            status = parserVersion()
            package = 'tran-%s.tgz' % getVersion()
            cmd = 'tar -zxvf %s -C %s' % (os.path.join(LOCALTMP,package),LOCALVERSION)
            command = "md5sum %s |awk -F' ' '{print $1}' > %s " % (os.path.join(LOCALTMP,package),os.path.join(LOCALVERSION,getVersion(),'md5file'))
            comm = 'rm -rf %s' % (os.path.join(LOCALTMP,package))
            if status == 1 or status == 0:
                with open(os.devnull,'w') as fd:
                    check_call(cmd, shell=True, stdout=fd, stderr=fd)
                    check_call([command], shell=True, stdout=fd, stderr=fd)
                    check_call([comm], shell=True, stdout=fd, stderr=fd)
            else:
                print "[%s] no download code." % (now)
        time.sleep(100)

def main():
    cmd = sys.argv[1]
    pidfile = '/var/run/getcode.pid'
    with open(pidfile, 'r') as fd:
        pid = fd.readlines()
    if cmd == 'start':
        if not pid:
            daemonize(stdout='/var/log/getcode.log', stderr='/var/log/getcode_error.log')
            ppid = str(os.getpid())
            with open(pidfile, 'w') as fd:
                fd.write(ppid)
            parserLastVersion()
        else:
            print "getcode subprocess already Running..."
            sys.exit(1)
    elif cmd == 'stop':
        comm = ': > %s' % pidfile
        if pid:
            p = int(pid[0])
            os.kill(p, signal.SIGTERM)
            check_call(comm, shell=True, stdout=PIPE, stderr=PIPE)
            print "getcode stopd."
    else:
        print "argv[1] command: start stop"
        sys.exit(1)
        
if __name__ == "__main__":
    main()
