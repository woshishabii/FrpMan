from django.urls import path

from . import views

app_name = 'node'
urlpatterns = [
    path('hello/', views.hello, name="hello"),
]
