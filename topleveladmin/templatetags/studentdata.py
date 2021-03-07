from django import template
from accounts.models import CustomUser,studentProfile

register = template.Library()

@register.simple_tag
def define(val=None):
  return val

@register.filter
def student_data(data):
    user = CustomUser.objects.get(id=data)
    tmp = {
        "name" : user.name,
        "phoneno" : user.phoneno,
        "course" : user.student.course,
        "rollno" : user.student.rollno,
        "serialno" : user.student.serialno,
        "admissiondate" : user.student.admissiondate
    }
    return tmp