from django.urls import path
from . import  views

urlpatterns = [
    path('login/',views.loginn,name="studentlogin"),
    path('logout/',views.logoutt,name="studentlogout"),
    path('',views.homepage,name="studenthomepage"),
    path('upcomingexam/<uuid:id>',views.upcomingexam,name="studentupcomingexams"),
    path('list/',views.chatlist,name="studentlist"),
    path('chat/<uuid:id>',views.chat),
    path('chatapi/<uuid:id>',views.chatapi),
    path('sendchat/<uuid:id>/',views.sendchatstudent),
    path("notes/",views.notes,name="studentnotes"),
    path('upcomingexamslist/',views.upcomingexamslist,name="studentupcomingexamslist"),
    path('pyq/',views.pyqq,name="studentpyq"),
    path('notverified/',views.notverified,name="notverified")
]