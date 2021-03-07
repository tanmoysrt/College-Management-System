from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import  logout
from functools import wraps
from college.settings import DEVELOPER_KEY

def developer_required(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        if 'devkey' in request.headers:
            key = request.headers.get('devkey')
            if key == DEVELOPER_KEY :
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("Not Verified",status=401)
        else:
            return HttpResponse("<h1>😊😊 Don't Try To Hack ........ 😊😊</h1>",status=500)
        
    return wrap
