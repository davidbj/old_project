#!/usr/local/bin/python2.7
#coding:utf-8

import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'sourceDns.settings')

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
