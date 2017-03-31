from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from contrib.admin.admin import views

urlpatterns = patterns('',
                       # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # always get the first record
    url(r'^$', login_required(views.DashboardView.as_view())),

                       )
