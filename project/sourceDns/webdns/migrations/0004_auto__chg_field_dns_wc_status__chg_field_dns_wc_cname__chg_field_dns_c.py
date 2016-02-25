# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Dns.wc_status'
        db.alter_column(u'webdns_dns', 'wc_status', self.gf('django.db.models.fields.CharField')(max_length=4, null=True))

        # Changing field 'Dns.wc_cname'
        db.alter_column(u'webdns_dns', 'wc_cname', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Dns.cc_cname'
        db.alter_column(u'webdns_dns', 'cc_cname', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Dns.source_ip'
        db.alter_column(u'webdns_dns', 'source_ip', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Dns.domain'
        db.alter_column(u'webdns_dns', 'domain', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Dns.owner'
        db.alter_column(u'webdns_dns', 'owner', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

        # Changing field 'Dns.cc_status'
        db.alter_column(u'webdns_dns', 'cc_status', self.gf('django.db.models.fields.CharField')(max_length=4, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Dns.wc_status'
        raise RuntimeError("Cannot reverse this migration. 'Dns.wc_status' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Dns.wc_status'
        db.alter_column(u'webdns_dns', 'wc_status', self.gf('django.db.models.fields.CharField')(max_length=4))

        # User chose to not deal with backwards NULL issues for 'Dns.wc_cname'
        raise RuntimeError("Cannot reverse this migration. 'Dns.wc_cname' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Dns.wc_cname'
        db.alter_column(u'webdns_dns', 'wc_cname', self.gf('django.db.models.fields.CharField')(max_length=100))

        # User chose to not deal with backwards NULL issues for 'Dns.cc_cname'
        raise RuntimeError("Cannot reverse this migration. 'Dns.cc_cname' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Dns.cc_cname'
        db.alter_column(u'webdns_dns', 'cc_cname', self.gf('django.db.models.fields.CharField')(max_length=100))

        # User chose to not deal with backwards NULL issues for 'Dns.source_ip'
        raise RuntimeError("Cannot reverse this migration. 'Dns.source_ip' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Dns.source_ip'
        db.alter_column(u'webdns_dns', 'source_ip', self.gf('django.db.models.fields.CharField')(max_length=100))

        # User chose to not deal with backwards NULL issues for 'Dns.domain'
        raise RuntimeError("Cannot reverse this migration. 'Dns.domain' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Dns.domain'
        db.alter_column(u'webdns_dns', 'domain', self.gf('django.db.models.fields.CharField')(max_length=100))

        # User chose to not deal with backwards NULL issues for 'Dns.owner'
        raise RuntimeError("Cannot reverse this migration. 'Dns.owner' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Dns.owner'
        db.alter_column(u'webdns_dns', 'owner', self.gf('django.db.models.fields.CharField')(max_length=10))

        # User chose to not deal with backwards NULL issues for 'Dns.cc_status'
        raise RuntimeError("Cannot reverse this migration. 'Dns.cc_status' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Dns.cc_status'
        db.alter_column(u'webdns_dns', 'cc_status', self.gf('django.db.models.fields.CharField')(max_length=4))

    models = {
        u'webdns.dns': {
            'Meta': {'object_name': 'Dns'},
            'cache_Content': ('django.db.models.fields.TextField', [], {}),
            'cc_cname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'cc_status': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
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
        u'webdns.upload': {
            'Meta': {'object_name': 'Upload'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'upload_dir': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['webdns']