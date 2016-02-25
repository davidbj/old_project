#!/usr/bin/env python
# -*- coding:utf-8 -*-

import subprocess
import socket
import re
import hashlib

class hostInfo(object):
    def getDMI(self):
        """get dmidemode information."""

        cmd = 'dmidecode'
        try:
            info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            stdout, stderr = info.communicate()
            data = stdout.strip()
        except ExecError as e:
            print e
        return data
   
    def getIp(self):
        """get ipaddress information."""

        cmd = 'ifconfig'
        try:
            info = subprocess.Popen(cmd, shell=True, stdout= subprocess.PIPE)
            stdout, stderr = info.communicate()
            data = stdout.strip()
        except ExecError as e:
            print e
        return data

    def getMemory(self):
        """get host memory size."""
        
        cmd = 'cat /proc/meminfo'
        try:
            info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            stdout, stderr = info.communicate()
        except ExecError as e:
            print e
        return stdout.strip()

    def getCpuInfo(self):
        cmd = 'cat /proc/cpuinfo'
        try:
            info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            stdout, stderr = info.communicate()
        except ExecError as e:
            print e
        return stdout.strip()

    def parserDMI(self):
         """return host product infomation."""

         dmidata = self.getDMI()
         line_in = False
         pd = {}
         fd = {}
         for line in dmidata.split('\n'):
             if line.startswith('System Information'):
                 line_in = True
                 continue 
             if line_in and line.startswith('\t'):
                 k, v = [i.strip() for i in line.split(':')]
                 pd[k] = v
             else:
                 line_in = False
         name = "verdor:%s ; sn:%s ; uuid:%s" % (pd['Product Name'], pd['Serial Number'], pd['UUID'])
         for i in name.split(';'):
             k, v = [j.strip() for j in i.split(':')]
             fd[k] = v
         return fd
     
    def parserHostName(self):
        """return hostname."""
        fd = {}
        hostname = socket.gethostname()        
        fd['hostname'] = hostname
        return fd
    
    def parserIpaddr(self):
        """return ipaddress."""
        
        ip_data = self.getIp()
        fd = {}
        inet = re.compile(r'inet addr:([\d\.]{7,15})')
        data = inet.findall(ip_data)
        if '127.0.0.1' in data:
            data.pop()
        fd['ip'] = data
        return fd

    def parserMemory(self):
        """return memory Total"""
        
        mem_data = self.getMemory()
        fd = {}
        for line in mem_data.split('\n'):
            if line.startswith('MemTotal:'):
                k, v = [i for i in line.split(':')]
        fd[k] = v.strip() 
        return fd        

    def parserCpu(self):
        """return cpu cores and cpu vendor"""
        cpu_data = self.getCpuInfo()
        ld = []
        pd = {}
        dt = [] 
        for line in cpu_data.split('\n'):
            if line.startswith('processor'):
                ld.append(line)
                continue
            if line.startswith('model name'):
                dt.append(line)
        name = "cores:%s ; model:%s" % (ld[-1].split(':')[-1], dt[-1].split(':')[-1])
        for i in name.split(';'):
            k, v = [i for i in i.split(':')]
            pd[k.strip()] = v.strip()
        if pd['cores'] == '0':
            pd['cores'] = int(1)
        return pd

    def getIdentity(self):
        """get ssh-keygen"""
        cmd = "ssh-keygen -lf /etc/ssh/ssh_host_rsa_key | awk '{print $2}' | sed -e 's/://g'"
        try:
            info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            stdout, stderr = info.communicate()
        except ExecError as e:
            print e
      
        return stdout.strip()
    
    def parserIdentity(self):
        pd = {}
        ssh_data = self.getIdentity()
        md5 = hashlib.md5()
        md5.update(ssh_data)
        identity = md5.hexdigest()
        pd['identity'] = identity
        return pd
    
    def getOsname(self):
        cmd = 'lsb_release -i -r -s'
        pd = {}
        try:
            info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            stdout, stderr = info.communicate()
        except ExecError as e:
            print e
        pd['os'] = stdout.strip()
        return pd


