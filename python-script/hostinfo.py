#!/usr/bin/python
#-*- coding:utf-8 -*-

import socket
import platform
import netifaces
import psutil
from subprocess import Popen, PIPE
import urllib
import urllib2

#get 'dmidecode' infomation
def getDMI(cmd):
    #cmd = 'dmidecode'
    p = Popen(cmd, shell=True, stdout=PIPE)
    stdout, stderr = p.communicate()
    return stdout.strip()

#get Host infomation
def getHostName():
    fd = {}
    Host = socket.gethostname()
    OsRelease = platform.dist()[0]+platform.dist()[1]
    fd['HostName'] = Host
    fd['OsRelease'] = OsRelease
    return fd     

#get Host NIC information
def getIpaddr():
    fd = {}
    pd = ''
    nic = netifaces.interfaces()
    for i in nic:
         pd += netifaces.ifaddresses(i)[2][0]['addr']+','
    pd = pd[:-1]
    fd['Ipaddr'] = pd
    return fd

#get product infomation
def getHostProduct(dmidata):
    pd = {}
    fd = {}
    line_in = False
    for line in dmidata.split('\n'):
        if line.startswith('System Information'):
            line_in = True
            continue
        if line.startswith('\t') and line_in:
            k, v = [i.strip() for i in line.split(':')] 
            pd[k] = v
        else:
            line_in = False
    name = "Vendor:%s ; Sn:%s ; Product:%s" % (pd['Manufacturer'], pd['Serial Number'], pd['Product Name'])
    for i in name.split(';'):
        k, v = [j.strip() for j in i.split(':')]
        fd[k] = v
    return fd

#get Host Memory info
def getMemory():
    fd = {}
    mem = str(int(psutil.virtual_memory().total)/(1024**2))+' MB'
    fd['MemSize'] = mem
    return fd

#get Host Cpu info
def getCpu():
    fd = []
    vd = set()
    pd = set()
    sd = {}
    cmd = 'cat /proc/cpuinfo'
    p = Popen(cmd, shell=True, stdout=PIPE)
    stdout, stderr = p.communicate()    
    cpuInfo = stdout.strip()
    for i in cpuInfo.split('\n'):
        if i.startswith('processor'):
           fd.append(int(i.split(':')[1].strip()))
    Core = max(fd)+1    #get Cpu Cores
    for i in cpuInfo.split('\n'):
        if i.startswith('vendor_id'):
            vd.add(i.split(':')[1].strip())
    Product = vd.pop()
    for i in cpuInfo.split('\n'):
        if i.startswith('model name'):
            pd.add(i.split(':')[1].strip())
    Model = pd.pop()
    sd['CpuCores'] = Core
    sd['CpuModel'] = Model
    sd['CpuVendor'] = Product
    return sd 
        
def main():
    ld = []
    fd = {}
    cmd = 'dmidecode'
    dmidata = getDMI(cmd)
    product = getHostProduct(dmidata)
    hostname = getHostName()
    ipaddr = getIpaddr()
    memory = getMemory()
    cpu = getCpu()
    for k in product.iteritems():
        ld.append(k)
    for k in hostname.iteritems():
        ld.append(k)
    for k in ipaddr.iteritems():
        ld.append(k)
    for k in memory.iteritems():
        ld.append(k)
    for k in cpu.iteritems():
        ld.append(k)
    
    for i in ld:
        fd[i[0]] = i[1]
    
    data = urllib.urlencode(fd)
    req = urllib2.Request('http://django_ip:port/api/collect',data)
    response = urllib2.urlopen(req)
    return response.read()
    
if __name__ == "__main__":
    main() 
