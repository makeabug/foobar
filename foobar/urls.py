from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'foobar.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'foobar.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^reader/', include('foobar.apps.readers.urls', namespace="readers")),
)
