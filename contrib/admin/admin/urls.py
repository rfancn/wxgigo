from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # always get the first record
    url(r'^$', include('wxmp.admin.dashboard.urls')),
    url(r'^dashboard/', include('wxmp.admin.dashboard.urls')),
    url(r'^config/', include('wxmp.admin.config.urls')),
    url(r'^plugin/', include('wxmp.admin.plugin.urls')),
    url(r'^test/', TemplateView.as_view(template_name='test.html')),
)
