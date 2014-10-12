from django.conf.urls import patterns, url
from foobar.apps.readers import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
	
	url(r'^api/', views.api_root, name='api'),
	url(r'^articles/', views.ArticleListView.as_view(), name='articles'),
)