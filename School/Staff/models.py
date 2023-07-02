from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):
  user = models.OneToOneField(User , on_delete=models.CASCADE , null=True)
  student_id = models.IntegerField(unique=True)
  name = models.CharField(max_length=100)
  phone_no = models.CharField(max_length=20)
  dob = models.DateField()
  address = models.CharField(max_length=100)
  course = models.CharField(max_length=100 , default="BSC Hons")
  intake = models.CharField(max_length=100 , default= "Spring Intake")
  level = models.CharField(max_length=100 , default="Level 4")
  profile_pic = models.ImageField(upload_to='profile', null=True)
  
  def __str__(self):
    return self.name
  
class Profile(models.Model):
  student = models.OneToOneField(Student ,null=True, on_delete=models.CASCADE )
  token = models.CharField(max_length=200)
  is_verified = models.BooleanField(default=False)
  