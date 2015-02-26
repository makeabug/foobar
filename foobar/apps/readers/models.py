# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
import urllib2
from xml.etree import ElementTree
from collections import namedtuple
from django.core.cache import cache
from django.utils import timezone

import logging
logger = logging.getLogger(__package__)

import traceback

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
        verbose_name = ugettext('Category')
        verbose_name_plural = ugettext('Categories')

    def __unicode__(self):
        return self.name

class Feed(models.Model):

    category = models.ForeignKey(Category, verbose_name=_('Category'))
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    url = models.URLField(max_length=200, unique=True, verbose_name=_('URL'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Time'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name=_('Updated Time'))

    _element_tree = None

    @property
    def content(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.2; WOW64) '\
                     'AppleWebKit/537.36 (KHTML, like Gecko) '\
                     'Chrome/36.0.1985.125 Safari/537.36'
        headers = {'User-Agent': user_agent}
        req = urllib2.Request(self.url, headers=headers)
        response = urllib2.urlopen(req)
        return response

    @property
    def element_tree(self):
        """Get feed xml object."""
        if self._element_tree is None:
            self._element_tree = ElementTree.parse(self.content)
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

    def fetch(self):
        total = 0
        namespaces = {
            'dc': 'http://purl.org/dc/elements/1.1/',
            'wfw': 'http://wellformedweb.org/CommentAPI/',
            'slash': 'http://purl.org/rss/1.0/modules/slash/',
            'content': "http://purl.org/rss/1.0/modules/content/",
        }
        date_fmt = '%a, %d %b %Y %H:%M:%S'

        for item in self.element_tree.findall('./channel/item'):
            try:
                creator = item.find('./dc:creator', namespaces)
                article, created = Article.objects.update_or_create(
                    feed = self,
                    link = item.find('./link').text,
                    defaults = {
                        'title': item.find('./title').text,
                        'description': item.find('./description').text,
                        'pub_date': timezone.datetime.strptime(item.find('./pubDate').text[:-6], date_fmt),
                        'dc_creator': u'佚名' if creator is None else creator.text
                    }
                )

                for tag in item.findall('./category'):
                    t, created = Tag.objects.get_or_create(name=tag.text)
                    article.tags.add(t)

                total += 1
            except Exception as e:
                logger.error(u'Fetch feed:{0} has error:{1}'.format(self.title, e.message))
                traceback.print_exc()
        return total

    @classmethod
    def fetchAll(cls):
        return reduce(
            lambda x, y: x.fetch() + y.fetch(), 
            cls.objects.filter(is_active=True)
        )

    class meta:
        db_table = 'readers_feeds'
        verbose_name = ugettext('Feed')
        verbose_name_plural = ugettext('Feeds')

    def __unicode__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    counter = models.IntegerField(default=0, verbose_name=_('Counter'))

    class meta:
        db_table = 'readers_tags'
        verbose_name = ugettext('Tag')
        verbose_name_plural = ugettext('Tag')

    def __unicode__(self):
        return self.name

class Article(models.Model):
    feed = models.ForeignKey(Feed, verbose_name=_('Feed'))
    title = models.CharField(max_length=256, verbose_name=_('Title'))
    link = models.URLField(max_length=200, unique=True, verbose_name=_('Link'))
    pub_date = models.DateTimeField(null=True, verbose_name=_('Pub Date'))
    dc_creator = models.CharField(max_length=128, verbose_name=_('Creator'))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_('Tag'))
    description = models.TextField(default='', verbose_name=_('Description'))
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Time'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name=_('Updated Time'))

    class meta:
        db_table = 'readers_articles'
        verbose_name = ugettext('Article')
        verbose_name_plural = ugettext('Articles')

