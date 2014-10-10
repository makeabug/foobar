# -*- coding: utf-8 -*-

from django.views import generic

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Feed, Category


@api_view(('GET',))
def api(request, format=None):
    return Response({
            	'detail': reverse('detail', request=request, format=format),
            })

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