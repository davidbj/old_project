#!/usr/bin/env python
#-*- coding:utf-8 -*-

def apacheCachePercentage(logfile):
    contents = open(logfile, 'r')
    totalRequest = 0
    cachedRequests = 0
    for line in contents:
        totalRequest +=1
        if line.split(' ')[8] == '304':
            cachedRequests += 1
    return int(0.5+float(100*cachedRequests)/totalRequest)
    #return (float(cachedRequests)/totalRequest)*100

if __name__ == "__main__":
    import sys
    print apacheCachePercentage(sys.argv[1])
