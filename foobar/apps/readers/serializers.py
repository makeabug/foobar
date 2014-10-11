# -*- coding: utf-8 -*-

from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('title', 'link', 'description', 'pub_date', 'comments',)