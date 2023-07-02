from django.shortcuts import render , redirect
from Staff.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . utils import *
import random

# Create your views here.
@login_required(login_url='/')
def staff_dashboard(request):
  
  return render(request, 'dashboard.html')

@login_required(login_url='/')
def student_registration(request):
  
  upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  lower_case = " abcdefghijklmnopqrstuvwxyz"
  digits = "123456789"
  
  String = upper_case+lower_case+digits
  length = 12
  password = "".join(random.sample(String,length))
  student_id = "".join(random.choices(digits , k = 4))
  
  if request.method == 'POST':
    data = request.POST
    
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    course = data.get('course')
    dob = data.get('dob')
    intake =data.get('intake')
    level = data.get('level')
    
    
    user = User.objects.create(username = email)
    user.set_password(password)
    user.save()
    
    student = Student.objects.create(
      user = user,
      student_id = student_id,
      name= name,
      phone_no = phone,
      dob = dob,
      address = address,
      course = course,
      intake = intake,
      level = level,
    )
    
    send_password(email , password , intake)
    messages.success(request , f'Successfully Registered {name}')
    return redirect('/staff/student_registration/')
  
  return render(request , 'registration.html')

def view_student(request):
  
  return render(request , 'view student.html')