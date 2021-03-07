from django.shortcuts import redirect
from django.contrib.auth import  logout
from functools import wraps


def teacher_required(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_teacher :
                return view_func(request, *args, **kwargs)
            else:
                logout(request)
                return redirect('/teacher/login/')
        else:
            logout(request)
            return redirect('/teacher/login/')
    return wrap
