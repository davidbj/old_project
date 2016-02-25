# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Dns'
        db.create_table(u'webdns_dns', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('wc_cname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('wc_status', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('source_ip', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('cc_cname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('cc_status', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('cache_Content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'webdns', ['Dns'])

        # Adding model 'Upload'
        db.create_table(u'webdns_upload', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('upload_dir', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'webdns', ['Upload'])


    def backwards(self, orm):
        # Deleting model 'Dns'
        db.delete_table(u'webdns_dns')

        # Deleting model 'Upload'
        db.delete_table(u'webdns_upload')


    models = {
        u'webdns.dns': {
            'Meta': {'object_name': 'Dns'},
            'cache_Content': ('django.db.models.fields.TextField', [], {}),
            'cc_cname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'cc_status': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'source_ip': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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