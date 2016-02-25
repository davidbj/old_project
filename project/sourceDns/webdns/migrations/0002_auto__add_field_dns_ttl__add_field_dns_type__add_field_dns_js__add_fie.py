# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Dns.ttl'
        db.add_column(u'webdns_dns', 'ttl',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=10),
                      keep_default=False)

        # Adding field 'Dns.type'
        db.add_column(u'webdns_dns', 'type',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=10),
                      keep_default=False)

        # Adding field 'Dns.js'
        db.add_column(u'webdns_dns', 'js',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=4),
                      keep_default=False)

        # Adding field 'Dns.sm'
        db.add_column(u'webdns_dns', 'sm',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Dns.ttl'
        db.delete_column(u'webdns_dns', 'ttl')

        # Deleting field 'Dns.type'
        db.delete_column(u'webdns_dns', 'type')

        # Deleting field 'Dns.js'
        db.delete_column(u'webdns_dns', 'js')

        # Deleting field 'Dns.sm'
        db.delete_column(u'webdns_dns', 'sm')


    models = {
        u'webdns.dns': {
            'Meta': {'object_name': 'Dns'},
            'cache_Content': ('django.db.models.fields.TextField', [], {}),
            'cc_cname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cc_status': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'js': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'sm': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'source_ip': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ttl': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'wc_cname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'wc_status': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        u'webdns.upload': {
            'Meta': {'object_name': 'Upload'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'upload_dir': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['webdns']