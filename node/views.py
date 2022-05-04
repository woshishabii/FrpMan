from django.shortcuts import render, HttpResponse

# Create your views here.


def hello(request):
    return HttpResponse(f"Hello! FrpMan! Made by woshishabii")
