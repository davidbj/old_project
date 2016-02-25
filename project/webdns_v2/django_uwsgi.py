#!/usr/bin/env python

import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webdns.settings")

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
