from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from wxmp.admin.plugin.views import PluginListView, WXMPPluginActionView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'web.views.home', name='home'),
    # always get the first record
    url(r'^$', login_required(PluginListView.as_view()), name="plugin-list"),
    url(r'^load_config/$', login_required(WXMPPluginActionView.as_view())),
    url(r'^load_meta/$', login_required(WXMPPluginActionView.as_view())),
    url(r'^save/$', login_required(WXMPPluginActionView.as_view())),
    #url(r'^(?P<action_name>[a-zA-Z]+)/(?P<plugin_uuid>[a-zA-Z0-9]{32})/', login_required(PluginActionView.as_view()), name="plugin-action"),
    #url(r'^load/(?P<plugin_uuid>[a-zA-Z0-9])/$', login_required(PluginActionView.as_view()), name="plugin-action"),
)
