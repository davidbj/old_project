#-*- coding:utf-8 -*-

import re

UPLOAD_DIR = '/david/webdns'

def parserIp(ip):
    '''ip地址处理函数'''
    
    ld=[]
    p = re.compile(r'\r\n')
    ips = re.findall(p, ip)
    if ips:
        data = ip.strip().split('\r\n')
        for i in data:
            ld.append(i)
    else:
        ld.append(ip)
    
    return ld
