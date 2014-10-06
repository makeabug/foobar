# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('link', models.URLField(unique=True, verbose_name='Link')),
                ('comments', models.URLField(verbose_name='Comment')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Pub Date')),
                ('dc_creator', models.CharField(max_length=128, verbose_name='Creator')),
                ('tag', models.CharField(max_length=256, verbose_name='Tag')),
                ('description', models.TextField(default=b'', verbose_name='Description')),
                ('content', models.TextField(default=b'', verbose_name='Content')),
                ('comment_rss', models.URLField(verbose_name='Comment Rss')),
                ('slash_comments', models.IntegerField(default=0, verbose_name='Slash Comments')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Updated Time')),
                ('feed', models.ForeignKey(verbose_name='Feed', to='readers.Feed')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='feed',
            name='category',
            field=models.ForeignKey(verbose_name='Category', to='readers.Category'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='feed',
            name='url',
            field=models.URLField(unique=True, verbose_name='URL'),
        ),
    ]
