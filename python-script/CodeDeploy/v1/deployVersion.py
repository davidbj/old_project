#!/usr/bin/python
#-*- coding:utf-8 -*-

import urllib
from subprocess import check_call, PIPE
import os
import datetime
import time
import sys
from os import path
import signal

DIRNAME = path.dirname(__file__)
OPSTOOLS_DIR = path.abspath(DIRNAME)
sys.path.append(OPSTOOLS_DIR)
from daemonize import daemonize

LIVEURL = 'http://133.96.7.120/livever'
RUNDIR = '/opt/data/apache2/deploy/livever'

def getLiveVersion():
    lv = urllib.urlopen(LIVEURL)
    version = lv.readlines()[0].split('\n')[0]
    return version

def runLiveVersion():
    with open(RUNDIR,'r') as fd:
        rv = fd.readlines()[0].split('\n')[0]
    return rv

def parserLiveVersion():
    while True:
        d = datetime.datetime.now()
        now = d.strftime('%Y-%m-%d %H:%M:%S')
        lt = getLiveVersion()
        rt = runLiveVersion()
        lastver  = '/opt/data/apache2/deploy/lastver/%s/tran-%s' % (lt,lt)
        runver = '/opt/data/apache2/htdocs/Tran'
        cmd = 'echo %s > %s' % (lt,RUNDIR)
        command = 'rm -rf %s' % (runver)
        comm = 'ln -sf %s %s' % (lastver,runver)
        if lt != rt:
            with open(os.devnull,'w') as fd:
                check_call(cmd, shell=True, stdout=fd, stderr=fd)
                check_call(command, shell=True, stdout=fd, stderr=fd)
                check_call(comm, shell=True, stdout=fd, stderr=fd)
                check_call('/opt/data/tomcat/bin/shutdown.sh', shell=True, stdout=fd, stderr=fd)
                time.sleep(10)
                check_call('/opt/data/tomcat/bin/startup.sh', shell=True, stdout=fd, stderr=fd)
                check_call('/opt/data/apache2/bin/apachectl restart', shell=True, stdout=fd, stderr=fd)
        time.sleep(150)

def main():
    cmd = sys.argv[1]
    pidfile = '/var/run/deploy.pid'
    with open(pidfile, 'r') as fd:
        pid = fd.readlines()
    if cmd == 'start':
        if not pid:
            daemonize(stdout='/var/log/getcode.log', stderr='/var/log/getcode_error.log')
            ppid = str(os.getpid())
            with open(pidfile, 'w') as fd:
                fd.write(ppid)
            parserLiveVersion()
        else:
            print "deploy subprocess already Running..."
            sys.exit(1)
    elif cmd == 'stop':
        comm = ': > %s' % pidfile
        if pid:
            p = int(pid[0])
            os.kill(p, signal.SIGTERM)
            check_call(comm, shell=True, stdout=PIPE, stderr=PIPE)
            print "deploy stopd."
    else:
        print "argv[1] command: start stop"
        sys.exit(1)
    
if __name__  == "__main__":
    main()