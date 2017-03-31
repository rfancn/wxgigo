from __future__ import absolute_import

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from contrib.admin.admin.config import views

urlpatterns = patterns('',
                       # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # always get the first record
    url(r'^$', login_required(views.ConfigDetailView.as_view())),
                       url(r'^load/$', login_required(views.WXMPConfigActionView.as_view())),
                       url(r'^save/$', login_required(views.WXMPConfigActionView.as_view())),
                       url(r'^edit/$', login_required(views.ConfigUpdateView.as_view())),
                       )
