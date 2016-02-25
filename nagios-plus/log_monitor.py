#!/usr/local/src/python2.7/bin/python
#!-*- coding:utf-8 -*-

from optparse import OptionParser
from subprocess import PIPE,Popen 
import datetime
import operator
import sys

OK = 0
WARING = 1
CRITICAL = 2
UNKNOWN = 3
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

def opt():
    parser = OptionParser(usage="usage: %prog -w WARNING -c CRITICAL -s SECONDS")
    parser.add_option('-c',default=3,action="store",type="int",dest="critical")
    parser.add_option('-w',default=5,action="store",type="int",dest="warning")
    parser.add_option('-s',default=300,action='store',type='int',dest='seconds')
    return parser.parse_args()

def getLogInfo():
    options, args=opt()
    w_lines = options.warning*options.seconds
    c_lines = options.critical*options.seconds
    log = Popen('tail -n %s /var/log/messages' % str(c_lines),shell=True,stdout=PIPE)
    stdout, stderr = log.communicate()
    return stdout.strip()

def conver2datetime(s):
    import sys
    now = datetime.datetime.now()
    month, day, time = s
    hour, minute, second = time.split(':')
    t = datetime.datetime(now.year, MONTH[month], int(day), int(hour), int(minute), int(second))  
    return t

def parserLog(data):
    ret={}
    options, args=opt()
    now = datetime.datetime.now()
    five_minutes_ago = now - datetime.timedelta(seconds=int(options.seconds))
    #print five_minutes_ago
    for lines in data.split('\n'):
        log_time = conver2datetime(lines.split()[:3])
        if five_minutes_ago < log_time:
            if log_time in ret:
                ret[log_time]+=1
            else:
                ret[log_time]=1
    return ret    

def main():
    options, args=opt()
    data = getLogInfo()
    sorted_date = sorted(parserLog(data).iteritems(),key=operator.itemgetter(1),reverse=True)
    print sorted_date
    for t,n in sorted_date:
        if options.critical > n >= options.warning:
            print 'WARNING,At %s Total %s log' % (t,n)
            sys.exit(WARNING)
        elif n > options.critical:
            print 'CRITICAL,At %s Total %s log' %(t,n)
            sys.exit(CRITICAL)
        elif n < options.warning:
            print 'OK,At %s Total %s log' %(t,n)
            sys.exit(OK)
        else:
            print 'UNKNOWN'
            sys.exit(UNKNOWN) 
    
if __name__ == "__main__":
    main()
