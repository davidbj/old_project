#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from bind.models import UserPermission, Zone, Letv_ct, Letv_any, Upload
from bind.util import parserIp, UPLOAD_DIR
import xlrd
from datetime import datetime
from bind.db import mdelete, select
from forms import UploadFileForm
import os, sys, logging
import requests, json

logger = logging.getLogger('webdns.bind.views')

def index(req):
    '''回源DNS 首页'''

    zones = Zone.objects.all()  #二级域名
    limit=5                     #分页显示行数
    dc={}                   
   
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
        user = req.session.get('username', None)
        up = UserPermission.objects.filter(user='%s' % user).first()    #权限管理

        if req.method == 'GET':
            host = req.GET.get('host')
            zone = req.GET.get('zone')
            ip = req.GET.get('ip')
            owner = req.GET.get('owner')
            operator = req.GET.get('operator')
            data = selectFilter(host, zone, owner, ip, operator)
            if host:
                dc['host'] = host
            if zone:
                dc['zone'] = zone
            if ip:
                dc['ip'] = ip
            if owner:
                dc['owner'] = owner
            if operator:
                dc['operator'] = operator
        elif req.method == 'POST':
            host = req.POST.get('host')
            zone = req.POST.get('zone')
            ip = req.POST.get('ip')
            owner = req.POST.get('owner')
            operator = req.POST.get('operator')
            data = selectFilter(host, zone, owner, ip, operator)
            if host:
                dc['host'] = host
            if zone:
                dc['zone'] = zone
            if ip:
                dc['ip'] = ip
            if owner:
                dc['owner'] = owner
            if operator:
                dc['operator'] = operator

        paginator = Paginator(data, limit)
        page = req.GET.get('page')
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        return render(req, 'index.html', {'data': data, 'dc':dc, 'zones':zones, 'up':up, 'user':user}) 
    else:
        return HttpResponseRedirect('http://upload.oss.david.cn:9340/index?project=huiyuan&url=http://111.206.210.40') 

