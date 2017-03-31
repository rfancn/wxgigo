from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # always get the first record
    url(r'^member/', include('web.apps.member.urls')),
)
