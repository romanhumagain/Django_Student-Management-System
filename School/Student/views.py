from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth import logout
from  Staff . models import *
# Create your views here.

def student_dashboard(request , uid ):
  students = Student.objects.filter(user = uid)
  
  if request.method ==  'POST':
    action = request.POST.get('action')
    if action == 'profile_pic':
      pic= request.FILES.get('profile_pic')
      for student in students:
        student. profile_pic = pic
        student.save()
      messages.success(request , 'Successfully Uploaded Profile Pic')
      return redirect(f'/student/student_dashboard/{uid}')
   
  context = {'student':students ,'uid':uid}
  return render(request , 'student dashboard.html' , context)

def sign_out(request):
  logout(request)
  return redirect('/')
  