# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readers', '0005_auto_20141019_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='comment_rss',
        ),
        migrations.RemoveField(
            model_name='article',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='article',
            name='content',
        ),
        migrations.RemoveField(
            model_name='article',
            name='slash_comments',
        ),
    ]
