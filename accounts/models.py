from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
import uuid
from .variables import COURSE_CHOICE

class CustomUser(AbstractUser):
    username = None
    first_name=None
    last_name=None
    id = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False) 
    email = models.EmailField(_('email address'))
    phoneno=models.BigIntegerField(_('phone no'),unique=True)
    name=models.CharField(max_length=50,default='No_NAME')
    is_topleveladmin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_stafff = models.BooleanField(default=False)
    verified_by_teacher = models.BooleanField(default=False)
    designation=models.TextField(default="-1",null=True)
    USERNAME_FIELD = 'phoneno'
    REQUIRED_FIELDS = ['email','name']
    objects = CustomUserManager()

    def __str__(self):
        return str(self.name)

class OTPData(models.Model):
    phoneno=models.BigIntegerField()
    otp=models.IntegerField()
    def __str__(self):
        return f"{self.phoneno} has sent otp : {self.otp}"

class studentProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="student")
    course = models.CharField(max_length=50,choices=COURSE_CHOICE,null=True)
    rollno = models.TextField(null=True)
    admissiondate=models.DateField(null=True,editable=True)
    serialno=models.TextField(null=True,unique=True)

    def __str__(self) :
        return str(self.user.name)

class questionPaper(models.Model):
    id = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False)
    key = models.TextField(null=True)
    title = models.TextField(null=True)
    link  = models.TextField(null=True)
    course = models.CharField(max_length=50,choices=COURSE_CHOICE,null=True)
    startdate = models.DateField(null=True)
    starttime = models.TimeField(null=True)
    enddate = models.DateField(null=True)
    endtime = models.TimeField(null=True)
    total_marks = models.BigIntegerField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class answerPaper(models.Model):
    id = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False) 
    studentid = models.UUIDField(null=True)
    questionid=models.UUIDField(null=True)
    answerlink = models.TextField(null=True)
    marks = models.BigIntegerField(null=True,default=0)
    evaluated = models.BooleanField(default=False)
    submitted_on=models.DateTimeField(auto_now_add=True)
    ipaddress=models.GenericIPAddressField(null=True)

    def __str__(self):
        return str(self.studentid)

class registrationLinkStudent(models.Model):
    id = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False)
    created_on=models.DateTimeField(auto_now_add=True)
    course = models.CharField(max_length=50,choices=COURSE_CHOICE,null=True)
    open = models.BooleanField(default=False)

    def __str__(self) :
        return str(self.course)

class notesData(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    course = models.CharField(max_length=50, choices=COURSE_CHOICE, null=True)
    title=models.TextField(null=True)
    link=models.TextField(default="")
    teachername=models.CharField(max_length=100,null=True)
    teacherid=models.UUIDField(null=True)
    created_on=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class noticeData(models.Model):
    title=models.TextField(null=True)
    data=models.TextField(null=True)
    created_on=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class chatMessage(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    teacherid = models.UUIDField(null=True)
    student = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="chat")
    data = models.TextField(default="[]",null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student.name

class pyq(models.Model):
    id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    course = models.CharField(max_length=50, choices=COURSE_CHOICE, null=True)
    title=models.TextField(null=True)
    link=models.TextField(default="")
    created_on=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
