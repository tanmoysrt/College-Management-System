from college.settings import BASE_DIR
import os
from django.contrib.auth import authenticate, login, logout
from django.http import request
from django.shortcuts import redirect, render
from accounts.models import CustomUser, studentProfile, questionPaper, answerPaper, registrationLinkStudent, \
    notesData, noticeData,pyq
from .decorators import top_level_admin_required
from django.core.files.storage import FileSystemStorage
import  secrets
from django.utils.timezone import now
from django.http import JsonResponse

def loginn(request):
    if request.user.is_authenticated and request.user.is_topleveladmin:
        return redirect("/adminn")
    else:
        if request.method == "POST":
            username = request.POST.get("username", "-1")
            password = request.POST.get("password", "-1")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print(user.name)
                login(request, user)
                return redirect("/adminn")
        return render(request, "topleveladmin/login.html")


@top_level_admin_required
def logoutt(request):
    logout(request)
    return redirect("/adminn")


@top_level_admin_required
def studentdatas(request):
    data = {
        "students": CustomUser.objects.filter(is_student=True)
    }
    ids = request.GET.get("id", "-1")
    action = request.GET.get("action","-1")
    if ids != "-1":
        try:
            if int(action) == 1:
                user = CustomUser.objects.get(id=ids)
                user.delete()
                data['message'] = '''
                <div class="alert alert-danger" role="alert">
                User Deleted Successfully !
                </div>
                '''
            elif int(action) == 2 :
                user = CustomUser.objects.get(id=ids)
                user.verified_by_teacher = True
                user.save()
                data['message'] = '''
                <div class="alert alert-success" role="alert">
                User Approved Successfully !
                </div>
                '''
        except:
            data['message'] = '''
            <div class="alert alert-warning" role="alert">
            Error Occurred ! Contact Webadmin
            </div>
            '''
    return render(request, "topleveladmin/studentdatas.html", data)


@top_level_admin_required
def teacherdatas(request):
    data = {
        "teachers": CustomUser.objects.filter(is_teacher=True)
    }
    ids = request.GET.get("id", "-1")
    if ids != "-1":
        try:
            user = CustomUser.objects.get(id=ids)
            user.delete()
            data['message'] = '''
                <div class="alert alert-danger" role="alert">
                User Deleted Successfully !
                </div>
                '''
        except:
            data['message'] = '''
                <div class="alert alert-warning" role="alert">
                Error Occurred ! Contact Webadmin
                </div>
                '''
    return render(request, "topleveladmin/teacherdatas.html", data)


@top_level_admin_required
def staffdatas(request):
    data = {
        "staffs": CustomUser.objects.filter(is_stafff=True)
    }
    ids = request.GET.get("id", "-1")
    if ids != "-1":
        try:
            user = CustomUser.objects.get(id=ids)
            user.delete()
            data['message'] = '''
                   <div class="alert alert-danger" role="alert">
                   User Deleted Successfully !
                   </div>
                   '''
        except:
            data['message'] = '''
                   <div class="alert alert-warning" role="alert">
                   Error Occurred ! Contact Webadmin
                   </div>
                   '''
    return render(request, "topleveladmin/staffsdatas.html", data)


