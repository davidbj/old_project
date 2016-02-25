#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re

ip_specs = r'\.'.join([r'\d{1,3}']*4)
re_ip = re.compile(ip_specs)
ipHitListing = {}

def apacheListen(logFile):
    contens = open(logFile, 'r')
    for line in contens:
        match = re_ip.match(line)
        if match:
            ip = match.group()
            #ipHitListing[ip] = ipHitListing.get(ip, 0) + 1
            try:
                quad = map(int, ip.split('.'))
            except ValueError:
                pass
            else:
                if len(quad) == 4 and min(quad) >=0 and max(quad)<=255:
                    ipHitListing[ip] = ipHitListing.get(ip, 0) + 1
    return ipHitListing

if __name__ == "__main__":
    import sys
    print apacheListen(sys.argv[1])
