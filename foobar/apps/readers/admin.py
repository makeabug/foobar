# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Category, Feed, Article
from django.utils.translation import ugettext, ugettext_lazy as _

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'position', 'updated_time',)
    ordering = ['position', '-created_time']
    list_filter = ['updated_time']

admin.site.register(Category, CategoryAdmin)

class FeedAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'category', 'url_html', 'updated_time',)
    list_filter = ('updated_time', 'category__name',)
    list_editable = ('is_active',)

    def url_html(self, obj):
        return "<a href='{feed.url}' target='_blank'>{feed.url}</a>"\
            .format(feed=obj)
    url_html.short_description = _('URL')
    url_html.allow_tags = True


admin.site.register(Feed, FeedAdmin)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'feed', 'tags_html', 'dc_creator', 'pub_date',
        'created_time')
    fields = ('title_html', ('dc_creator', 'pub_date',), 'desc_html',
        'tags', 'created_time', 'updated_time')
    readonly_fields = ('title_html', 'pub_date', 'dc_creator', 'desc_html',
        'created_time', 'updated_time')
    search_fields = ('title', 'tags__name')
    list_filter = ('pub_date', 'feed', 'tags__name',)
    filter_horizontal = ('tags',)

    def tags_html(self, obj):
        return ', '.join([ tag.name for tag in obj.tags.all()])
    tags_html.short_description = _('Tag')

    def desc_html(self, obj):
        return obj.description
    desc_html.short_description = _('Description')
    desc_html.allow_tags = True

    def title_html(self, obj):
        return u"<a href='{article.link}' target='_blank'>{article.title}</a>"\
            .format(article=obj)
    title_html.short_description = _('Title')
    title_html.allow_tags = True

admin.site.register(Article, ArticleAdmin)