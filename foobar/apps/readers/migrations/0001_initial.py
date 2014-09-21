# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200, verbose_name='Category Name')),
                ('slug', models.SlugField(unique=True, max_length=32, verbose_name='Category Slug')),
                ('position', models.IntegerField(default=0, verbose_name='Position')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Updated Time')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Feed Title')),
                ('url', models.URLField(unique=True, verbose_name='Feed Url')),
                ('position', models.IntegerField(default=0, verbose_name='Position')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Updated Time')),
                ('category', models.ForeignKey(verbose_name='Reader Category', to='readers.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
