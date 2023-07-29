from django.shortcuts import render , redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from  Staff . models import *
from .utils import *
from django.db.models import Sum

from datetime import datetime , date
from django.contrib.auth.decorators import login_required
# Create your views here.
import uuid
from django.core.paginator import Paginator


@login_required(login_url='/')
def student_dashboard(request , uid ):
  user = User.objects.get(id = uid)
  student = Student.objects.get(user = user)
  first_name, last_name = student.name.split(' ', 1)
  name = [first_name , last_name ]
  
  context = {'name':name}
  
  user = User.objects.get(id = uid)
  profile = Profile.objects.get(user = user)
  
  is_verified = profile.is_verified
  notice = Notice.objects.all()
  notice_count = notice.count()
  
  level_id = student.level
  course_id = student.course
  
  submitted_assignments = SubmittedAssignment.objects.filter(student = student).values_list('assignment_id', flat=True)
  assignments = Assignment.objects.filter(course = course_id , level = level_id).exclude(id__in=submitted_assignments)

  ass_count = assignments.count()
  current_date = date.today()
  try:
    attendance = Attendance.objects.get(student = student , date = current_date)
    attendance_status =  attendance.attendance 
    if attendance_status == "Absent":
      context.update({'absent_error': "Absent"})
    
    else:
      context.update({'absent_error':None})
      
  except Attendance.DoesNotExist:
    context.update({'pending_status': "Pending"})
    
  current_time = datetime.now().time()
  greeting = ""
  if current_time.hour < 12:
        greeting = "Good Morning"
  elif 12 <= current_time.hour < 18:
        greeting = "Good Afternoon"
  else:
        greeting = "Good Evening"
  
  context.update({'student':student ,'uid':uid , 'notices':notice, 'notice_count':notice_count , 'assignments':assignments , 'ass_count':ass_count , 'greeting':greeting})
  
  if not is_verified:
    context['verification_error'] = 'please verify your account'
  
  if request.method ==  'POST':
    action = request.POST.get('action')
    if action == 'profile_pic':
      pic= request.FILES.get('profile_pic')
      student.profile_pic = pic
      student.save()
      # messages.success(request , 'Successfully Uploaded Profile Pic')
      return redirect(f'/student/student_dashboard/{uid}')
   
    if action == 'verify':
      user = User.objects.get(id = uid)
      email = user.username
      
      profile = Profile.objects.get(user = user)
      verification_token = profile.token
       
      send_verification(email , verification_token)
      messages.success(request , 'successfully sent verification link' )
      return redirect(f'/student/student_dashboard/{uid}')
    
    if action == "EditInfo":
      first_name = request.POST.get('firstName')
      last_name = request.POST.get('lastName')
      phone_no = request.POST.get('phoneNo')
      
      full_name = " ".join([first_name , last_name])
      print(full_name)
      student.name =  full_name
      student.phone_no = phone_no
      student.save()
      
      return redirect(f'/student/student_dashboard/{uid}/')
    
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

        totalMarkObjects = TotalMark.objects.filter(student=student)
        results = []

        for exam in exams:
            subjectMarks = SubjectMarks.objects.filter(student=student, exam=exam)
            sub_count = Subject.objects.filter(course__course=course, level__level=level).count()

            total_full_marks = sub_count * 100
            total_marks = subjectMarks.aggregate(total_marks=Sum('marks'))['total_marks']
            total_marks = total_marks or 0

            percentage = (total_marks / total_full_marks) * 100 if total_full_marks != 0 else 0
            totalMarkObj = totalMarkObjects.filter(exam=exam).first()
            rank = totalMarkObj.rank if totalMarkObj else None

            results.append({
                'exam': exam,
                'subjectMarks': subjectMarks,
                'total_marks': total_marks,
                'percentage': percentage,
                'rank': rank,
            })

        context = {
            'student': student,
            'results': results,
            'uid': id,
        }

        notice = Notice.objects.all()
        notice_count = notice.count()
        
        level_id = student.level
        course_id = student.course
  
        submitted_assignments = SubmittedAssignment.objects.filter(student = student).values_list('assignment_id', flat=True)
        assignments = Assignment.objects.filter(course = course_id , level = level_id).exclude(id__in=submitted_assignments)

        ass_count = assignments.count()
        context.update({'notice_count':notice_count , 'ass_count':ass_count})
        
        current_date = date.today()
        try:
          attendance = Attendance.objects.get(student = student , date = current_date)
          attendance_status =  attendance.attendance 
          if attendance_status == "Absent":
            context.update({'absent_error': "Absent"})
          
          else:
            context.update({'absent_error':None})
            
        except Attendance.DoesNotExist:
          context.update({'pending_status': "Pending"})
          

        return render(request, 'gradesheet.html', context)

    except User.DoesNotExist:
        return HttpResponse('User Not Found!')

    except Student.DoesNotExist:
        return HttpResponse('Student Not Found!')
  
