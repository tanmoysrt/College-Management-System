from django.contrib.auth import login, authenticate, logout
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from teacher.decorators import teacher_required
from accounts.models import notesData, chatMessage,pyq
from college.settings import BASE_DIR
import os,json
from django.http import JsonResponse
from django.utils.timezone import now

def loginn(request):
    if request.user.is_authenticated and request.user.is_teacher :
        return redirect("/teacher/")
    else:
        if request.method == "POST":
            phoneno = request.POST.get("phoneno","-1")
            password = request.POST.get("password","-1")
            user = authenticate(phoneno=phoneno,password=password)
            if user is not None:
                login(request,user)
                return redirect("/teacher/")
        return render(request,'teacher/login.html')

@teacher_required
def logoutt(request):
    logout(request)
    return redirect("/teacher")

@teacher_required
def homepage(request):
    return render(request,"teacher/home.html")

@teacher_required
def uploadnote(request):
    data = {}
    if request.method == "POST" and request.FILES:
        title = request.POST.get("title",None)
        course = request.POST.get("course",None)
        file = request.FILES['note']
        fs = FileSystemStorage(location='media/notes/')
        finalfilename = ''.join(e for e in file.name if e.isalnum() or e== ".")
        filename = fs.save(finalfilename, file)
        finalfile = fs.generate_filename(filename)
        print(finalfile)
        notesData.objects.create(
            title=title,
            link=finalfile,
            course=course,
            teacherid=request.user.id,
            teachername=request.user.name
        )
        data["message"] = "File Uploaded Successfully"
    return render(request,"teacher/notesupload.html",data)

@teacher_required
def previousnotes(request):
    data = {
        "notes":notesData.objects.filter(teacherid=request.user.id)
    }
    noteid = request.GET.get("id","-1")
    if noteid != "-1":
        try:
            note = notesData.objects.get(id=noteid)
            if os.path.exists(os.path.join(os.path.join(os.path.join(BASE_DIR,"media"),"notes"),str(note.link))):
                os.remove(os.path.join(os.path.join(os.path.join(BASE_DIR,"media"),"notes"),str(note.link)))
            else:
                print("The file does not exist")
            note.delete()
            data["message"]='''
                    <div class="alert alert-danger" role="alert">
                    Note Deleted Successfully !
                    </div>
                    '''
        except:
            data["message"] = '''
                <div class="alert alert-warning" role="alert">
                Warning ! Some Error Occurred ! Contact Webadmin
                </div>
                '''
    return render(request,"teacher/notes.html",data)

@teacher_required
def listofmessage(request):
    data = {
        "chats":chatMessage.objects.filter(teacherid=request.user.id),
    }
    return render(request,"teacher/listofmessage.html",data)

@teacher_required
def chat(request,id):
    data = {
        "messagetoken" : id,
    }
    return render(request,"teacher/chat.html",data)

@teacher_required
def chatapi(request,id):
    messagedata = json.loads(chatMessage.objects.get(id=id).data)
    return JsonResponse(messagedata,safe=False)

@teacher_required
def sendchatteacher(request,id):
    message=request.GET.get("message","-1")
    selectedmessage =chatMessage.objects.get(id=id)
    messagedata = json.loads(selectedmessage.data)
    messagedata.append({
        "message":message,
        "sender" : "teacher",
    })
    selectedmessage.data = json.dumps(messagedata)
    selectedmessage.save()
    return HttpResponse(status="200")

@teacher_required
def pyqq(request):
    data={
        "pyqs":pyq.objects.all()
    }
    pyqid = request.GET.get("id","-1")
    if request.method == "POST" and request.FILES:
        title = request.POST.get("title",None)
        course = request.POST.get("course",None)
        file = request.FILES['note']
        fs = FileSystemStorage(location='media/pyq/')
        finalfilename = ''.join(e for e in file.name if e.isalnum() or e== ".")
        filename = fs.save(finalfilename, file)
        finalfile = fs.generate_filename(filename)
        pyq.objects.create(
            title=title,
            link=finalfile,
            course=course,
        )
        data["message"] ='''
        <div class="alert alert-success" role="alert">
                    PYQ Uploaded Successfully
        </div>'''
    else:
        if pyqid != "-1":
            try:
                pyqqq = pyq.objects.get(id=pyqid)
                if os.path.exists(os.path.join(os.path.join(os.path.join(BASE_DIR,"media"),"notes"),str(pyqqq.link))):
                    os.remove(os.path.join(os.path.join(os.path.join(BASE_DIR,"media"),"notes"),str(pyqqq.link)))
                else:
                    print("The file does not exist")
                pyqqq.delete()
                data["message"]='''
                        <div class="alert alert-danger" role="alert">
                        PYQ Deleted Successfully !
                        </div>
                        '''
            except:
                data["message"] = '''
                    <div class="alert alert-warning" role="alert">
                    Warning ! Some Error Occurred ! Contact Webadmin
                    </div>
                    '''
    return render(request,"teacher/pyq.html",data)