@top_level_admin_required
def studentregister(request):
    if request.method == "POST":
        name = request.POST.get("name", "NAME_ERROR")
        email = request.POST.get("email", "EMAIL_NOT_ENTERED")
        phoneno = request.POST.get("phoneno", "PHONENO_ERROR")
        coursename = request.POST.get("corsename", "COURSENAME_ERROR")
        rollno = request.POST.get("rollno", "ROLL_NO_ERROR")
        admissiondate = request.POST.get("admissiondate", "ADMISSION_DATE_ERROR")
        serialno = request.POST.get("serialno", "SERIAL_NO_ERROR")
        if len(CustomUser.objects.filter(phoneno=phoneno)) != 0:
            message = f'''
            <div class="alert alert-danger" role="alert">
            User With This Phone Number {phoneno} Already Exsists
            </div>
            '''
            return render(request, "topleveladmin/studentregister.html", {"message": message})
        elif len(studentProfile.objects.filter(serialno=serialno)) != 0:
            message = f'''
            <div class="alert alert-danger" role="alert">
            User With This Admission Serial No  {serialno} Already Exsists
            </div>
            '''
            return render(request, "topleveladmin/studentregister.html", {"message": message})
        else:
            user = CustomUser.objects.create_user(
                name=name,
                phoneno=phoneno,
                email=email,
                password=serialno
            )
            user.set_password(serialno)
            user.is_student = True
            user.verified_by_teacher = True
            user.save()
            studentProfile.objects.create(
                user=user,
                course=coursename,
                rollno=rollno,
                admissiondate=admissiondate,
                serialno=serialno,
            )
            message = f'''
                <div class="alert alert-success" role="alert">
                User With This Phone Number {phoneno} Created Successfully
                </div>
                '''
            return render(request, "topleveladmin/studentregister.html", {"message": message})
    return render(request, "topleveladmin/studentregister.html")


@top_level_admin_required
def teacherregister(request):
    if request.method == "POST":
        name = request.POST.get("name", "NAME_ERROR")
        email = request.POST.get("email", "EMAIL_NOT_ENTERED")
        phoneno = request.POST.get("phoneno", "PHONENO_ERROR")
        designation = request.POST.get("designation", "DESIGNATION_ERROR")
        if len(CustomUser.objects.filter(phoneno=phoneno)) != 0:
            message = f'''
            <div class="alert alert-danger" role="alert">
            User With This Phone Number {phoneno} Already Exsists
            </div>
            '''
            return render(request, "topleveladmin/teacherregister.html", {"message": message})
        else:
            user = CustomUser.objects.create_user(
                name=name,
                phoneno=phoneno,
                email=email,
                designation=designation,
                password=phoneno
            )
            user.set_password(phoneno)
            user.is_teacher = True
            user.verified_by_teacher = True
            user.save()
            message = f'''
            <div class="alert alert-success" role="alert">
            User With This Phone Number {phoneno} Account Created Successfully
            </div>
            '''
            return render(request, "topleveladmin/teacherregister.html", {"message": message})

    return render(request, "topleveladmin/teacherregister.html")


@top_level_admin_required
def staffregister(request):
    if request.method == "POST":
        name = request.POST.get("name", "NAME_ERROR")
        email = request.POST.get("email", "EMAIL_NOT_ENTERED")
        phoneno = request.POST.get("phoneno", "PHONENO_ERROR")
        designation = request.POST.get("designation", "DESIGNATION_ERROR")
        if len(CustomUser.objects.filter(phoneno=phoneno)) != 0:
            message = f'''
            <div class="alert alert-danger" role="alert">
            User With This Phone Number {phoneno} Already Exsists
            </div>
            '''
            return render(request, "topleveladmin/staffregister.html", {"message": message})
        else:
            user = CustomUser.objects.create_user(
                name=name,
                phoneno=phoneno,
                email=email,
                designation=designation,
                password=phoneno
            )
            user.set_password(phoneno)
            user.is_stafff = True
            user.verified_by_teacher = True
            user.save()
            message = f'''
            <div class="alert alert-success" role="alert">
            User With This Phone Number {phoneno} Account Created Successfully
            </div>
            '''
            return render(request, "topleveladmin/staffregister.html", {"message": message})
    return render(request, "topleveladmin/staffregister.html")


@top_level_admin_required
def studentedit(request, id):
    data = {}
    try:
        user = CustomUser.objects.get(id=id)
        data['user'] = user
        if request.method == "POST":
            name = request.POST.get("name", "NAME_ERROR")
            email = request.POST.get("email", "EMAIL_NOT_ENTERED")
            phoneno = request.POST.get("phoneno", "PHONENO_ERROR")
            coursename = request.POST.get("corsename", "COURSENAME_ERROR")
            rollno = request.POST.get("rollno", "ROLL_NO_ERROR")
            admissiondate = request.POST.get("admissiondate", "ADMISSION_DATE_ERROR")
            serialno = request.POST.get("serialno", "SERIAL_NO_ERROR")
            print(admissiondate)
            user.name = name
            user.email = email
            user.phoneno = phoneno
            user.student.course = coursename
            user.student.rollno = rollno
            user.student.admissiondate = admissiondate
            user.student.serialno = serialno
            user.save()
            user.student.save()
            data['message'] = f'''
            <div class="alert alert-success" role="alert">
            Student Details Updated Successfully .
            </div>
            '''
    except:
        data['message'] = f'''
        <div class="alert alert-warninif=g" role="alert">
        Warning ! Some Error Occurred ! Contact Webadmin
        </div>
        '''
    return render(request, "topleveladmin/studentedit.html", data)


