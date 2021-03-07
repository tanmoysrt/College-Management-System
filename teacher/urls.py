from django.urls import path
from . import  views
urlpatterns = [
    path('login/',views.loginn,name="teacherlogin"),
    path('logout/',views.logoutt,name="teacherlogout"),
    path('', views.homepage,name="teacherhome"),
    path('notes/',views.previousnotes,name="teacherpreviousnotes"),
    path('uploadnotes/',views.uploadnote,name="teacheruploadnotes"),
    path('chatlist/',views.listofmessage,name="chatlist"),
    path('chat/<uuid:id>/',views.chat,name="chat"),
    path('chatapi/<uuid:id>/',views.chatapi),
    path('sendchat/<uuid:id>/',views.sendchatteacher),
    path('pyq/',views.pyqq,name="teaherpyq")
]