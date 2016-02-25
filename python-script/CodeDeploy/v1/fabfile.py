#!/usr/bin/python
#-*- coding:utf-8 -*-

from fabric.api import *
import os

env.username = 'root'
env.password = '123456'
env.hosts = ['132.96.77.188',]

version = '/var/www/html/deploy/package/lastver'
livever = '/var/www/html/deploy/package/livever'
with open(version,'r') as fd:
    ver = fd.readlines()[0].split('\n')[0]
webroot = '/var/www/html/deploy/lastver/%s' % (ver)
localroot = '/var/www/html/deploy/package/%s/md5file' % (ver)

def deploy():
    with cd(webroot):
        lastver = run('cat md5file')
    
    with open(localroot,'r') as fd:
        dver = fd.readlines()[0].split('\n')[0]

    if dver == lastver:
        local('echo %s > %s' % (ver,livever))
        print 'sucess'
    else:
        raise Exception('The md5 value is not same.') 
