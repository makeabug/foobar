# -*- coding: utf-8 -*-

from django.views import generic
from .models import Feed

class IndexView(generic.ListView):
	template_name = 'readers/main.html'
	
	def get_queryset(self):
		return Feed.objects.all()