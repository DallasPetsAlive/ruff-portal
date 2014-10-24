from django.shortcuts import render
from django.http import HttpResponse
from rg_sync import RGSync


def index(request):
    sync_class = RGSync()
    return_str = sync_class.get_available_animals()
    return HttpResponse(return_str)
