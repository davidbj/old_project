#-*- coding:utf-8 -*-
from django.db import models

# Create your models here.

class Letv_ct(models.Model):
    '''电信视图'''
    zone = models.CharField(max_length=255)
    host = models.CharField(max_length=255, default='@')
    type = models.CharField(max_length=6, default='A')
    data = models.CharField(max_length=255, null=True)
    ttl = models.CharField(max_length=11, default='3600', null=True)
    mx_priority = models.CharField(max_length=6, null=True)
    refresh = models.CharField(max_length=11, null=True)
    retry = models.CharField(max_length=11, null=True)
    expire = models.CharField(max_length=11, null=True)
    minimum = models.CharField(max_length=11, null=True)
    serial = models.CharField(max_length=20, null=True)
    resp_person = models.CharField(max_length=255, null=True)
    owner = models.CharField(max_length=10, null=True)
    wc_cname = models.CharField(max_length=10, null=True)
    cc_cname = models.CharField(max_length=10, null=True)
    operator = models.CharField(max_length=10, null=True)
    cache = models.CharField(max_length=2, null=True)
    cache_content = models.TextField(null=True)
    status = models.CharField(max_length=2, null=True, default='1')
    allAdd = models.CharField(max_length=2, null=True, default='0')

    def __unicode__(self):
        return self.host
    
class Letv_any(models.Model):
    '''联通视图'''
    zone = models.CharField(max_length=255)
    host = models.CharField(max_length=255, default='@')
    type = models.CharField(max_length=6, default='A')
    data = models.CharField(max_length=255, null=True)
    ttl = models.CharField(max_length=11, default='3600', null=True)
    mx_priority = models.CharField(max_length=6, null=True)
    refresh = models.CharField(max_length=11, null=True)
    retry = models.CharField(max_length=11, null=True)
    expire = models.CharField(max_length=11, null=True)
    minimum = models.CharField(max_length=11, null=True)
    serial = models.CharField(max_length=20, null=True)
    resp_person = models.CharField(max_length=255, null=True)
    owner = models.CharField(max_length=10, null=True)
    wc_cname = models.CharField(max_length=10, null=True)
    cc_cname = models.CharField(max_length=10, null=True)
    operator = models.CharField(max_length=10, null=True)
    cache = models.CharField(max_length=2, null=True)
    cache_content = models.TextField(null=True)
    status = models.CharField(max_length=2, null=True, default='1')
    allAdd = models.CharField(max_length=2, null=True, default='0')

    def __unicode__(self):
        return self.host

class UserPermission(models.Model):
    '''
    Function:用户权限管理
    Field:
        group_name == 'super_admin'     #超级管理员(查询、批量更改、二级域名修改、记录增删改查)
        group_name == 'admin'           #管理员(查询、二级域名增删改查、记录增删改查)
        group_name == 'user'            #普通用户(查询)
    '''
    group_name = models.CharField(max_length=20, null=True)
    user = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.user

class Zone(models.Model):
    '''
    Function:区域管理
    Field:
        zone    #修改的域名名称
        content #域名描述
    '''
    zone = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    
    def __unicode__(self):
        return self.zone

class Upload(models.Model):
    '''
    Function:批量更改时,存储的上传路径
    Field:
        upload_dir #存储文件上传的路径
    '''
    upload_dir = models.FileField(upload_to='file/')
