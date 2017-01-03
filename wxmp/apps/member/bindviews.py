#!/usr/bin/env python
# coding=utf-8
"""
 Copyright (C) 2010-2013, Ryan Fan <ryan.fan@oracle.com>

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Library General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
"""
from __future__ import absolute_import

from django.http.response import HttpResponseRedirect
from django.views.generic import FormView
from django.core import urlresolvers
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from wxmp.apps.member.forms import BindForm
from wxmp.apps.member.models import Member

from wxmp import celery_call

import logging
logger = logging.getLogger(__name__)

class BindView(FormView):
    form_class = BindForm
    template_name = 'apps/member/bind.html'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        open_id = request.GET.get('open_id', None)
        # if this the first time enter into bind process, try to get open_id
        if not open_id:
            core_auth_url = urlresolvers.reverse('core.auth.sns_base') + '?next_url={0}'.format(request.path)
            logger.debug("Need web authorization, redirect to: {0}".format(core_auth_url))
            return HttpResponseRedirect(core_auth_url)

        try:
            Member.objects.get(open_id=open_id)
        except ObjectDoesNotExist:
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            context = self.get_context_data(form=form)
            context['open_id'] = open_id
            return self.render_to_response(context)

        return HttpResponseRedirect(urlresolvers.reverse('apps.member.bind-already'))

    def get_success_url(self):
        return urlresolvers.reverse('apps.member.bind-success')

    def bind_user(self, open_id, telephone):
        # try to get system user if such user exist in our system
        try:
            user = User.objects.get(username=telephone)
        except ObjectDoesNotExist:
            user = None

        user_info_dict = celery_call('api.webauth.get_user_info', (open_id,))
        if not user_info_dict:
            logger.error("Failed to get weixin user basic info in bind_user()")
            return False

        try:
            member = Member(open_id=open_id,
                            telephone=telephone,
                            nickname=user_info_dict['nickname'],
                            headimg_url=user_info_dict['headimgurl'],
                            sex=user_info_dict['sex'])
            # add ticket
            ticket = celery_call('api.qrcode.get_limit_str_ticket', (open_id,))
            if not ticket:
                logger.error("Failed to get QRcode ticket")
                return False

            member.ticket = ticket
            member.save()
        except Exception, e:
            logger.error("Failed to create member and save it because of: {0})".format(e))
            return False

        return True

    def form_valid(self, form):
        open_id = form.data['open_id']
        telephone = form.cleaned_data['telephone']
        if not self.bind_user(open_id, telephone):
            return HttpResponseRedirect(urlresolvers.reverse('apps.member.bind-error'))

        return super(BindView, self).form_valid(form)
