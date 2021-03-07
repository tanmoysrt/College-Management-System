from django.urls import path
from . import views
from qdownloader.videostream import stream_video
urlpatterns = [
    path("questionpaper/<id>/<key>",views.qdownload),
    path("answerscript/<id>",views.adownload),
    path("note/<uuid:id>",views.notesDownload),
    path("stream/<a>", stream_video),
    path("video/<a>",views.videodownload)
]
