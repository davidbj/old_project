#-*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from forms import UploadFileForm, DomainForm
from datetime import datetime
from webdns.models import Dns, Upload, Domain, UserPermission
from webdns.db import mdelete, select
from webdns.util import UPLOAD_DIR, changeDns, addDns, updateDns, parserIp, remove
import os
import sys
import xlrd
import re
import urllib
import json
import requests
import logging

#收集日志
logger = logging.getLogger('sourceDns.webdns.views')

def index(req):
    """
        function:回源DNS 首页
        message: 
            1 --dns和数据库都插入成功.
            2 --dns更新成功,数据库操作失败.
            3 --dns操作失败,数据库未操作.
            4 --标识的意思
        info:
            1 --当info==1,在模板页alert弹出消息.
            2 --标识的意思
    """

    #单点登入验证
    if req.GET.get('rest'):
        rest = req.GET.get('rest')
        req.session['rest']=rest
        cookies={'JSESSIONID':rest}
        d=requests.get('http://upload.oss.david.cn:9340/getuser?project=huiyuan',cookies=cookies)
        req.session['username']=json.loads(d.text)['username']
        username =  req.session.get('username', None)
    else:
        username = req.session.get('username', None)

    if username:
        #二级域名组遍历
        gdata = Domain.objects.all()
        limit=10
        dc={}
        if req.method == 'POST':
            info = '2'
            message='4'
            cid=0
            if req.POST.get('fid') == '1':
                id = req.POST.get('id')
                domain = req.POST.get('f_domain')
                type = req.POST.get('type')
                ttl = req.POST.get('ttl')
                source_ip = req.POST.get('source_ip')
                cc_cname = req.POST.get('cc_cname')
                wc_cname = req.POST.get('wc_cname')
                js = req.POST.get('js')
                owner = req.POST.get('f_owner')
                cache_Content = req.POST.get('cache_Content')
                sm = req.POST.get('sm')
                host = req.POST.get('f_host')
                source_ip = parserIp(source_ip)
                if id:
                    info='1'
                    code = updateDns(host, domain, source_ip, ttl, type) 
                    if code:
                        try:
                            saveData(id, source_ip, domain, type, ttl, cc_cname, wc_cname, js, owner, cache_Content, sm, host)
                            message='1'
                        except Exception, e:
                            message='2'
                            logger.error(e)
                            
                    else:
                        message='3'
                    cid = id

            host = req.POST.get('host')
            domain = req.POST.get('domain')
            owner = req.POST.get('owner')
            data = selectFilter(host, domain, owner)

            if host:
                dc['host']=host
            if domain:
                dc['domain']=domain
            if owner:
                dc['owner']=owner
        else:
            info = '2'
            message='4'
            cid = req.GET.get('cid')
            if not cid:
                cid=0

            host = req.GET.get('host')
            domain = req.GET.get('domain')
            owner = req.GET.get('owner')
            if host:
                dc['host']=host
            if domain:
                dc['domain']=domain
            if owner:
                dc['owner']=owner
            data = selectFilter(host, domain, owner)

        #分页
        paginator = Paginator(data, limit)
        page = req.GET.get('page')
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        
        #权限管理
        user = req.session['username']
        ld = permission()

        return render(req, 'index.html', {'data': data, 'gdata':gdata, 'dc':dc, 'permission':ld, 'user':user, 'message':message, 'info':info, 'cid':int(cid)})
    else:
        return HttpResponseRedirect('http://upload.oss.david.cn:9340/index?project=huiyuan&url=http://115.182.94.177')

