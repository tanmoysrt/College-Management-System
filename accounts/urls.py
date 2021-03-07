from django.contrib import admin
from django.urls import path,include
from . import views
app_name = 'accounts'
urlpatterns = [
    path('student/<uuid:id>',views.registerlinkstudent),
]
