#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re
from  subprocess import PIPE, Popen
LOG_DIR="/opt/data/web/nginx/logs/access_20131128.log"

def getLog():
    fd = open(LOG_DIR,'r')
    line = fd.readline()
    html = line
    while line:
        line = fd.readline()
        html +=line
    fd.close()
    return html.strip()

def parserLog(data):
    ret = {}
    fd = set()
    _pv = re.compile(r'(\"GET / HTTP/1.1\")')
    _nologin_select = re.compile(r'(\"GET \/listwithoutlogin.jsp\?action=listwithoutlogin HTTP/1.1\")')
    _zjwf_select = re.compile(r'(\"GET \/listbyjszh\.jsp HTTP/1.1\")')
    _login_select = re.compile(r'(GET \/tranplat\/detail\.jsp)')
    _gzym = re.compile(r'(GET \/pages\/selfProcese1\/bInform1\.jsp)')
    _login_select_pic = re.compile(r'(GET \/peccancy\.do\?action=viewphoto)')
    _user_login = re.compile(r'(GET \/user\.do\?jsonpcallback=\?\&action=login)') 
 
    for line in data.split('\n'):
        _ppv = re.search(_pv, line)
        _pnologin_select = re.search(_nologin_select, line)
        _pzjwf_select = re.search(_zjwf_select, line)
        _plogin_select = re.search(_login_select, line)
        _pgzym = re.search(_gzym, line)
        _plogin_select_pic = re.search(_login_select_pic, line)
        _puser_login = re.search(_user_login, line)
        
        if _ppv:
            if 'pv' not in ret:
                ret['pv'] = 1
            else:
                ret['pv'] +=1
      
        if _pnologin_select:
            if 'nologin_select' not in ret:
                ret['nologin_select'] = 1
            else:
                ret['nologin_select'] +=1

        if  _pzjwf_select:
            if 'zjwf_select' not in ret:
                ret['zjwf_select'] = 1
            else:
                ret['zjwf_select'] += 1

        if _plogin_select:
            if 'login_select' not in ret:
                ret['login_select'] = 1
            else:
                ret['login_select'] +=1

        if _pgzym:
            if 'gzym' not in ret:
                ret['gzym'] = 1
            else:
                ret['gzym'] += 1

        if _plogin_select_pic:
            if 'login_select_pic' not in ret:
                ret['login_select_pic'] = 1
            else:
                ret['login_select_pic'] += 1

        if _puser_login:
            if 'user_login' not in ret:
                ret['user_login'] = 1
            else:
                ret['user_login'] += 1
  
        fd.add(line.split()[0])
    
    ret['ip'] = len(fd)
    return ret
 
if __name__ == "__main__":
    logs = getLog()
    print parserLog(logs)
