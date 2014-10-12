# -*- coding: utf-8 -*-

from rest_framework import serializers
from django.utils import timezone

from .models import Article

class LocalDateTimeField(serializers.DateTimeField):

    def to_native(self, value):
        return value.astimezone(timezone.get_current_timezone()).strftime(self.format)

class ArticleSerializer(serializers.ModelSerializer):

    pub_date = LocalDateTimeField('pub_date', format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Article
        fields = ('id', 'title', 'link', 'description', 'pub_date', 'comments',)
