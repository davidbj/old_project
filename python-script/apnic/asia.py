#!/usr/local/bin/python2.7
#-*- coding:utf-8 -*-
from subprocess import PIPE, Popen
import urllib2
import re
import json
import MySQLdb as mdb 


def getApnic():
    ld=[]
    dt=[]
    response = urllib2.urlopen('http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest')
    html = response.read()
    for i in html.strip().split('\n'):
	ld.append(i)
    for ln in ld:
	data = ln.split('|')
        if data[0] == 'apnic' and data[1] == 'CN' and data[2] == 'ipv4':
	    dt.append(ln)
    return dt

def subnet(data):
    for i in range(0, 33):
	s = 2**i
	if s == int(data):
	    subnet = int(32) - int(i)
	    return subnet

def parserIp():
    dc={}
    ld=[]
    data = getApnic()
    for ln in data:
        i=ln.split('|')
        dc['city'] = i[1]
        dc['ip'] = i[3]
        dc['subnet'] = subnet(i[4])
        ld.append(dc)
        dc={}
    return ld

def getTaoBaoIp():
    dc = {}
    ld=[]
    data = parserIp()
    for i in data:
	info = urllib2.urlopen('http://ip.taobao.com/service/getIpInfo.php?ip=%s' % i['ip']).read()
	dt = json.loads(info)
        i['city'] = dt['data']['city']
        i['city_id'] = dt['data']['city_id']
        i['isp'] = dt['data']['isp']
        i['isp_id'] = dt['data']['isp_id']
        i['region'] = dt['data']['region']
        i['region_id'] = dt['data']['region_id']
        ld.append(i)
    return ld

def connMysql():
    host = '127.0.0.1'
    user = 'root'
    port = 3306
    db = 'ip_database'
    
    conn = mdb.connect(host=host,
		       port=port,
		       user=user,
		       db=db,
		       charset='utf8',
		       use_unicode=True)
    cur = conn.cursor()
    return cur


def insert(cur, ld):
    sql = "insert into apnic_ip_database(subnet, city, city_id, ip, region, region_id, isp_id, isp) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % ld
    cur.execute(sql)

def main():
    ld = []
    data = getTaoBaoIp()
    for i in data:
        ld = [i['subnet'], i['city'], i['city_id'], i['ip'], i['region'], i['region_id'], i['isp_id'], i['isp']]
        ld = tuple(ld)
        insert(connMysql(), ld)
 	ld = []

if __name__ == "__main__":
    print main()
