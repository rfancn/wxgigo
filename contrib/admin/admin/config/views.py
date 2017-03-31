from __future__ import absolute_import

import json
import logging

from django.http import HttpResponse
from django.views.generic import View, TemplateView

from contrib.admin import celery_call

logger = logging.getLogger(__name__)

class WXMPConfigActionView(View):
    def get(self, request):
        """
        Load action
        """
        config_dict = celery_call('api.config.load')
        if config_dict is None:
            raise Exception("Failed to load configuration data!")

        return HttpResponse(json.dumps(config_dict), content_type="application/json")

    def post(self, request):
        """
        Save action
        """
        recv = request.POST
        response = celery_call('api.config.save', (recv,))
        return HttpResponse(json.dumps(response), content_type="application/json")

class ConfigDetailView(TemplateView):
    template_name = "detail.html"

class ConfigUpdateView(TemplateView):
    template_name = "edit.html"