@top_level_admin_required
def teacheredit(request, id):
    data = {}
    try:
        user = CustomUser.objects.get(id=id)
        data['user'] = user
        if request.method == "POST":
            name = request.POST.get("name", "NAME_ERROR")
            email = request.POST.get("email", "EMAIL_NOT_ENTERED")
            phoneno = request.POST.get("phoneno", "PHONENO_ERROR")
            designation = request.POST.get("designation", "DESIGNATION_ERROR")
            user.name = name
            user.email = email
            user.phoneno = phoneno
            user.designation = designation
            user.save()
            data['message'] = f'''
                <div class="alert alert-success" role="alert">
                Student Details Updated Successfully .
                </div>
                '''
    except:
        data['message'] = f'''
            <div class="alert alert-warninif=g" role="alert">
            Warning ! Some Error Occurred ! Contact Webadmin
            </div>
            '''
    return render(request, "topleveladmin/teacheredit.html", data)


@top_level_admin_required
def staffedit(request, id):
    data = {}
    try:
        user = CustomUser.objects.get(id=id)
        data['user'] = user
        if request.method == "POST":
            name = request.POST.get("name", "NAME_ERROR")
            email = request.POST.get("email", "EMAIL_NOT_ENTERED")
            phoneno = request.POST.get("phoneno", "PHONENO_ERROR")
            designation = request.POST.get("designation", "DESIGNATION_ERROR")
            user.name = name
            user.email = email
            user.phoneno = phoneno
            user.designation = designation
            user.save()
            data['message'] = f'''
                    <div class="alert alert-success" role="alert">
                    Student Details Updated Successfully .
                    </div>
                    '''
    except:
        data['message'] = f'''
                <div class="alert alert-warning" role="alert">
                Warning ! Some Error Occurred ! Contact Webadmin
                </div>
                '''
    return render(request, "topleveladmin/staffedit.html", data)


@top_level_admin_required
def notes(request):
    data={
        "notes":notesData.objects.all()
    }
    return render(request, "topleveladmin/notes.html",data)

@top_level_admin_required
def add_notice(request):
    if request.method == "POST" and request.FILES:
        title = request.POST.get("title")
        noticefile = request.FILES['data']
        fs = FileSystemStorage(location='media/notice/')
        filename = fs.save(noticefile.name, noticefile)
        noticefilename = fs.generate_filename(filename)
        noticeData.objects.create(
            title=title,
            data='notice/'+noticefilename
        )
        message = '''
                <div class="alert alert-success" role="alert">
                Notice Published Sucessfully !
                </div>
                '''
        return render(request, "topleveladmin/noticeadd.html",{"message":message})
    return render(request,"topleveladmin/noticeadd.html")

@top_level_admin_required
def notice(request):
    data={
        "notices":noticeData.objects.all().order_by("-id")
    }
    ids = request.GET.get("id", "-1")
    if ids != "-1":
        try:
            user = noticeData.objects.get(id=ids)
            user.delete()
            data['message'] = '''
                    <div class="alert alert-danger" role="alert">
                    Notice Deleted Successfully !
                    </div>
                    '''
        except:
            data['message'] = '''
                    <div class="alert alert-warning" role="alert">
                    Error Occurred ! Contact Webadmin
                    </div>
                    '''
    return render(request, "topleveladmin/noticelist.html",data)


