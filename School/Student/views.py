from django.shortcuts import render , redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash

from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from  Staff . models import *
from .utils import *
from django.db.models import Sum

from datetime import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.
import uuid

@login_required(login_url='/')
def student_dashboard(request , uid ):
  student = Student.objects.get(user = uid)
  
  user = User.objects.get(id = uid)
  profile = Profile.objects.get(user = user)
  
  is_verified = profile.is_verified
  notice = Notice.objects.all()
  notice_count = notice.count()
  
  level_id = student.level.id
  course_id = student.course.id
  
  assignment = Assignment.objects.filter(course = course_id , level = level_id)
  
  ass_count = assignment.count()
  
  current_time = datetime.now().time()
  greeting = ""
  if current_time.hour < 12:
        greeting = "Good Morning"
  elif 12 <= current_time.hour < 18:
        greeting = "Good Afternoon"
  else:
        greeting = "Good Evening"
  
  context = {'student':student ,'uid':uid , 'notices':notice, 'notice_count':notice_count , 'assignments':assignment , 'ass_count':ass_count , 'greeting':greeting}
  
  
  if not is_verified:
    context['verification_error'] = 'please verify your account'
  
  if request.method ==  'POST':
    action = request.POST.get('action')
    if action == 'profile_pic':
      pic= request.FILES.get('profile_pic')
      student.profile_pic = pic
      student.save()
      messages.success(request , 'Successfully Uploaded Profile Pic')
      return redirect(f'/student/student_dashboard/{uid}')
    
    if action == 'change_password':
       password = request.POST.get('password')
       
       user = User.objects.get(id = uid)
       user.set_password(password)
       user.save()
       
       update_session_auth_hash(request, user)
       
       messages.success(request , 'successfully changed password, Re-login your account ')
       return redirect('/')
       
    if action == 'verify':
      user = User.objects.get(id = uid)
      email = user.username
      
      profile = Profile.objects.get(user = user)
      verification_token = profile.token
       
      send_verification(email , verification_token)
      messages.success(request , 'successfully sent verification link' )
      return redirect(f'/student/student_dashboard/{uid}')
    
  return render(request , 'student dashboard.html' , context)

def sign_out(request):
  logout(request)
  return redirect('/')

def verify_account(request , token):
  try:
    profile = Profile.objects.get(token = token)
    profile.is_verified = True
    profile.save()
    return HttpResponse('Congratulation! Successfully Verified Your Account')
  
  except Exception as e:
    return HttpResponse('Sorry Couldnt Verify Your Account')
    print(str(e))
    
def gradesheet(request, id):
    try:
        user = User.objects.get(id=id)
        student = Student.objects.get(user=user)
        exams = Examination.objects.all().order_by('-id') 
        course = student.course
        level = student.level

        subjectMarks = SubjectMarks.objects.filter(student=student)
        sub_count = Subject.objects.filter(course__course=course, level__level=level).count()

        total_full_marks = sub_count * 100

        try:
            total_marks = subjectMarks.aggregate(total_marks=Sum('marks'))['total_marks']
            total_marks = total_marks or 0  # Ensure it's not None
            percentage = (total_marks / total_full_marks) * 100
        except (TypeError, KeyError):
            return HttpResponse('Result Not Published Yet !!')

        try:
            totalMarkObj = TotalMark.objects.get(student=student)
            rank = totalMarkObj.rank
        except TotalMark.DoesNotExist:
            totalMarkObj = None
            rank = None

        if rank is None:
            return HttpResponse('Result Not Published Yet !!')

        context = {
            'student': student,
            'subjectMarks': subjectMarks,
            'total_marks': total_marks,
            'percentage': percentage,
            'totalMarkObj': totalMarkObj,
            'uid': id,
            'exams':exams,
        }

        return render(request, 'gradesheet.html', context)

    except User.DoesNotExist:
        return HttpResponse('User Not Found!')

    except Student.DoesNotExist:
        return HttpResponse('Student Not Found!')