def busi(req):
    """
    function:增加和编辑记录.
    message: 
        1 --dns和数据库都插入成功.
        2 --dns更新成功,数据库操作失败.
        3 --dns操作失败,数据库未操作.
        4 --标识的意思
    """

    if req.session.get('username', None):
        #权限管理
        ld = permission()
        user = req.session.get('username')
        if user in ld:
            data = Domain.objects.all()
            if req.method == "POST":
                id = req.POST.get('id')
                domain = req.POST.get('domain')
                type = req.POST.get('type')
                ttl = req.POST.get('ttl')
                source_ip = req.POST.get('source_ip')
                cc_cname = req.POST.get('cc_cname')
                wc_cname = req.POST.get('wc_cname')
                js = req.POST.get('js')
                owner = req.POST.get('owner')
                cache_Content = req.POST.get('cache_Content')
                sm = req.POST.get('sm')
                host = req.POST.get('host')
                source_ip = parserIp(source_ip)
                if id:
                    code = updateDns(host, domain, source_ip, ttl, type) 
                else:
                    code = addDns(host, domain, source_ip, ttl, type)
                if code:
                    try:
                        saveData(id, source_ip, domain, type, ttl, cc_cname, wc_cname, js, owner, cache_Content, sm, host)
                        message='1'
                        return render(req, 'busi.html', {'message':message, 'cid':id})
                    except Exception, e:
                        message='2'
                        logger.error(e)
                        return render(req, 'busi.html', {'message':message})
                else:
                    message='3'
                    return render(req, 'busi.html', {'message':message})
            else:
                id = req.GET.get('id')
                message='4'
                if id:
                    query = Dns.objects.filter(id='%s' % id).first()
                    if int(id) != 0:
                        p1 = re.compile(r'\s')
                        d1 = re.findall(p1, query.source_ip)
                        if d1:
                            query.source_ip = query.source_ip.replace(' ', '\n')
                    return render(req, 'busi.html', {'data':data, 'query':query, 'message':message})
            return render(req, 'busi.html', {'data':data, 'message':message})
        else:
            return HttpResponse('权限被拒绝!')
    else:
        return HttpResponseRedirect('http://upload.oss.david.cn:9340/index?project=huiyuan&url=http://115.182.94.177')

def xls(req):
    """通过XML 方式批量添加记录."""

    if req.session.get('username', None):
        #权限管理
        ld = permission()
        user = req.session['username']

        if user in ld:
            dt = datetime.now()
            if req.method == "POST":
                uf = UploadFileForm(req.POST, req.FILES)
                if uf.is_valid():
                    try:
                        mdelete()
                        f = uf.cleaned_data['file']
                        u = Upload(upload_dir=f)
                        u.save()
                    except Exception, e: 
                        logger.error(e)
                        sys.exit(1)
                    dir = select()
                    parserxls(dir)
                    return HttpResponse('ok')
            return render(req, 'xls.html')
        else:
            return HttpResponse('权限被解决')
    else:
        return HttpResponseRedirect('http://upload.oss.david.cn:9340/index?project=huiyuan&url=http://115.182.94.177')

def list(req):
    """查询解析记录"""

    if req.session.get('username', None):
        if req.method == "GET":
            id = req.GET.get('id')
            data = Dns.objects.filter(id=id).first()
        return render(req, 'list.html', {'data':data})
    else:
        return HttpResponseRedirect('http://upload.oss.david.cn:9340/index?project=huiyuan&url=http://115.182.94.177')

def domain(req):
    """添加二级域名"""
    if req.session.get('username',None):
        #权限管理
        ld = permission()
        user = req.session['username']
        if user in ld:
            if req.method == "POST":
                uf = DomainForm(req.POST, req.FILES)
                if uf.is_valid():
                    domain = uf.cleaned_data['domain']
                    content = uf.cleaned_data['content']
                    d = Domain(domain=domain, content=content)
                    d.save()
                    return HttpResponse(u'添加成功')
            else:
                uf=DomainForm()
            return render(req, 'domain.html', {'uf':uf})
        else:
            return HttpResponse('权限被拒绝')
    else:
        return HttpResponseRedirect('http://upload.oss.david.cn:9340/index?project=huiyuan&url=http://115.182.94.177')