def view_assignment(request , id):
  user = User.objects.get(id= id)
  student = Student.objects.get(user = user)
  context = {}
  
  current_date = date.today()
  current_time = datetime.now().time()
  
  current_date_time = datetime.now()
  
  if request.method == "POST":
    data = request.POST
    assignment_id = data.get('assignment')
    assignment_description = data.get('assignmentDesc')
    assignment_file = request.FILES.get('assignmentFile')
    assignment = get_object_or_404(Assignment, id=assignment_id)
    due_date = assignment.due_date
    due_time = assignment.due_time
    
    due_date_time = datetime.combine(due_date,due_time )
    
    assignment_status = ""
    if current_date_time >= due_date_time :
      assignment_status = "Late Submission"
    else:
      assignment_status = "Submitted"
      
    assignment_submission =SubmittedAssignment.objects.create(student = student , assignment = assignment ,submitted_date = current_date, submitted_time = current_time ,submitted_assignment = assignment_file , assignment_description = assignment_description , submission_status =assignment_status )
    return redirect('std_assignment' , id = id)
  
  notice = Notice.objects.all()
  notice_count = notice.count()
  
  try:
    attendance = Attendance.objects.get(student = student , date = current_date)
    attendance_status =  attendance.attendance 
    if attendance_status == "Absent":
      context.update({'absent_error': "Absent"})
    
    else:
      context.update({'absent_error':None})
      
  except Attendance.DoesNotExist:
    context.update({'pending_status': "Pending"})
    
  
  level_id = student.level
  course_id = student.course
  

  submitted_assignments = SubmittedAssignment.objects.filter(student = student).values_list('assignment_id', flat=True)
  assignments = Assignment.objects.filter(course = course_id , level = level_id).exclude(id__in=submitted_assignments)
  ass_count = assignments.count()

  assignment_submissions = SubmittedAssignment.objects.filter(student = student)
  context.update({'student':student ,'uid':id ,'assignments':assignments  , 'notice_count':notice_count , 'ass_count':ass_count , 'submitted_assignments':assignment_submissions})
  
  return render(request , 'std_assignment.html' , context)

def view_attendance(request , id):
    context = {}
    user = User.objects.get(id = id)
    student = Student.objects.get(user = user)
    attendance_records = Attendance.objects.filter(student = student).order_by('-date')
    
    paginator = Paginator(attendance_records, 3)
    page_number = request.GET.get("page" , 1)
    page_obj = paginator.get_page(page_number)
    
    print(page_obj.object_list)
    attendance_count = attendance_records.count()
    present_attendance_count = 0
  
    for attendance in attendance_records:
        if attendance.attendance == "Present":
            present_attendance_count += 1
    
    if attendance_count != 0:
        present_attendance_percentage = (present_attendance_count / attendance_count) * 100
        context.update({"present_attendance_percentage":present_attendance_percentage})
    else:
        context.update({'attendance_status':"Attendance Not Taken"})
    
    if request.method == "POST":
        data = request.POST
        search = data.get('search')
        
        if search:
            page_obj = attendance_records.filter(date__contains = search)
    
    notice = Notice.objects.all()
    notice_count = notice.count()
        
    level_id = student.level
    course_id = student.course
  
    submitted_assignments = SubmittedAssignment.objects.filter(student = student).values_list('assignment_id', flat=True)
    assignments = Assignment.objects.filter(course = course_id , level = level_id).exclude(id__in=submitted_assignments)

    ass_count = assignments.count()
    current_date = date.today()
    try:
      attendance = Attendance.objects.get(student = student , date = current_date)
      attendance_status =  attendance.attendance 
      if attendance_status == "Absent":
        context.update({'absent_error': "Absent"})
      
      else:
        context.update({'absent_error':None})
        
    except Attendance.DoesNotExist:
      context.update({'pending_status': "Pending"})  
       
    context.update({'notice_count':notice_count , 'ass_count':ass_count})
    
    context.update({'attendance_records':page_obj , 'uid':id})
    return render(request, 'std_attendance.html' , context)
