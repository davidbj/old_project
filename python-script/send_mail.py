#!/usr/bin/env python
#-*- coding:utf-8 -*-

import threading
import smtplib
from email.mime.text import MIMEText
import time

def send_mail(to_list, sub, content):
    mail_host = "smtp.126.com"
    mail_user = "david_bj"
    mail_pass = "xxxxxxxx"
    mail_postfix="126.com"
    me=sub+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content, _subtype="plain", _charset="utf-8")
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ';'.join(to_list)
    try:
        server=smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False


class mythread(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name=threadname)

    def run(self):
        lock.acquire()
        mailto_list=['zhsz_bj@126.com']
        if send_mail(mailto_list, '线程一发送邮件', '张'):
            print "线程一发送成功"
        else:
            print "线程一发送失败"
        time.sleep(2)
        lock.release()
        

class ythread(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name=threadname)

    def run(self):
        lock.acquire()
        mailto_list=['zhsz_bj@126.com']
        if send_mail(mailto_list, '线程二发送邮件', '李'):
            print "线程二发送成功"
        else:
            print "线程二发送失败"
        time.sleep(2)
        lock.release()

lock = threading.RLock()
t1=[]
for i in range(2):
    if i == 0:
        t=mythread(str(i))
        t1.append(t)
    else:
        t2=ythread(str(i))
        t1.append(t2)


for i in t1:
    i.start()
