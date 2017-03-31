from django.conf.urls import patterns, url
from wxgigo.admin.core import views

from contrib.admin.core import web_auth_views

urlpatterns = patterns('',
                       # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # always get the first record
    url(r'^$', views.main),
                       #url(r'^auth/sns_base/', views.test),
    url(r'^auth/sns_userinfo/', web_auth_views.SnsUserinfoWebView.as_view(), name='core.auth.sns_userinfo'),
                       url(r'^auth/sns_base/$', web_auth_views.SnsBaseWebView.as_view(), name='core.auth.sns_base'),
                       url(r'^web/user_info/$', web_auth_views.web_user_info, name='core.web.user_info'),
                       url(r'^user/basic_info/$', web_auth_views.sys_user_info, name='core.user.basic_info'),
                       )
