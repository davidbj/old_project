#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
    Author:David.Zhang
    Date:2014/02/07
    Function:check host port status.
"""

import socket
from optparse import OptionParser
import sys

def checkPort(address, port):
    s = socket.socket()
    try:
        s.connect((address, port))
        print "connected to %s on port %s true." % (address, port)
        return True
    except socket.error, e:
        print "connection to %s on port %s failed." % (address, port)
        return False

def opt():
    parser = OptionParser()
    parser.add_option("-a", "--address", dest='address', default='localhost', help='Connecting to Host address')
    parser.add_option("-p", "--port", dest='port', type="int", default=22, help="Connecting to Host port")
    options, args = parser.parse_args()
    return options, args

def main():
    options, args = opt()
    checkPort(options.address, options.port)

if __name__ == "__main__":
    main()