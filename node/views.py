from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.conf import settings

import json

# Create your views here.


def hello(request):
    return HttpResponse(f"Hello! FrpMan! Made by woshishabii")


def node_server_info(request):
    content = {
        'info': {
            'version': settings.FRPMAN_VERSION,
            'build': settings.FRPMAN_BUILD,
            'name': settings.FRPMAN_NAME,
        },
        'node': {
            'version': settings.FRPMAN_NODE_VERSION,
            'update': settings.FRPMAN_UPDATE_REQUIRED,
        },
    }
    return JsonResponse(content)