def delete(req):
    """删除记录"""
    if req.session.get('username', None): 
        #权限管理
        ld = permission()
        user = req.session['username']
        if user in ld:
            if req.method == "GET":
                id = req.GET.get('id')
                ids = req.GET.get('ids')
                if id:
                    data = Dns.objects.filter(id=id).first()
                    domain = data.domain
                    host = data.host
                    code = remove(domain, host)
                    if code:
                        try:
                            data.delete()
                        except Exception, e:
                            logger.error(e)
                            return HttpResponse('<script>alert("数据库删除失败!");location.replace("/")</script>')
                    else:
                        return HttpResponse('<script>alert("Dns删除操作失败!");location.replace("/")</script>')
                if ids:
                    #print ids
                    ids = ids.split(',')
                    for i in ids:
                        data = Dns.objects.filter(id=i).first()
                        domain = data.domain
                        host = data.host
                        code = remove(domain, host)
                        if code:
                            try:
                                data.delete()
                            except Exception, e:
                                logger.error(e)
                                return HttpResponse('<script>alert("数据库删除失败!");location.replace("/")</script>')
                        else:
                            return HttpResponse('<script>alert("Dns记录删除失败!");location.replace("/")</script>')
            return HttpResponse('<script>alert("Dns记录删除成功!");location.replace("/")</script>')
        else:
            return HttpResponse('权限被拒绝')
    else:
        return HttpResponseRedirect('http://upload.oss.david.cn:9340/index?project=huiyuan&url=http://115.182.94.177')

def logout(req):
    '''退出登入'''

    if req.session.get('username', None):
        if req.method == "GET":
            user = req.GET.get('user')
            req.session['username']=None
            return HttpResponse('<script>top.location.href="http://cas.oss.david.cn:7777/cas/logout"</script>') 
    else:
        return HttpResponseRedirect('http://upload.oss.david.cn:9340/index?project=huiyuan&url=http://115.182.94.177')

def selectFilter(host, domain, owner):
    if host and domain and owner:
        data = Dns.objects.filter(host=host, domain=domain, owner=owner).all()
    elif host and domain:
        data = Dns.objects.filter(host=host, domain=domain).all()
    elif host and owner:
        data = Dns.objects.filter(host=host, owner=owner).all()
    elif domain and owner:
        data = Dns.objects.filter(domain=domain, owner=owner).all()
    elif host:
        data = Dns.objects.filter(host=host).all()
    elif domain:
        data = Dns.objects.filter(domain=domain).all()
    elif owner:
        data = Dns.objects.filter(owner=owner).all()
    else:
        data = Dns.objects.all()
    return data

def permission():
    ld = []
    permission = UserPermission.objects.filter(group_name='admin').all()
    for i in permission:
        ld.append(i.user)
    return ld

def parserxls(dir):
    path = os.path.join(UPLOAD_DIR, dir)
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrows = table.nrows
    for i in range(nrows):
        if i > 0:
            host = table.row_values(i)[0]
            domain = table.row_values(i)[1]
            owner = table.row_values(i)[2]
            wc_cname = table.row_values(i)[3]
            wc_status = table.row_values(i)[4]
            js = table.row_values(i)[5]
            source_ip = table.row_values(i)[6]
            cc_cname = table.row_values(i)[7]
            cc_status = table.row_values(i)[8]
            sm = table.row_values(i)[9]
            cache_Content = table.row_values(i)[10]
            type = 'A'
            ttl = '600'
            
            dns = Dns()
            dns.host = host
            dns.domain = domain
            dns.owner = owner
            dns.wc_cname = wc_cname
            dns.wc_status = wc_status
            dns.source_ip = source_ip
            dns.ttl = ttl
            dns.type = type
            dns.js = js
            dns.sm = sm
            dns.cc_cname = cc_cname
            dns.cc_status = cc_status
            dns.cache_Content = cache_Content
            dns.save()
            print changeDns(host, domain, source_ip, ttl, type)
    return domain 

def saveData(id, source_ip, domain, type, ttl, cc_cname, wc_cname, js, owner, cache_Content, sm, host):
    dns = Dns()
    source_ip = '\n'.join(source_ip)
    if id:
        dns.id = id
    dns.source_ip = source_ip
    dns.domain = domain
    dns.type = type
    dns.ttl = ttl
    dns.cc_cname = cc_cname
    dns.wc_cname = wc_cname
    dns.js = js
    dns.owner = owner
    dns.cache_Content = cache_Content
    dns.sm = sm
    dns.host = host
    dns.save()

def check_form(req):
    host = req.GET.get('host')
    domain = req.GET.get('domain')
    code = Dns.objects.filter(host=host, domain=domain).all()
    if code:
        return HttpResponse("<font color=red>主机名已存在</font>")
    else:
        return HttpResponse("<font color=green>主机名可以使用</font>")
