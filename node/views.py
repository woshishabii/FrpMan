from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.conf import settings

from django.shortcuts import get_object_or_404

from . import models

# Create your views here.


def hello(request):
    return HttpResponse(f"Hello! FrpMan! Made by woshishabii")


def node_server_info(request):
    nodes = models.Node.objects.all()
    uuid_list = []
    for node in nodes:
        uuid_list.append(node.identifier)
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
        'node_list': uuid_list,
    }
    return JsonResponse(content)


def node_node_api(request, node_uuid, node_man_pwd):
    model = get_object_or_404(models.Node, identifier=node_uuid)
    if node_man_pwd == model.manage_password:
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
    else:
        content = {
            'error': 'Wrong Password',
        }
    return JsonResponse(content)
