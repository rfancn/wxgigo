import logging


from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse

from controller import WXMPController

logger = logging.getLogger(__name__)

@csrf_exempt
def main(request):
    """
    Http Request -> Celery Server -> Response

    :param request: django.http.HttpRequest
    :return:        string
    """
    controller = WXMPController(request)
    response = controller.dispatch()

    return HttpResponse(response)


