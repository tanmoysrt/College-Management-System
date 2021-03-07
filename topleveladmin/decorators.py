from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from functools import wraps


def top_level_admin_required(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_topleveladmin :
                return view_func(request, *args, **kwargs)
            else:
                logout(request)
                return redirect('/adminn/login/')
        else:
            logout(request)
            return redirect('/adminn/login/')
    return wrap
