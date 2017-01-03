import logging
import requests

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.generic import View, TemplateView, CreateView
from django.core.exceptions import ObjectDoesNotExist
from django.core import urlresolvers

from wxmp import celery_call

logger = logging.getLogger(__name__)

from wxmp.apps.member.models import Member

class IndexView(TemplateView):
    template_name = 'apps/member/index.html'

    def get(self, request, *args, **kwargs):
        open_id = request.GET.get('open_id', None)
        if not open_id:
            #core_auth_url = request.build_absolute_uri(urlresolvers.reverse('core.auth.sns_base'))
            core_auth_url = urlresolvers.reverse('core.auth.sns_base') + '?next_url={0}'.format(request.path)
            logger.debug("Need web authorization, redirect to: {0}".format(core_auth_url))
            return HttpResponseRedirect(core_auth_url)

        context = self.get_context_data(**kwargs)
        try:
            member = Member.objects.get(open_id=open_id)
        except:
            member = None

        context['member'] = member
        context['open_id'] = open_id
        return self.render_to_response(context)

def myqrcode(request):
    ticket = request.GET.get('ticket', None)
    if not ticket:
        logger.debug("Failed to get ticket in myqrcode()")
        return HttpResponseBadRequest("No ticket")

    url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={0}".format(ticket)
    response = requests.get(url)
    return HttpResponse(response, content_type='image/jpg')

class TestView(TemplateView):
    template_name = 'apps/member/test.html'

    def get(self, request, *args, **kwargs):
        logger.debug("in test view")
        context = self.get_context_data(**kwargs)
        profile = {
            "openid":" OPENID",
            "nickname": 'nickname',
            "sex":"1",
            "province":"PROVINCE",
            "city":"CITY",
            "country":"COUNTRY",
            "headimgurl":"http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/46",
            "privilege":[ "PRIVILEGE1" "PRIVILEGE2"],
            "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
        }

        context['profile'] = request.build_absolute_uri(urlresolvers.reverse('core.auth.sns_userinfo'))

        return self.render_to_response(context)

class BaseView(TemplateView):
    """
    snsapi_base web authorization
    """
    template_name = 'apps/member/test.html'

    def get(self, request, *args, **kwargs):
        open_id = request.GET.get('open_id', None)
        if not open_id:
            core_auth_url = request.build_absolute_uri(urlresolvers.reverse('core.auth.sns_base'))
            core_auth_url += '?next_url={0}'.format(request.path)
            logger.debug("Need web authentication, redirect to: {0}".format(core_auth_url))
            return HttpResponseRedirect(core_auth_url)

        logger.debug("In BaseView, open_id is:{0}".format(open_id))

        context = self.get_context_data(**kwargs)
        context['open_id'] = open_id
        return self.render_to_response(context)

class UserInfoView(TemplateView):
    """
    snsapi_userinfo web authorization
    """
    template_name = 'apps/member/index.html'

    def get_user_info(self, open_id):
        user_info_dict = celery_call('api.web.get_user_info', (open_id,))
        if not user_info_dict:
            logger.debug("Fetched empty userinfo dict")
            return None

        class UserInfo:
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)

        return UserInfo(**user_info_dict)

    def get(self, request, *args, **kwargs):
        open_id = request.GET.get('open_id', None)
        if not open_id:
            core_auth_url = request.build_absolute_uri(urlresolvers.reverse('core.auth.userinfo'))
            core_auth_url += '?next_url={0}'.format(request.path)
            logger.debug("Need web authentication, redirect to: {0}".format(core_auth_url))
            return HttpResponseRedirect(core_auth_url)

        context = self.get_context_data(**kwargs)
        context['wx_profile'] = self.get_user_info(open_id)
        return self.render_to_response(context)