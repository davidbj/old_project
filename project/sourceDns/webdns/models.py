from django.db import models

# Create your models here.

class Dns(models.Model):
    host = models.CharField(max_length=100, null=True)
    domain = models.CharField(max_length=100, null=True)
    owner  = models.CharField(max_length=10, null=True)
    wc_cname = models.CharField(max_length=100, null=True)
    wc_status = models.CharField(max_length=4, null=True)
    source_ip = models.CharField(max_length=100, null=True)
    ttl = models.CharField(max_length=10, null=True)
    type = models.CharField(max_length=10, null=True)
    js = models.CharField(max_length=4, null=True)
    sm = models.CharField(max_length=100, null=True)
    cc_cname = models.CharField(max_length=100, null=True)
    cc_status = models.CharField(max_length=4, null=True)
    cache_Content = models.TextField(null=True)

    def __unicode__(self):
        return self.domain


class Upload(models.Model):
    upload_dir = models.FileField(upload_to='file/')

class Domain(models.Model):
    domain = models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)

    def __unicode__(self):
        return self.domain

class UserPermission(models.Model):
    group_name = models.CharField(max_length=20, null=True)
    user = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.group_name
