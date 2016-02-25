# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('images_id', models.CharField(default=b'', max_length=100)),
                ('name', models.CharField(default=b'', max_length=100)),
                ('version', models.CharField(default=b'', max_length=40)),
                ('created', models.CharField(default=b'', max_length=40)),
                ('virtual_size', models.CharField(default=b'', max_length=20)),
            ],
        ),
    ]