@top_level_admin_required
def examportaladdnewexams(request):
    if request.method == "POST" and request.FILES:
        title=request.POST.get("title")
        startdate=request.POST.get("startdate")
        starttime=request.POST.get("starttime")
        enddate=request.POST.get("enddate")
        endtime=request.POST.get("endtime")
        totalmarks=request.POST.get("totalmarks")
        coursename=request.POST.get("coursename")
        filepdf=request.FILES["filepdf"]
        if filepdf.name.endswith(".pdf"):
            fs = FileSystemStorage(location='secured_folder/')
            filename = fs.save(filepdf.name, filepdf)
            questionfile = fs.generate_filename(filename)
            questionPaper.objects.create(
                title=title,
                startdate=startdate,
                starttime=starttime,
                enddate=enddate,
                endtime=endtime,
                total_marks=totalmarks,
                link=questionfile,
                course=coursename,
                key=secrets.token_hex(30)
            )
            message = '''
                    <div class="alert alert-success" role="alert">
                           Exam Scheduled Successfully !
                    </div>
                            '''
        else:
            message = '''
                    <div class="alert alert-danger" role="alert">
                           Cancelled ! You must upload questionpaper in pdf format.
                    </div>
                    '''
        return render(request, "topleveladmin/examportaladdnewexams.html",{"message":message})
    return render(request,"topleveladmin/examportaladdnewexams.html")

@top_level_admin_required
def examportalupcomingexams(request):
    data = {
        "upcomingexams":questionPaper.objects.filter(enddate__gte=now().date())
    }
    ids = request.GET.get("id", "-1")
    if ids != "-1":
        try:
            questionpaper = questionPaper.objects.get(id=ids)
            questionpaper.delete()
            data['message'] = '''
                        <div class="alert alert-danger" role="alert">
                        Question Paper Deleted Successfully !
                        </div>
                        '''
        except:
            data['message'] = '''
                        <div class="alert alert-warning" role="alert">
                        Error Occurred ! Contact Webadmin
                        </div>
                        '''
    return render(request,"topleveladmin/examportalupcomingexams.html",data)


@top_level_admin_required
def dashboard(request):
    return render(request, "topleveladmin/dashbaord.html")


@top_level_admin_required
def examportaldashboard(request):
    return render(request, "topleveladmin/examportaldashboard.html")


@top_level_admin_required
def examportaloldexams(request):
    data = {
        "oldexams":questionPaper.objects.filter(enddate__lt=now().date())
    }
    return render(request,"topleveladmin/examportaloldexams.html",data)


@top_level_admin_required
def examportalanswerscripts(request,id):
    data={
        "link" : "http://127.0.0.1:8000/",
        "questionpaper":questionPaper.objects.get(id=id),
        "answerscripts":answerPaper.objects.filter(questionid=id)
    }
    if request.method == "POST":
        try:
            answerid=request.POST.get("answerid","-1")
            marks=request.POST.get("marks")
            answerscript = answerPaper.objects.get(id=answerid)
            answerscript.marks=marks
            answerscript.evaluated=True
            answerscript.save()
            data['message'] = '''
            <div class="alert alert-success" role="alert">
            Marks Updated Successfully 
            </div>
            '''
        except:
            data['message'] = '''
            <div class="alert alert-danger" role="alert">
            !!! ERROR !!!Marks Not Updated Successfully 
            </div>
            '''
    return render(request,"topleveladmin/examportalanswerscripts.html",data)


@top_level_admin_required
def examportalanswerscriptsstudentdata(request,id):
    answerscript = answerPaper.objects.get(id=id)
    studentdata = CustomUser.objects.get(id=answerscript.studentid)
    data = {
        "name" : studentdata.name,
        "marks" : answerscript.marks,
        "answerid" : str(answerscript.id),
        "totalmarks"  : questionPaper.objects.get(id=answerscript.questionid).total_marks
    }
    return JsonResponse(data,safe=False)

@top_level_admin_required
def studentregistrationlinks(request):
    data = {
        "prefix" : "http://127.0.0.1:8000/account/student/",
        "tokens" : registrationLinkStudent.objects.all()
    }
    return render(request,"topleveladmin/studentregistrationlinks.html",data)


@top_level_admin_required
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
    return render(request,"topleveladmin/pyq.html",data)