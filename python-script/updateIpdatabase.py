#!/usr/bin/env python
#-*- coding:utf-8 -*-
from subprocess import PIPE, Popen
from Queue import Queue
import time, urllib2, threading
import json

def parserLog():
    cmd = "sed '/ANY/p' dns_logs.0 | awk -F' ' '{print $6}'"
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    data = stdout.strip()
    data = data.split('\n')
    return data

def getIp():
    ld = []
    data = parserLog()
    for i in data:
        if i.split('#')[0] not in ld:
	    ld.append(i.split('#')[0])
    return ld

class ThreadClass(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
	ld=[]
	dc={}
	dt={}
        while True:
            host = self.queue.get()
	    try:
                data = urllib2.urlopen('http://ip.taobao.com/service/getIpInfo.php?ip=%s' % host).read() 	
		with open('dns.txt', 'a') as fd:
		    fd.write(data+'\n')                                                                             
  		                                                                                       
		time.sleep(1)
                self.queue.task_done()                                                                  	
	    except:
	        pass
	
def main():
    queue = Queue()
    for i in range(15):
        t = ThreadClass(queue)
        t.setDaemon(True)
        t.start()

    hosts = getIp()
    for host in hosts:
        queue.put(host)

    queue.join()


if __name__ == "__main__":
    st = time.time()
    main()
    print '%f'%(time.time()-st) 
