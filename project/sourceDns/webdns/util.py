#-*- coding:utf-8 -*-

import dns.tsigkeyring
import dns.update
import dns.query
import dns.message
import re
import logging


#dnspython 更新记录DNS Server
#keyring 是DNS Server 秘钥
#SERVER_IP Dns server ip 地址
keyring = dns.tsigkeyring.from_text({'davidddns':'6InIotdDmbMkn5bwTg8pQA=='})
UPLOAD_DIR = '/david/sourceDns/upload'
SERVER_IP = '127.0.0.1'

#记录日志
logger = logging.getLogger('sourceDns.webdns.util')

def changeDns(host, domain, ip, ttl, ty):
    '''批量添加记录'''

    ip = parserIp(ip)
    try:
        for i in ip:
            #querymessage = dns.message.make_query(domain, dns.rdatatype.A)
            #r = dns.query.udp(querymessage, SERVER_IP)
            #a = r.answer
            #ndomain = domain.split('.')[-2]+'.'+domain.split('.')[-1]
            #fdomain = '.'.join(domain.split('.')[:-2])
            up = dns.update.Update(domain, keyring=keyring)
            #fdomain = fdomain.encode()
            host = host.encode()
            i = i.strip().encode()
            #if a:
            #    up.replace(fdomain, ttl, type, i)
            #else:
            up.add(host, ttl, ty, i)
            dns.query.tcp(up, SERVER_IP)
        data = True
    except Exception, e:
        logger.error(e)    
        data = False
    return data

def parserIp(ip):
    '''ip 地址处理函数'''

    p = re.compile(r'\n')
    p1 = re.compile(r',')
    p2 = re.compile(r'\r\n')
    q = re.findall(p, ip)
    a = re.findall(p1, ip)
    a2 = re.findall(p2, ip)
    ld = []
    if a2:
        d = ip.strip().split('\r\n')
        for i in d:
            ld.append(i)
    elif q:
        d = ip.strip().split('\n')
        for i in d:
            ld.append(i)
    elif a:
        d = ip.strip().split(',')
        for i in d:
            ld.append(i)
    #elif a2:
    #    print 'aaa'
    #    d = ip.strip().split('\\r\n')
    #    for i in d:
    #        ld.append(i)
    else:
        ld.append(ip)
    
    return ld

def addDns(host, domain, ip, ttl, Type):
    '''添加DNS 记录'''

    try:
        up = dns.update.Update(domain, keyring=keyring)
        host = host.encode()
        ttl = ttl.encode()
        Type = Type.encode()
        if isinstance(ip, list):
            for i in ip:
                i = i.encode()
                up.add(host, ttl, Type, i)
                dns.query.tcp(up, SERVER_IP)
        else:
            up.add(host, ttl, Type, ip)
            dns.query.tcp(up, SERVER_IP)
        data = True 
    except Exception, e:
        logger.error(e)
        data = False
    return data

def updateDns(host, domain, ip, ttl, Type):
    '''更新Dns 记录'''

    try:
        up = dns.update.Update(domain, keyring=keyring)
        host = host.encode()
        ttl = ttl.encode()
        Type = Type.encode()
        if isinstance(ip, list):
            up.delete(host)
            for i in ip:
                i = i.encode()
                up.add(host, ttl, Type, i)
                dns.query.tcp(up, SERVER_IP)
        else:
            ip = ip.encode()
            up.replace(host, ttl, Type, ip)
            dns.query.tcp(up, SERVER_IP)
        data = True
    except Exception, e:
        logger.error(e)
        data = False
    return data

def remove(domain, host):
    '''删除Dns 记录'''

    try:
        up = dns.update.Update(domain, keyring=keyring)
        host = host.encode()
        up.delete(host)
        dns.query.tcp(up, SERVER_IP)
        code=True
        return code
    except Exception, e:
        logger.error(e)
        code=False
        return code
