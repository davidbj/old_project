#!/usr/bin/python
#-*- coding:utf-8 -*-

import re
from subprocess import Popen,PIPE
import datetime
import time
import socket
from os import path
import sys

DIRNAME = path.dirname(__file__)
OPSTOOLS_DIR = path.abspath(DIRNAME)
sys.path.append(OPSTOOLS_DIR)
from daemonize import daemonize

LOGFILE = '/var/log/httpd/graphite-web-access.log'
rule = re.compile(r'[0-9/]{1,3}[A-Za-z/]{4}[\d:]{13}')
SECOND = 6
MESSAGE = 1   
MONTH = {
    'Jan':1,
    'Feb':2,
    'Mar':3,
    'Apr':4,
    'May':5,
    'Jun':6,
    'Jul':7,
    'Aug':8,
    'Sep':9,
    'Oct':10,
    'Nov':11,
    'Dec':12
}

def getTime(data):
    d = rule.search(data)
    dt = d.group(0)
    for k, v in MONTH.items():
        if dt.split('/')[1] == k:
            month = v
    day = dt.split('/')[0]
    year = dt.split('/')[2].split(':')[0]
    hour = dt.split('/')[2].split(':')[1]
    minute = dt.split('/')[2].split(':')[2]
    second = dt.split('/')[2].split(':')[3]
    t = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    return t 

def getHttpStatus(data):
    stat = data.split()[-2]
    return stat

def getLastTime():
    cmd = 'tail -n 1 %s' % LOGFILE
    f = Popen(cmd, shell=True, stdout=PIPE)
    stdout, stderr = f.communicate()
    return getTime(stdout)    

def getMessageNum(num):
    cmd = 'tail -n %d %s' % (num,LOGFILE)
    f = Popen(cmd, shell=True, stdout=PIPE)
    stdout, stderr = f.communicate()
    return stdout.strip()

def checkMessage():
    ret = {}
    tm = getLastTime()
    s = True
    info = int(MESSAGE)*int(SECOND)
    while s:
        lt = getMessageNum(info).split('\n')
        for i  in lt:
            if datetime.timedelta(seconds=0) <  tm - getTime(i) < datetime.timedelta(seconds=60):
                info+=50
                s = True
                break
            else:
                x = getMessageNum(info)
                s = False
                break
    
    for i in x.strip().split('\n'):
        if datetime.timedelta(seconds=0) < tm - getTime(i) <= datetime.timedelta(seconds=60):
            ln = i.split()
            if ln[-2] in ret:
                ret[ln[-2]]+=1
            elif i[-2] not in ret:
                ret[ln[-2]]=1
    return ret

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1',2003))
    while True:
        h = getLastTime()
        for k, v in checkMessage().items():
            s = 'http.http_%s %d %s\n' % (k,v,h.strftime('%s'))
            sock.send(s)
        time.sleep(60) 

if __name__  == "__main__":     
    daemonize(stdout='/var/log/httpd/monitor.log', stderr='/var/log/httpd/monitor_error.log')
    main()
