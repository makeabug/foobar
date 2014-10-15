# -*- coding: utf-8 -*-

from django.views import generic
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics

from .models import Feed, Category, Article
from .serializers import ArticleSerializer


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'articles': reverse('readers:articles', request=request, format=format),
    })

class IndexView(generic.ListView):
    # model = Article
    template_name = 'readers/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        limit = 20
        articles = Article.objects.all().order_by('-updated_time', '-pub_date')
        paginator = Paginator(articles, limit)

        page = self.request.GET.get('page')
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        return articles

class DetailView(generic.DetailView):
    model = Feed
    template_name = 'readers/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('position')
        context['current_category_id'] = self.get_object().category.id
        return context

class ArticleListView(generics.ListCreateAPIView):
    queryset = Article.objects.all().order_by('-updated_time', '-pub_date')
    serializer_class = ArticleSerializer
    paginate_by = 10