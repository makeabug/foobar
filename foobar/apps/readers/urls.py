from django.conf.urls import patterns, url
from foobar.apps.readers import views

urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index')
)