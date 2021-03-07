import json

from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.http import request
from django.shortcuts import render, redirect
from student.decorators import student_required
from accounts.models import pyq, questionPaper,answerPaper,notesData,chatMessage,CustomUser
from django.utils.timezone import now
import random

def loginn(request):
    if request.user.is_authenticated and request.user.is_student :
        return redirect("/student/")
    else:
        if request.method == "POST":
            phoneno = request.POST.get("phoneno","-1")
            password = request.POST.get("password","-1")
            user = authenticate(phoneno=phoneno,password=password)
            if user is not None:
                login(request,user)
                return redirect("/student/")
        return render(request,'student/login.html')

def logoutt(request):
    logout(request)
    return redirect("/student")

@student_required
def upcomingexam(request,id):
    selectedexam = questionPaper.objects.get(id=id)
    # After the preferred date and time started will be true
    # If the user does not upload answer paper yet or exam has not ended canupload will be true
    data = {
        "id" : str(selectedexam.id),
        "name" : selectedexam.title,
        "startdate" : selectedexam.startdate,
        "starttime" :selectedexam.starttime,
        "enddate" : selectedexam.enddate,
        "endtime" : selectedexam.endtime,
        "link" : "http://127.0.0.1:8000/download/questionpaper/"+str(selectedexam.id)+"/"+selectedexam.key,
        "canupload" : True,
        "started" : True
    }
    if request.FILES:
        print("trigger")
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        answerpaper = request.FILES['answerpaper']
        fs = FileSystemStorage(location='answer_scripts_secured/')
        filename = fs.save(answerpaper.name, answerpaper)
        finalfile = fs.generate_filename(filename)
        answerPaper.objects.create(
            questionid=id,
            answerlink=finalfile,
            studentid=request.user.id,
            ipaddress=ip
        )
    return render(request,"student/upcomingexamdetails.html",data)

@student_required
def homepage(request):
    data ={}
    return render(request,"student/home.html",data)

@student_required
def chatlist(request):
    data = {
        "chats" : CustomUser.objects.filter(is_teacher=True)
    }
    return render(request,"student/chatlist.html",data)

@student_required
def chat(request,id):
    try:
        selectedchat = chatMessage.objects.filter(student_id=request.user.id).filter(teacherid=id)[0]
    except:
        chatMessage.objects.create(
            teacherid=id,
            student_id=request.user.id
        )
    selectedchat = chatMessage.objects.filter(student_id=request.user.id).filter(teacherid=id)[0]

    return render(request,"student/chat.html",{"messagetoken":selectedchat.id})

@student_required
def chatapi(request,id):
    messagedata = json.loads(chatMessage.objects.get(id=id).data)
    return JsonResponse(messagedata,safe=False)

@student_required
def sendchatstudent(request,id):
    message=request.GET.get("message","-1")
    selectedmessage =chatMessage.objects.get(id=id)
    messagedata = json.loads(selectedmessage.data)
    messagedata.append({
        "message":message,
        "sender" : "student",
    })
    selectedmessage.data = json.dumps(messagedata)
    selectedmessage.save()
    return HttpResponse(status="200")

@student_required
def notes(request):
    data={
        "notes":notesData.objects.filter(course=request.user.student.course)
    }
    return render(request,"student/notes.html",data)

@student_required
def upcomingexamslist(request):
    data = {
        "upcomingexams" : questionPaper.objects.filter(course=request.user.student.course)
    }
    return render(request,"student/upomingexamlist.html",data)

@student_required
def pyqq(request):
    data={
        "pyqs":pyq.objects.filter(course=request.user.student.course)
    }
    return render(request,"student/pyq.html",data)

def notverified(request):
    return render(request,"student/notverified.html")