from typing import Any, MutableMapping, Optional, Tuple
from django.db import models
from django.db.models.query import QuerySet

class StudentManager(models.Manager):
  def get_queryset(self) -> QuerySet:
    return super().get_queryset().filter(is_deleted = False)

# Create your models here.
class DumyDepartment(models.Model):
  department = models.CharField(max_length=200)
  
  def __str__(self) -> str:
    return self.department

class DumyStudent(models.Model):
  department = models.ForeignKey(DumyDepartment, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  address = models.CharField(max_length=100)
  email = models.EmailField()
  age = models.IntegerField()
  is_deleted = models.BooleanField(default=False)
  
  objects = StudentManager()
  admin_objects = models.Manager()
  
  def __str__(self) -> str:
    return self.name
  