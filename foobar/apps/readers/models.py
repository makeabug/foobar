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
    # position = models.IntegerField(default=0, verbose_name=_('Position'))
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

        for item in self.element_tree.findall('./channel/item'):
            try:
                encoded = item.find('./content:encoded', namespaces)
                date_fmt = '%a, %d %b %Y %H:%M:%S +0000'

                attr = {
                    'title': item.find('./title').text,
                    'comments': item.find('./comments').text,
                    'pub_date': timezone.datetime.strptime(item.find('./pubDate').text, date_fmt),
                    'dc_creator': item.find('./dc:creator', namespaces).text,
                    'tag': ','.join([tag.text for tag in item.findall('./category')]),
                    'description': item.find('./description').text,
                    'content': encoded.text if encoded else '',
                    'comment_rss': item.find('./wfw:commentRss', namespaces).text,
                    'slash_comments': item.find('./slash:comments', namespaces).text,
                }

                created, article = Article.objects.get_or_create(
                    link = item.find('./link').text,
                    defaults = dict({'feed': self}, **attr)
                )

                if not created:
                    for field, val in attr.items():
                        setattr(article, field, val)
                    article.save()

                total += 1
            except Exception as e:
                logger.error(u'Fetch feed:{0} has error:{1}'.format(self.title, e.message))
                traceback.print_exc()
        return total

    @classmethod
    def fetchAll(cls):
        feeds = cls.objects.filter(is_active=True)
        total = 0
        for feed in feeds:
            total += feed.fetch()

        return total

    class meta:
        db_table = 'readers_feeds'
        verbose_name = ugettext('Feed')
        verbose_name_plural = ugettext('Feeds')

    def __unicode__(self):
        return self.title

class Article(models.Model):
    feed = models.ForeignKey(Feed, verbose_name=_('Feed'))
    title = models.CharField(max_length=256, verbose_name=_('Title'))
    link = models.URLField(max_length=200, unique=True, verbose_name=_('Link'))
    comments = models.URLField(max_length=200, verbose_name=_('Comment'))
    pub_date = models.DateTimeField(null=True, verbose_name=_('Pub Date'))
    dc_creator = models.CharField(max_length=128, verbose_name=_('Creator'))
    tag = models.CharField(max_length=256, verbose_name=_('Tag'))
    description = models.TextField(default='', verbose_name=_('Description'))
    content = models.TextField(default='', verbose_name=_('Content'))
    comment_rss = models.URLField(max_length=200, verbose_name=_('Comment Rss'))
    slash_comments = models.IntegerField(default=0, verbose_name=_('Slash Comments'))

    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Time'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name=_('Updated Time'))

    class meta:
        db_table = 'readers_articles'
        verbose_name = ugettext('Article')
        verbose_name_plural = ugettext('Articles')
