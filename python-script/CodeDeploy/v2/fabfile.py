#!/usr/local/bin/python2.7
#-*- coding:utf-8 -*-

from fabric.api import *

env.user = 'root'
env.port = '65535' 
env.password = '123456'
#env.hosts = ['133.96.7.103','133.96.7.102','133.96.7.100','133.96.7.104','133.96.7.105']
env.hosts = ['133.96.7.103']

def deploy():
    run("""LAST_VER=`curl http://133.96.7.120/Tran_lastver`;
        LAST_WP=/opt/data/apache2/deploy/releases/Tran-${LAST_VER}
        test -d ${LAST_WP}
    """)
