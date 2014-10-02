# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
import urllib2
from xml.etree import ElementTree
from collections import namedtuple

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name=_('Category Name'))
    slug = models.SlugField(max_length=32, unique=True, verbose_name=_('Category Slug'))
    position = models.IntegerField(default=0, verbose_name=_('Position'))
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Time'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name=_('Updated Time'))
    
    @property
    def feeds(self):
        return self.feed_set.all()

    class meta:
        db_table = 'readers_categories'
        verbose_name = ugettext('Reader Category')
        verbose_name_plural = ugettext('Reader Categories')
        
    def __unicode__(self):
        return self.name

class Feed(models.Model):
    
    category = models.ForeignKey(Category, verbose_name=_('Reader Category'))
    title = models.CharField(max_length=200, verbose_name=_('Feed Title'))
    url = models.URLField(max_length=200, unique=True, verbose_name=_('Feed Url'))
    position = models.IntegerField(default=0, verbose_name=_('Position'))
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Time'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name=_('Updated Time'))
    
    _element_tree = None
    
    @property
    def element_tree(self):
        """Get feed xml object."""
        if self._element_tree is None:
            user_agent = 'Mozilla/5.0 (Windows NT 6.2; WOW64) '\
                         'AppleWebKit/537.36 (KHTML, like Gecko) '\
                         'Chrome/36.0.1985.125 Safari/537.36'
            headers = {'User-Agent': user_agent}
            req = urllib2.Request(self.url, headers=headers)
            response = urllib2.urlopen(req)
            self._element_tree = ElementTree.parse(response)
        return self._element_tree

    @property
    def desc(self):
        return self.element_tree.find("./channel/description").text

    @property
    def items(self):
        rowset = []
        FeedItem = namedtuple('FeedItem', 'title,link,description,comments')
        for item in self.element_tree.findall('./channel/item'):
            rowset.append(FeedItem(
                title = item.find('./title').text,
                link = item.find('./link').text,
                description = item.find('./description').text,
                comments = item.find('./comments').text,
            ))
        return rowset

    class meta:
        db_table = 'readers_feeds'
        verbose_name = ugettext('Reader Feed')
        verbose_name_plural = ugettext('Reader Feeds')
        
    def __unicode__(self):
        return self.title