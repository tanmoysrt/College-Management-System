from django.conf.urls import url
from django.urls import path, include
from django.views.decorators.cache import never_cache

from . import views

urlpatterns = [
    path("login/", views.loginn),
    path("", views.dashboard, name="dashboard"),
    path("logout/", views.logoutt, name="logout"),
    path("studentdatas/", views.studentdatas, name="studentdatas"),
    path("teacherdatas/", views.teacherdatas, name="teacherdatas"),
    path("staffdatas/", views.staffdatas, name="staffdatas"),
    path("studentregister/", views.studentregister,name="studentregister"),
    path("teacherregister/",views.teacherregister,name="teacherregister"),
    path("staffregister/",views.staffregister,name="staffregister"),
    path("notes/",views.notes,name="notes"),
    path("examportal/",views.examportaldashboard,name="examportaldashboard"),
    path("studentedit/<uuid:id>",views.studentedit),
    path("teacheredit/<uuid:id>",views.teacheredit),
    path("staffedit/<uuid:id>",views.staffedit),
    path('noticeadd/',views.add_notice,name="noticepublish"),
    path('notice/',views.notice,name="notice"),
    path("examportal/upcomingexams/",views.examportalupcomingexams,name="examportalupcomingexams"),
    path("examportal/addexam/",views.examportaladdnewexams,name="examportaladdnewexams"),
    path("examportal/oldexam/",views.examportaloldexams,name="examportaloldexams"),
    path("examportal/answerscripts/<uuid:id>",views.examportalanswerscripts,name="examportalanswerscripts"),
    path("examportal/data/<uuid:id>",views.examportalanswerscriptsstudentdata),
    path("registrationlinks/",views.studentregistrationlinks,name="studentregistrationlinks"),
    path('pyq/',views.pyqq,name="toplevelpyq")
]
