from __future__ import absolute_import

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from contrib.admin import views, bindviews

urlpatterns = patterns('',
                       # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # always get the first record
    url(r'^$', views.IndexView.as_view(), name='apps.member.index'),
                       # bind
    url(r'^bind/$', bindviews.BindView.as_view(), name='apps.member.bind'),
                       url(r'^bind/success/$', TemplateView.as_view(template_name='apps/member/bind-success.html'), name='apps.member.bind-success'),
                       url(r'^bind/error/$', TemplateView.as_view(template_name='apps/member/bind-error.html'), name='apps.member.bind-error'),
                       url(r'^bind/already/$', TemplateView.as_view(template_name='apps/member/bind-already.html'), name='apps.member.bind-already'),
                       # qrcode
    url(r'^myqrcode/$', views.myqrcode, name='apps.member.my-qrcode'),

                       # open_id
    url(r'^base/$', views.BaseView.as_view(), name='apps.member.base'),
                       url(r'^userinfo/$', views.UserInfoView.as_view(), name='apps.member.userinfo'),
                       url(r'^test/$', views.TestView.as_view(), name='apps.member.test'),
                       )
