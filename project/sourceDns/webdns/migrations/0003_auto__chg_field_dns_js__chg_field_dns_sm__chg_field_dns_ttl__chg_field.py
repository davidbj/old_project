# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Dns.js'
        db.alter_column(u'webdns_dns', 'js', self.gf('django.db.models.fields.CharField')(max_length=4, null=True))

        # Changing field 'Dns.sm'
        db.alter_column(u'webdns_dns', 'sm', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Dns.ttl'
        db.alter_column(u'webdns_dns', 'ttl', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

        # Changing field 'Dns.type'
        db.alter_column(u'webdns_dns', 'type', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Dns.js'
        raise RuntimeError("Cannot reverse this migration. 'Dns.js' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Dns.js'
        db.alter_column(u'webdns_dns', 'js', self.gf('django.db.models.fields.CharField')(max_length=4))

        # User chose to not deal with backwards NULL issues for 'Dns.sm'
        raise RuntimeError("Cannot reverse this migration. 'Dns.sm' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Dns.sm'
        db.alter_column(u'webdns_dns', 'sm', self.gf('django.db.models.fields.CharField')(max_length=100))

        # User chose to not deal with backwards NULL issues for 'Dns.ttl'
        raise RuntimeError("Cannot reverse this migration. 'Dns.ttl' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Dns.ttl'
        db.alter_column(u'webdns_dns', 'ttl', self.gf('django.db.models.fields.CharField')(max_length=10))

        # User chose to not deal with backwards NULL issues for 'Dns.type'
        raise RuntimeError("Cannot reverse this migration. 'Dns.type' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Dns.type'
        db.alter_column(u'webdns_dns', 'type', self.gf('django.db.models.fields.CharField')(max_length=10))

    models = {
        u'webdns.dns': {
            'Meta': {'object_name': 'Dns'},
            'cache_Content': ('django.db.models.fields.TextField', [], {}),
            'cc_cname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cc_status': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'js': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'sm': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'source_ip': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ttl': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
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