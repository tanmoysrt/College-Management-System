from django.shortcuts import redirect, render
from django.contrib.auth import  logout
from functools import wraps


def student_required(view_func):
    @wraps(view_func)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_student :
                if request.user.verified_by_teacher:
                    return view_func(request, *args, **kwargs)
                else :
                    return render(request,"student/notverified.html")
            else:
                logout(request)
                return redirect('/student/login/')
        else:
            logout(request)
            return redirect('/student/login/')
    return wrap