def form(req):
    """
    function:增加和编辑记录.
    message: 
        1 --dns和数据库都插入成功.
        2 --dns更新成功,数据库操作失败.
        3 --dns操作失败,数据库未操作.
        4 --标识的意思
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
        user = req.session.get('username', None)
        up = UserPermission.objects.filter(user='%s' % user).first()    #权限管理

        zones = Zone.objects.all()
        if req.method == "POST":
            id = req.POST.get('id')
            zone = req.POST.get('zone')
            type = req.POST.get('ctype')
            ttl = req.POST.get('ttl')
            data = req.POST.get('data')
            cc_cname = req.POST.get('cc_cname')
            wc_cname = req.POST.get('wc_cname')
            cache_content = req.POST.get('cache_content')
            owner = req.POST.get('owner')
            host = req.POST.get('host')
            operator = req.POST.get('operator')
            allAdd = req.POST.get('allAdd')
            print allAdd
            if type == 'A':
                ips = parserIp(data)
            elif type == 'CNAME':
                ip = data
                
            #try:
            if type == 'A':
                try:
                    for ip in ips:
                        saveData(id, ip, zone, type, ttl, cc_cname, wc_cname, owner, cache_content, host, operator, allAdd)
                    message='Y'
                    return render(req, 'form.html', {'message':message, 'operator':operator, 'up':up, 'user':user})
                except Exception, e:
                    logger.error(e)
                    message='N'
                    return render(req, 'form.html', {'message':message, 'operator':operator, 'up':up, 'user':user})
                    
            elif type == 'CNAME':
                try:
                    code = saveData(id, ip, zone, type, ttl, cc_cname, wc_cname, owner, cache_content, host, operator, allAdd)
                    if code and operator == 'ct':
                        message='CNN'
                    elif code and operator == 'any':
                        message='ANN'
                    else:
                        message='Y'
                    return render(req, 'form.html', {'message':message, 'operator':operator, 'up':up, 'user':user})
                except Exception, e:
                    logger.error(e)
                    message='N'
                    return render(req, 'form.html', {'message':message, 'operator':operator, 'up':up, 'user':user})
            else:
                return HttpResponseRedirect('/index.html')
        elif req.method == 'GET':
            id = req.GET.get('id')
            operator = req.GET.get('operator')
            if id:
                if operator == 'ct':
                    query = Letv_ct.objects.filter(id='%s' % id).first()
                    return render(req, 'form.html', {'zones':zones, 'query':query, 'up':up, 'user':user})
                elif operator == 'any':
                    query = Letv_any.objects.filter(id='%s' % id).first()
                    return render(req, 'form.html', {'zones':zones, 'query':query, 'up':up, 'user':user})
                else:
                    return HttpResponse('<script>alert("请选择要修改的运营商;");location.replace("/")</script>')
            else:
                return render(req, 'form.html', {'zones':zones, 'up':up})
    else:
        return HttpResponseRedirect('http://upload.oss.david.cn:9340/index?project=huiyuan&url=http://111.206.210.40') 

def delete(req):
    '''
    Function:记录删除
    '''
    
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
        user = req.session.get('username', None)
        up = UserPermission.objects.filter(user='%s' % user).first()    #权限管理
        if up.group_name == 'admin' or up.group_name == 'super_admin':
            if req.method == 'GET':
                id = req.GET.get('id')
                operator = req.GET.get('operator')
                if id:
                    if operator == 'ct':
                        data = Letv_ct.objects.filter(id='%s' % id).first()
                        try:
                            data.delete()
                            message='Y'
                            return render(req, 'delete.html', {'message':message, 'operator':operator})
                        except Exception,e:
                            logger.error(e)
                            message='N'
                            return render(req, 'delete.html', {'message':message, 'operator':operator})
                    elif operator == 'any':
                        data = Letv_any.objects.filter(id='%s' % id).first()
                        print data
                        try:
                            data.delete()
                            message='Y'
                            return render(req, 'delete.html', {'message':message, 'operator':operator})
                        except Exception,e:
                            logger.error(e) 
                            message='N'
                            return render(req, 'delete.html', {'message':message, 'operator':operator})
                    else:
                        message="NN"
                        return render(req, 'delete.html', {'message':message, 'operator':operator})
            else:
                return HttpResponse('<script>alert("权限不足!")</script>;location.replace("/")')
    else:
        return HttpResponseRedirect('http://upload.oss.david.cn:9340/index?project=huiyuan&url=http://111.206.210.40') 

def zone(req):
    '''zone 管理'''

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
        user = req.session.get('username', None)
        up = UserPermission.objects.filter(user='%s' % user).first()    #权限管理
        zones = Zone.objects.all()
        if req.method == "POST":
            zone = req.POST.get('zone', None)
            content = req.POST.get('content', None)
            id = req.POST.get('id', None)
            
            try:
                qOne = Zone.objects.filter(zone='%s' % zone ).first()
                if not id:
                    if not qOne:
                        addZone(id, zone, content)
                        return HttpResponse('<script>alert("操作成功!");location.replace("/zone.html")</script>')
                    else:
                        return HttpResponse('<script>alert("该Zone已存在");location.replace("/zone.html")</script>')
                else:
                    addZone(id, zone, content)
                    return HttpResponse('<script>alert("操作成功!");location.replace("/zone.html")</script>')
            except Exception, e:
                logger.error(e) 
                return HttpResponse('<script>alert("操作失败!");location.replace("/zone.html")</script>')

        elif req.method == 'GET':
            id = req.GET.get('id')
            if id:
                query = Zone.objects.filter(id='%s' % id).first()
                return render(req, 'zone.html', {'zones':zones, 'query':query, 'up':up, 'user':user})
            else:    
                return render(req, 'zone.html', {'zones':zones, 'up':up, 'user':user})
    else:
        return HttpResponseRedirect('http://upload.oss.david.cn:9340/index?project=huiyuan&url=http://111.206.210.40') 

def delete_zone(req):
    '''删除二级域'''
    
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
        user = req.session.get('username', None)
        up = UserPermission.objects.filter(user='%s' % user).first()    #权限管理
        if up.group_name == 'super_admin' or up.group_name == 'admin':
            if req.method == "GET":
                id = req.GET.get('id')
                try:
                    data = Zone.objects.filter(id="%s" % id).first()
                    data.delete()
                    return HttpResponse('<script>alert("删除成功");location.replace("/zone.html")</script>')
                except Exception, e:
                    logger.error(e)
                    return HttpResponse('<script>alert("删除失败");location.replace("/zone.html")</script>')
        else:
            return HttpResponse('<script>alert("权限不足");location.replace("/")</script>')
    else:
        return HttpResponseRedirect('http://upload.oss.david.cn:9340/index?project=huiyuan&url=http://111.206.210.40') 

def logout(req):
    '''
    Function:退出回源Dns系统
    '''
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
        if req.method == "GET":
            user = req.GET.get('user')
            if user: 
                req.session['username']=None
            return HttpResponse('<script>top.location.href="http://cas.oss.david.cn:7777/cas/logout"</script>')
                 
        else:
            return render(req, 'index.html')
    else:
        return HttpResponseRedirect('http://upload.oss.david.cn:9340/index?project=huiyuan&url=http://111.206.210.40')
def xls(req):
    '''批量添加记录'''
    
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
        user = req.session.get('username', None)
        up = UserPermission.objects.filter(user='%s' % user).first()    #权限管理
        if up.group_name == 'admin' or up.group_name == 'super_admin':
            dt = datetime.now()
            if req.method == 'POST':
                uf = UploadFileForm(req.POST, req.FILES)
                if uf.is_valid():
                    try:
                        mdelete()
                        f = uf.cleaned_data['file']
                        u = Upload(upload_dir=f)
                        u.save()
                    except Exception, e:
                        logger.error(e)


                    dir = select()
                    code = parserxls(dir)
                    if code:
                        return HttpResponse('<script>alert("添加成功!");location.replace("/")</script>')
                    else:
                        return HttpResponse('<script>alert("添加失败!");location.replace("/")</script>') 
                else:
                    return HttpResponse('<script>alert("上传失败!");location.replace("/")</script>')
        else:
            return HttpResponse('<script>alert("权限不足");location.replace("/")</script>')
    else:
        return HttpResponseRedirect('http://upload.oss.david.cn:9340/index?project=huiyuan&url=http://111.206.210.40') 
                
def permission():
    ld=[]
    permission = UserPermission.objects.filter(group_name='admin').all()
    for i in permission:
        ld.append(i.user)
    return ld

def saveData(id, ip, zone, type, ttl, cc_cname, wc_cname, owner, cache_content, host, operator, allAdd):
    if allAdd == '1':
        dl = ['any', 'ct']
        for i in dl:
            if i == 'any':
                dns = Letv_any()
            else:
                dns = Letv_ct()

            if id:
                dns.id = id
            else:
                if i == 'any' and type == 'CNAME':
                    result = Letv_any.objects.filter(host='%s' % host, zone='%s' % zone, operator='%s' % operator).all()
                    if result:
                        return HttpResponse('Errorany')
                elif i == 'ct' and type == 'CNAME':
                    result = Letv_ct.objects.filter(host='%s' % host, zone='%s' % zone, operator='%s' % operator).all()
                    if result:
                        return HttpResponse('Errorct')
            
            dns.data = ip
            dns.zone = zone
            dns.type = type
            dns.ttl = ttl
            dns.cc_cname = cc_cname
            dns.wc_cname = wc_cname
            dns.owner = owner
            dns.cache_content = cache_content
            dns.host = host
            dns.operator = operator
            dns.allAdd = allAdd
            dns.save()
    else:
        if operator == 'ct':
            dns = Letv_ct()  
        elif operator == 'any':
            dns = Letv_any()

        if id:
            dns.id = id
        else:
            if operator == 'ct' and type == 'CNAME':
                result = Letv_ct.objects.filter(host='%s' % host, zone='%s' % zone, operator='%s' % operator).all()
                if result:
                    return HttpResponse('Errorct')
            elif operator == 'any' and type == 'CNAME':
                result = Letv_any.objects.filter(host='%s' % host, zone='%s' % zone, operator='%s' % operator).all()
                if result:
                    return HttpResponse('Errorany')
        dns.data = ip
        dns.zone = zone
        dns.type = type
        dns.ttl = ttl
        dns.cc_cname = cc_cname
        dns.wc_cname = wc_cname
        dns.owner = owner
        dns.cache_content = cache_content
        dns.host = host
        dns.operator = operator
        dns.save()

def addZone(id, zone, content):
    z = Zone()
    if id:
        z.id = id
    z.zone = zone
    z.content = content
    z.save()

def selectFilter(host, zone, owner, ip, operator):
    '''列表页展示'''

    if operator == 'any':
        if host and zone and owner and ip:
            data = Letv_any.objects.filter(host=host, zone=zone, owner=owner, data=ip, status='1').all()
        elif host and zone:
            data = Letv_any.objects.filter(host=host, zone=zone, status='1').all()
        elif host and owner:
            data = Letv_any.objects.filter(host=host, owner=owner, status='1').all()
        elif host and ip:
            data = Letv_any.objects.filter(host=host, data=ip, status='1').all()
        elif zone and owner:
            data = Letv_any.objects.filter(zone=zone, owner=owner, status='1').all()
        elif zone and ip:
            data = Letv_any.objects.filter(zone=zone, data=ip, status='1').all()
        elif owner and ip:
            data = Letv_any.objects.filter(owner=owner, data=ip, status='1').all()
        elif host:
            data = Letv_any.objects.filter(host=host, status='1').all()
        elif zone:
            data = Letv_any.objects.filter(zone=zone, status='1').all()
        elif owner:
            data = Letv_any.objects.filter(owner=owner, status='1').all()
        elif ip:
            data = Letv_any.objects.filter(data=ip, status='1').all()
        else:
            data = Letv_any.objects.filter(status='1').all()
    else:
        if host and zone and owner and ip:
            data = Letv_ct.objects.filter(host=host, zone=zone, owner=owner, data=ip, status='1').all()
        elif host and zone:
            data = Letv_ct.objects.filter(host=host, zone=zone, status='1').all()
        elif host and owner:
            data = Letv_ct.objects.filter(host=host, owner=owner, status='1').all()
        elif host and ip:
            data = Letv_ct.objects.filter(host=host, data=ip, status='1').all()
        elif zone and owner:
            data = Letv_ct.objects.filter(zone=zone, owner=owner, status='1').all()
        elif zone and ip:
            data = Letv_ct.objects.filter(zone=zone, data=ip, status='1').all()
        elif owner and ip:
            data = Letv_ct.objects.filter(owner=owner, data=ip, status='1').all()
        elif host:
            data = Letv_ct.objects.filter(host=host, status='1').all()
        elif zone:
            data = Letv_ct.objects.filter(zone=zone, status='1').all()
        elif owner:
            data = Letv_ct.objects.filter(owner=owner, status='1').all()
        elif ip:
            data = Letv_ct.objects.filter(data=ip, status='1').all()
        else:
            data = Letv_ct.objects.filter(status='1').all()
    return data 

def parserxls(dir):
    '''处理EXCEL'''
    path = os.path.join(UPLOAD_DIR, dir)
    data = xlrd.open_workbook(path)
    table = data.sheets()[0]
    nrows = table.nrows
    
    try:
        for line in range(nrows):
            if line>0:
                host = table.row_values(line)[0]
                zone = table.row_values(line)[1]
                owner = table.row_values(line)[2]
                ip = table.row_values(line)[3]
                type = table.row_values(line)[4]
                ttl = table.row_values(line)[5]
                ttl = str(int(ttl))
                wc_cname = table.row_values(line)[6]
                cc_cname = table.row_values(line)[7]
                operator = table.row_values(line)[8]
                cache_content = table.row_values(line)[9]
                if operator == 'any':
                    dns = Letv_any()
                elif operator == 'ct':
                    dns = Letv_ct()

                dns.host = host
                dns.zone = zone
                dns.owner = owner
                dns.data = ip
                dns.type = type
                dns.ttl = ttl
                dns.wc_cname = wc_cname
                dns.cc_cname = cc_cname
                dns.operator = operator
                dns.cache_content = cache_content
                dns.save()
        return 'true'
    except Exception, e:
        logger.error(e)
