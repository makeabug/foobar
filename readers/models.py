
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name=_('Category Name'))
    slug = models.SlugField(max_length=32, unique=True, verbose_name=_('Category Slug'))
    position = models.IntegerField(default=0, verbose_name=_('Position'))
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Time'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name=_('Updated Time'))
    
    class meta:
        db_table = 'readers_categories'
        verbose_name = _('Reader Category')
        verbose_name_plural = _('Reder Categories')
        
    def __unicode__(self):
        return self.name

class Feed(models.Model):
    category = models.ForeignKey(Category, verbose_name=_('Reader Category'))
    title = models.CharField(max_length=200, verbose_name=_('Feed Title'))
    url = models.URLField(max_length=200, unique=True, verbose_name=_('Feed Url'))
    position = models.IntegerField(default=0, verbose_name=_('Position'))
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Time'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name=_('Updated Time'))
    
    class meta:
        db_table = 'readers_feeds'
        verbose_name = _('Reader Feed')
        verbose_name_plural = _('Reader Feeds')
        
    def __unicode__(self):
        return self.title