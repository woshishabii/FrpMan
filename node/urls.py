from django.urls import path

from . import views

app_name = 'node'
urlpatterns = [
    path('hello/', views.hello, name="hello"),
    path('server_info/', views.node_server_info, name="server_info"),
    path('node_api/<str:node_uuid>', views.node_node_api, name='node_api'),
]
