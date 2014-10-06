# -*- coding: utf-8 -*-
import os
import sys

# CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
# BASE_PATH = os.path.normpath(os.path.join(CURRENT_PATH, '../../../../../../'))

# sys.path.append(os.path.normpath(os.path.join(BASE_PATH, 'foobar')))

from django.core.management.base import BaseCommand, CommandError
from foobar.apps.readers.models import Feed
import time

class Command(BaseCommand):
    args = '<>'
    help = 'Fetch all articles'

    def handle(self, *args, **options):
        func_start_time = time.time()
        
        result = Feed.fetchAll()

        print '{0} articles was successfully saved.'.format(result)
        print 'done, used: {0} s'.format(round(time.time() - func_start_time, 3))