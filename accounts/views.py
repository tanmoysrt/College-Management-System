from django.contrib.auth import login
from django.http import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import registrationLinkStudent,CustomUser,studentProfile

def registerlinkstudent(request,id):
    if request.method == "POST":
        name=request.POST.get("name","-1")
        phone=request.POST.get("phone","-1")
        emailid=request.POST.get("emailid","-1")
        rollno=request.POST.get("rollno","-1")
        admissiondate=request.POST.get("admissiondate","-1")
        serialno=request.POST.get("serialno","-1")
        password=request.POST.get("password","-1")
        user=CustomUser.objects.create(
            name=name,
            phoneno=phone,
            email=emailid,
            password=password,
            is_student=True,
            verified_by_teacher=registrationLinkStudent.objects.get(id=id).open
        )
        user.set_password(password)
        user.save()
        studentProfile.objects.create(
            user=user,
            course=registrationLinkStudent.objects.get(id=id).course,
            rollno=rollno,
            admissiondate=admissiondate,
            serialno=serialno
        )
        login(request,user)
        return redirect('/student/')
    return render(request,"accounts/studentlinkregister.html")

def handler404(request,exception =None):
    return render(request,"accounts/404.html",status=404)

def handler500(request,exception =None):
    return render(request,"accounts/500.html",status=500)