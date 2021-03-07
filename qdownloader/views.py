import os
import re
import mimetypes
from django.http import HttpResponse, Http404
from django.http.response import StreamingHttpResponse
from accounts.models import questionPaper,answerPaper,notesData
from college.settings import BASE_DIR, MEDIA_ROOT
from django.utils.timezone import  now
from django.shortcuts import render
from wsgiref.util import FileWrapper

def qdownload(request, id,key):
    try:
        file = questionPaper.objects.get(id=id)
        if file.key == key :
            if file.startdate <= now().date() and file.starttime <=now().time() :
                file_path = os.path.join(os.path.join(BASE_DIR,"secured_folder"), file.link)
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as fh:
                        response = HttpResponse(fh.read(), content_type="application/pdf")
                        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                        return response
                raise Http404
            else:
                return HttpResponse(f"Exam yet not started. Your exam will be started on {file.startdate} at {file.starttime}")
        else:
            return HttpResponse(status="401")
    except:
        return HttpResponse("Serious Problem ! Contact With Webadmin as soon as possible",status="500")

def adownload(request,id):
    try:
        file = answerPaper.objects.get(id=id).answerlink
        file_path = os.path.join(os.path.join(BASE_DIR, "answer_scripts_secured"), file)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
    except :
        return HttpResponse("Serious Problem ! Contact With Webadmin as soon as possible",status="500")

def videodownload(request,a):
    path=os.path.join(os.path.join(MEDIA_ROOT,"notes"), a)
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(path)
            return response
    raise Http404

def notesDownload(request,id):
    note = notesData.objects.get(id=id)
    if str(note.link).endswith(".pdf"):
        file_path = os.path.join(os.path.join(MEDIA_ROOT,"notes"), note.link)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
    elif str(note.link).endswith(".jpg") or str(note.link).endswith(".jpeg") or str(note.link).endswith(".JPG") or str(note.link).endswith(".JPEG"):
        file_path = os.path.join(os.path.join(MEDIA_ROOT,"notes"), note.link)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="image/jpeg")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
    elif str(note.link).endswith(".png") or str(note.link).endswith(".PNG") :
        file_path = os.path.join(os.path.join(MEDIA_ROOT,"notes"), note.link)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="image/png")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
    elif str(note.link).endswith(".mp4"):
        data = {
            "source" : '/download/stream/'+note.link,
            "type" : "video/mp4",
            "downloadlink" : "/download/video/"+note.link
        }
        return render(request,"qdownloader/player.html",data)
    elif str(note.link).endswith(".mkv"):
        print("mkv")
    return HttpResponse("OK")
