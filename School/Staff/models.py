from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Course(models.Model):
  course = models.CharField(max_length=100 , unique=True)
  
  def __str__(self):
    return self.course
  
class Level(models.Model):
  level = models.CharField(max_length=100)
  
  def __str__(self) -> str:
    return self.level
  
class Student(models.Model):
  user = models.OneToOneField(User , on_delete=models.CASCADE , null=True)
  course = models.ForeignKey(Course , on_delete=models.CASCADE)
  level = models.ForeignKey(Level, on_delete=models.CASCADE)
  student_id = models.IntegerField(unique=True)
  name = models.CharField(max_length=100)
  phone_no = models.CharField(max_length=20)
  dob = models.DateField()
  address = models.CharField(max_length=100)
  intake = models.CharField(max_length=100)
  profile_pic = models.ImageField(upload_to='profile_pic', null=True)
  
  def __str__(self):
    return self.name
  
class Profile(models.Model):
  student = models.OneToOneField(Student ,null=True, on_delete=models.CASCADE )
  token = models.CharField(max_length=200)
  is_verified = models.BooleanField(default=False)
  

class Subject(models.Model):
  course = models.ForeignKey(Course , on_delete=models.CASCADE)
  level = models.ForeignKey(Level , on_delete=models.CASCADE)
  sub_name = models.CharField(max_length=100)
  sub_code = models.CharField(max_length=100)
  
  
  
