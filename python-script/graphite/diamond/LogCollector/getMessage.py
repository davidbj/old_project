#!/usr/bin/python
#-*-coding:utf-8 -*-

import sys
import re
import os
import datetime

LOGFILE = '/var/log/httpd/graphite-web-access.log'

def getNowTime():
    d = datetime.datetime.now()
    now = d - datetime.timedelta(seconds=46800)
    return now

def getLastTime():
    d = datetime.timedelta(seconds=60)
    lastTime = getNowTime() - d  
    return lastTime 
 
def filerev(somefile, buffer=256):
  somefile.seek(0, os.SEEK_END)
  size = somefile.tell()
  lines = ['']
  rem = size % buffer
  pos = max(0, (size // buffer - 1) * buffer)
  while pos >= 0:
    somefile.seek(pos, os.SEEK_SET)
    data = somefile.read(rem + buffer) + lines[0]
    rem = 0
    pos -= buffer
    lines = re.findall(r'[^\n]*\n?', data)
    ix = len(lines) - 2
    while ix > 0:
      yield lines[ix]
      ix -= 1
  else:
    yield lines[0]

def getMessage():
    ret = {}
    p = re.compile(r'[\d :/]{19}')
    with open(LOGFILE, 'r') as f:
      for line in filerev(f):
          line = line.split('\n')[0]
          s = line.split()[-2]
          info = re.search(p,line)
          year = info.group(0).split('/')[2].split()[0]
          month = info.group(0).split('/')[1]
          day = info.group(0).split('/')[0]
          hour = info.group(0).split()[1].split(':')[0]
          minute = info.group(0).split()[1].split(':')[1]
          second = info.group(0).split()[1].split(':')[2]
          dt = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
          if dt - getLastTime() >= datetime.timedelta(seconds=0):
              if s in ret:
                  ret[s]+=1
              else:
                  ret[s]=1
    return ret
    
if __name__ == "__main__":
   print getMessage()
