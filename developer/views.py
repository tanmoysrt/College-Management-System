from django.http.response import HttpResponse
from django.shortcuts import render
from .decorators import developer_required
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@developer_required
def authfalse(request):
    return HttpResponse(status=200)

@csrf_exempt
@developer_required
def studentregister(request):
    pass

