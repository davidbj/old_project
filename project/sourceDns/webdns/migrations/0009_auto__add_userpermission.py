# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserPermission'
        db.create_table(u'webdns_userpermission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group_name', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'webdns', ['UserPermission'])


    def backwards(self, orm):
        # Deleting model 'UserPermission'
        db.delete_table(u'webdns_userpermission')


    models = {
        u'webdns.dns': {
            'Meta': {'object_name': 'Dns'},
            'cache_Content': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'cc_cname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'cc_status': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'js': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'sm': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'source_ip': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'ttl': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'wc_cname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'wc_status': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'})
        },
        u'webdns.domain': {
            'Meta': {'object_name': 'Domain'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'webdns.upload': {
            'Meta': {'object_name': 'Upload'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'upload_dir': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'webdns.userpermission': {
            'Meta': {'object_name': 'UserPermission'},
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        }
    }

    complete_apps = ['webdns']