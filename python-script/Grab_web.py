#!/usr/bin/python
#-*- conding:utf-8 -*-

import MySQLdb
import urllib2
import sys
import chardet
import re
import time

LASTNUM=[]

def connMysql(title, zddate, xn, xv, city, content):
    host = '127.0.0.1'
    db = 'xxx'
    user = 'xxxx'
    pwd = 'xxxxx'
    conn = MySQLdb.connect(host=host, db=db, user=user, passwd=pwd, charset="utf8")
    curs = conn.cursor()
    curs.execute("SET NAMES utf8")
    curs.execute("SET CHARACTER_SET_CLIENT=utf8")
    curs.execute("SET CHARACTER_SET_RESULTS=utf8")
    conn.commit()
    sql = "INSERT INTO bz(title_name, zd_name, x_name, gs_name, s_name, lk_name) values('%s','%s','%s','%s','%s','%s')" % (title, zddate, xn, xv, city, content)
    ret = curs.execute(sql)
    conn.commit()
    curs.close()
    curs.close()
 
def getUrl(url):
    req = urllib2.Request(url)
    content = urllib2.urlopen(req).read()
    typeEncode = sys.getfilesystemencoding()
    infoencode = chardet.detect(content).get('encoding','utf-8')
    html = content.decode(infoencode,'ignore').encode(typeEncode)
    return html

def getLastDataNum():
    url = 'http://www.chinahighway.gov.cn/roadInfo/queryRoadInfo.do?queryType=map&startDate=&cantonName=&cantonCode=&infoType=3&endDate=&startPlanDate=&_page_size=10&roadName=&mapList=-1&endRealDate=&roadCode=&provinceList=-1&endPlanDate=&startRealDate=&page=1'
    data = getUrl(url)
    p = re.compile(r'[<][\s\w=\":]{20}show[\(\d\'\)\"]{11}')
    d = p.findall(data)
    s = True

    for i in d:
        LASTNUM.append(i.split('(')[1].split('\'')[1])
    while s:
        s = False
        for j in range(len(LASTNUM)-1):
            if int(LASTNUM[j]) > int(LASTNUM[j+1]):
                temp = int(LASTNUM[j+1])
                LASTNUM[j+1] = int(LASTNUM[j])
                LASTNUM[j] = int(temp)
                s = True
    return int(LASTNUM[-1])

def getData():
    reload(sys)
    sys.setdefaultencoding('utf8')

    with open('/tmp/dt','r') as fd:
        id = fd.readlines()[0].split('\n')[0]
    zdstr = re.compile(r'<TD CLASS=h12 nowrap>[\d\s:-]{16}')
    titlestr = re.compile(u'<TITLE>(.*)</TITLE>')
    contentstr = re.compile(u'<TD colspan=3 CLASS=h12>[\s]{2}(.*)</font>')
    ct = re.compile(ur'..')
    xlstr = re.compile(r'[\w\d]{2,5}')
    
    for i in range(int(id),getLastDataNum()):
        url = "http://www.chinahighway.gov.cn/roadInfo/getRoadInfo.do?roadInfoId=%s" % i
        data = getUrl(url)
        zd = zdstr.findall(data)
        titleName = titlestr.findall(data)
        contentName = contentstr.findall(data)
        zddate = zd[0].split('>')[1]
        title = titleName[0].split(')')[1]      #title
        xl = titleName[0].split(')')[0]+')'     #xl include number and name
        xn = xlstr.match(xl).group(0)           #xl number
        xv = xl.split('(')[1].split(')')[0]     #xl name
        content = contentName[0].split('<')[0].strip()    #content
        city = ct.match(title.decode('utf8')).group(0)    #value
        connMysql(title.decode('utf8'), zddate, xn, xv.decode('utf8'), city.decode('utf8'), content.decode('utf8'))
        time.sleep(1)
        
if __name__ == "__main__":
    getData()
    with open('/tmp/dt','w') as fd:
        fd.write(str(getLastDataNum()))