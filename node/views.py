from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.conf import settings

from django.shortcuts import get_object_or_404

from . import models

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


def node_node_api(request, node_uuid):
    model = get_object_or_404(models.Node, identifier=node_uuid)
    content = {
        'basic': {
            'uuid': model.identifier,
            'prefix': model.prefix,
            'display_name': model.display_name,
            'domain_name': model.domain_name,
        },
        'frps': {
            'port_start': model.default_port_start,
            'port_end': model.default_port_end,
        },
        'detail': {
            'status': model.status,
            'announcement': model.announcement,
            'max_bandwidth': model.max_bandwidth,
            'price': model.price,
            'location': model.location,
        },
    }
    return JsonResponse(content)
