# -*- coding: utf-8 -*-

from django.db import models

import logging
logger = logging.getLogger(__package__)

import traceback

class Stock(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Stock Name'))
    code = models.CharField(max_length=200, unique=True, verbose_name=_('Stock Code'))

    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Time'))
    updated_time = models.DateTimeField(auto_now=True, verbose_name=_('Updated Time'))

    class meta:
        db_table = 'stocks_stock'
        verbose_name = ugettext('Stock')
        verbose_name_plural = ugettext('Stocks')

    def __unicode__(self):
        return self.code