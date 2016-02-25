#!/usr/local/python/bin/python
#-*- coding:utf-8 -*-

import dns.tsigkeyring, dns.update, dns.query 
from optparse import OptionParser
import os

KEYPATH = '/var/named/keys'
SERVER_IP = '132.96.77.188'

def opt():
    parser = OptionParser(usage="usage: %prog [options] [comm1 comm2]")
    parser.add_option('-a','--Action',
            dest="Action",
            action="store",
            default="add",
            help="Action.")
    parser.add_option("-z","--zone",
            dest="zone",
            action="store",
            default="david.com",
            help="domain zone name.")
    parser.add_option("-n","--name",
            dest="name",
            action="store",
            default="www",
            help="Host name.")
    parser.add_option("-t","--ttl",
            dest="ttl",
            action="store",
            default="21600",
            help="TTL times.")
    parser.add_option("-T","--type",
            dest="type",
            action="store",
            default="A",
            help="Record exmple:A MX TXT NS")
    parser.add_option("-i","--ipaddr",
            dest="ipaddr",
            action="store",
            default="127.0.0.1",
            help="Client IP addr.")
    return parser.parse_args() 
    
def mkdirZone():
    opts, args = opt()
    ttl = int(opts.ttl)
    zone = opts.zone
    dataString = """$TTL %d 
    @               IN SOA  %s. root.%s. (
                                    61         ; serial
                                    10800      ; refresh (3 hours)
                                    900        ; retry (15 minutes)
                                    604800     ; expire (1 week)
                                    86400      ; minimum (1 day)
                                    )
                            NS      %s.
    dns                     A       192.168.1.88
    """ % (ttl, zone, zone, zone)
    return dataString

def writeZone():
    opts, args = opt()
    zone = opts.zone
    zoneString = """
    zone "%s" IN {
            type master;
            file "%s.zone";
            allow-update {key mydns;};
    }; 
    """ % (zone, zone)
    return zoneString
   
def getKey():
    with open(KEYPATH,'r') as fd:
        k = fd.readline()
    k = k.split('\n')[0]
    return k

def up():
    dataString = mkdirZone()
    zoneString = writeZone()
    opts, args = opt()
    zone = opts.zone
    name = opts.name
    ttl = int(opts.ttl)
    action = opts.Action
    type = opts.type
    ip = opts.ipaddr
    k = getKey()
    zone_dir = os.path.join('/var/named','%s.zone') %zone
    named_dir = '/etc/named.rfc1912.zones'
    if not os.path.exists(zone_dir):
        with open(zone_dir,'w') as fd:
            fd.write(dataString)
        with open(named_dir,'a') as fd:
            fd.write(zoneString)
        os.system("sed -i 's/^    //g' %s" % zone_dir)
        os.system("sed -i 's/^    //g' %s" % named_dir)
        os.system("/etc/init.d/named restart > /dev/null 2>&1") 
    k = {'mydns':k}
    keyRing = dns.tsigkeyring.from_text(k)
    up = dns.update.Update(zone,keyring=keyRing)
    if action == 'add':
        up.add(name, ttl, type, ip)
        dns.query.tcp(up, SERVER_IP)
    elif action == 'delete':
        up.delete(name)
        dns.query.tcp(up, SERVER_IP)

if __name__ == "__main__":
    up()
