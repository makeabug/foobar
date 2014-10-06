# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readers', '0002_auto_20141006_2204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='position',
        ),
        migrations.AddField(
            model_name='feed',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is Active'),
            preserve_default=True,
        ),
    ]
