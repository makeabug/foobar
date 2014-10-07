# -*- coding: utf-8 -*-

from django.views import generic
from .models import Feed, Category

class IndexView(generic.ListView):
	template_name = 'readers/index.html'
	
	def get_queryset(self):
		return Feed.objects.all()

class DetailView(generic.DetailView):
	model = Feed
	template_name = 'readers/detail.html'

	def get_context_data(self, **kwargs):
		context = super(DetailView, self).get_context_data(**kwargs)
		context['categories'] = Category.objects.all().order_by('position')
		context['current_category_id'] = self.get_object().category.id
		return context