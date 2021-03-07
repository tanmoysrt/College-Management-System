from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser, OTPData, studentProfile, questionPaper,notesData, noticeData, chatMessage, answerPaper, registrationLinkStudent

admin.site.unregister(Group)
admin.site.register(CustomUser)
admin.site.register(OTPData)
admin.site.register(studentProfile)
admin.site.register(questionPaper)
admin.site.register(answerPaper)
admin.site.register(registrationLinkStudent)
admin.site.register(notesData)
admin.site.register(noticeData)
admin.site.register(chatMessage)