from datetime import timezone
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from . utils import generate_slugs
# Create your models here.

class UserType(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  user_type = models.CharField(max_length=100, default='student')

class Course(models.Model):
  course = models.CharField(max_length=100 , unique=True)
  
  def __str__(self):
    return self.course
  
class Level(models.Model):
  level = models.CharField(max_length=100 ,unique=True )
  
  def __str__(self) -> str:
    return self.level
  
class Student(models.Model):
  user = models.OneToOneField(User , on_delete=models.CASCADE , null=True)
  course = models.ForeignKey(Course , on_delete=models.CASCADE)
  level = models.ForeignKey(Level, default=None, on_delete=models.CASCADE)
  # slug = models.SlugField(unique=True , null=True , default=None)
  student_id = models.IntegerField(unique=True)
  name = models.CharField(max_length=100)
  phone_no = models.CharField(max_length=20)
  dob = models.DateField()
  address = models.CharField(max_length=100)
  intake = models.CharField(max_length=100)
  profile_pic = models.ImageField(upload_to='profile_pic', null=True)
  
  # def save(self ,*args , **kwargs):
  #   self.slug = generate_slugs(self.name)
  #   super(Student , self).save(*args , **kwargs)
  
  def __str__(self):
    return self.name
  
class Profile(models.Model):
  user = models.OneToOneField(User, null=True, on_delete=models.CASCADE )
  token = models.CharField(max_length=200 , unique=True)
  is_verified = models.BooleanField(default=False)
  
class Notice(models.Model):
  notice = models.TextField(max_length=500)
  
  def __str__(self) -> str:
    return self.notice
  
class Assignment(models.Model):
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  level = models.ForeignKey(Level, on_delete=models.CASCADE)
  assignment = models.TextField(max_length=500)
  due_date = models.DateField(default=timezone.now)
  due_time = models.TimeField(default=timezone.now)
  
  def __str__(self) -> str:
    return self.assignment
  
class Attendance(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  date = models.DateField(auto_now=True)
  attendance = models.CharField(max_length=100)

class Subject(models.Model):
  course = models.ForeignKey(Course , on_delete=models.CASCADE)
  level = models.ForeignKey(Level , on_delete=models.CASCADE)
  sub_name = models.CharField(max_length=100)
  sub_code = models.CharField(max_length=100)
  
  def __str__(self) -> str:
    return self.sub_name
  
class Examination(models.Model):
  exam = models.CharField(max_length=200)
  date = models.CharField(max_length=200, null= True , default=None)
  
  def __str__(self) -> str:
    return self.exam
  
class SubjectMarks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam = models.ForeignKey(Examination, null=True, on_delete=models.CASCADE)
    marks = models.IntegerField()

    class Meta:
        unique_together = ['student', 'subject', 'exam']

class TotalMark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default=None, null=True)
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE, default=None, null=True)
    total_mark = models.IntegerField(null=True, default=0)
    rank = models.IntegerField(null=True, default=0)

    class Meta:
        unique_together = ['student', 'exam']

  
  
   
  
  
