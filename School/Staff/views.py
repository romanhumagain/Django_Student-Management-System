from django.http import HttpResponse
import datetime
from django.shortcuts import render , redirect
from Staff.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . utils import *
import random , string
from django.db.models import Q
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
import uuid
from django.db.models import Sum , Q
from django.core.paginator import Paginator


@login_required(login_url="/")
def staff_dashboard(request):
  
  if request.method == 'POST':
    data = request.POST
    action = data.get('action')
    
    if action == "post_notice":
      notice =data.get('notice')
      notice = Notice.objects.create(notice = notice)
  
    # for searching attendance
    if action == "search":
      name = data.get('name')
      date = data.get('date')
      stdid = data.get('stdid')
      
      try:
        student = Student.objects.get(student_id = stdid , name = name )
      except ObjectDoesNotExist:
          messages.error(request , name +" with student id-"+stdid+" doesn't exists" )
          return redirect("/staff/staff_dashboard/")
      try:  
        attendance = Attendance.objects.get(student = student , date = date)
      except ObjectDoesNotExist:
          messages.error(request , "Attendance not taken on "+date )
          return redirect("/staff/staff_dashboard/")
      
      attendance_status = attendance.attendance  
      if attendance_status == "Present":
          messages.success(request , name+" was Present on "+date )
          return redirect('/staff/staff_dashboard/')
      else:
          messages.error(request , name+" was Absent on "+date )
          return redirect('/staff/staff_dashboard/')
        
  notice = Notice.objects.all()
  context = {'notices':notice}
  return render(request, 'dashboard.html',context)

@login_required(login_url='/')
def student_registration(request):
  
  upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  lower_case = " abcdefghijklmnopqrstuvwxyz"
  digits = "123456789"
  
  String = upper_case+lower_case+digits
  length = 12
  password = "".join(random.sample(String,length))
  student_id = "".join(random.choices(string.digits, k=4))
  
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
    user.set_password("romanroman")
    user.save()
    
    userType = UserType.objects.create(user = user)
    
    profile = Profile.objects.create(user = user , token = str(uuid.uuid4()))
    
    course = Course.objects.get(course = course)
    level = Level.objects.get(level = level)
    
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
    
    # send_password(email , password , intake)
    messages.success(request , f'Successfully Registered {name}')
    return redirect('/staff/student_registration/')
  
  return render(request , 'registration.html')

@login_required(login_url='/')
def view_student(request):
  student = Student.objects.all().order_by('level__level')
  context = {}
  action = request.GET.get('action')
  
  paginator = Paginator(student , 2)
  page_number = request.GET.get('page' , 1)
  page_obj = paginator.get_page(page_number)
  
  
  if action == "all":
    student = Student.objects.all().order_by('level__level')
  if action == "bsc": 
    student = Student.objects.filter(course__course__icontains = 'BSC Hons').order_by('level__level')
  if action == "bba": 
    student = Student.objects.filter(course__course__icontains = 'BBA Hons').order_by('level__level') 
  
  search = request.GET.get('search')
  
  if search:
    page_obj = student.filter( Q(name__icontains = search)|
                              Q(level__level__icontains = search ))
  if not student:
    context['error_message'] = 'No result found !'
    
  context.update({'querySet':page_obj})
  
  if request.method == "POST":
    data = request.POST
    action = data.get('action')
    attachment = None
    
    if action == "send_email":
      message = data.get('message')
      subject = data.get('subject')
      to_email = data.get('to')
      
      attachment = request.FILES.get('attachment')
      
      send_email(to_email, subject, message , attachment)
      messages.success(request , "successfully sent email")
      return redirect('/staff/view_student/')
    
  return render(request , 'view student.html' , context)

@login_required(login_url='/')
def course_details(request):
  
  bsc_count = Student.objects.filter(course__course = "BSC Hons").count()
  bsc_l4 = Student.objects.filter(course__course="BSC Hons", level__level="Level 4").count()
  bsc_l5 = Student.objects.filter(course__course="BSC Hons", level__level="Level 5").count()
  bsc_l6 = Student.objects.filter(course__course="BSC Hons", level__level="Level 6").count()

  bba_count = Student.objects.filter(course__course="BBA Hons").count()
  bba_l4 = Student.objects.filter(course__course="BBA Hons", level__level="Level 4").count()
  bba_l5 = Student.objects.filter(course__course="BBA Hons", level__level="Level 5").count()
  bba_l6 = Student.objects.filter(course__course="BBA Hons", level__level="Level 6").count()

  bsc_subjects = Subject.objects.filter(course__course = 'BSC Hons').order_by('level__level')
  levels = Level.objects.values_list('level' , flat=True).order_by('level')
  context = {
             'bbs_data':{
               'count': bsc_count,
               'bsc_l4':bsc_l4,
               'bsc_l5':bsc_l5,
               'bsc_l6':bsc_l6
               },
             'bba_data':{
               'count': bba_count,
               'bba_l4':bba_l4,
               'bba_l5':bba_l5,
               'bba_l6':bba_l6
             },
             'bsc_subjects':bsc_subjects,
             'levels':levels
             }
  if request.method == 'POST':
    course = ""
    
    data = request.POST
    action = data.get('action')
    subject_name = data.get('subject')
    code = data.get('code')
    level = data.get('level')
    
    if action == 'bsc':
      course = "BSC Hons"
    elif action =='bba':
      course = "BBA Hons"
    
    level_inst = Level.objects.get(level = level)
    course_inst = Course.objects.get(course = course)
        
    subject = Subject.objects.create(
      sub_name = subject_name,
      sub_code = code,
      level = level_inst,
      course = course_inst )
    
    messages.success(request , f"Successfully added {subject_name} subject")
    return redirect("/staff/course/")
      
  return render(request , 'course.html' , context)

@login_required(login_url='/')
def delete_notice(request , id):
  notice = Notice.objects.filter(id = id)
  notice.delete()
  return redirect('/staff/staff_dashboard/')

@login_required(login_url='/') 
def assignment(request):
  
  if request.method == 'POST':
    data = request.POST
    
    course = data.get('course')
    level = data.get('level')
    assignment = data.get('assignment')
    due_date = data.get('date')
    due_time = data.get('time')
    
    course = Course.objects.get(course = course)
    level = Level.objects.get(level = level)
    
    assignment = Assignment.objects.create(course = course , level = level , assignment = assignment , due_date =due_date , due_time = due_time)
    messages.success(request , 'successfully posted assignment')
    return redirect('/staff/assignment/')
  assignment = Assignment.objects.all()
  context = {'assignments':assignment}
  return render( request, 'assignment.html', context)

@login_required(login_url='/')
def delete_assignment(request , id):
  assignment = Assignment.objects.filter(id = id)
  assignment.delete()
  return redirect('/staff/assignment/')

@login_required(login_url='/')
def attendance(request):
    current_date_and_time = datetime.datetime.now()
    formatted_date_and_time = current_date_and_time.strftime("%Y-%m-%d %H:%M")

    current_date_and_time = datetime.datetime.now()
    context = {'current_date_and_time':formatted_date_and_time}
    
    current_date = date.today()
    global course 
    global level 
    
    if request.method == 'POST':
      data = request.POST
      action = data.get('action')
      
      if action == 'sort':
            current_date = date.today()
            course = data.get('course')
            level = data.get('level')
            
            
            course_inst = Course.objects.get(course=course)
            level_inst = Level.objects.get(level=level)
            
            students = Student.objects.filter(course=course_inst, level=level_inst)
            
            for student in students:
              attendance = Attendance.objects.filter(student = student , date = current_date)
              if attendance:
                messages.error(request , 'Attendance Already Taken !!')
                return redirect('/staff/attendance/')
              else:
                break
            if not students:
                context['error_message'] = 'No students found'
            context.update({'students': students})
            
      if action == 'attendance':
        
            course_inst = Course.objects.get(course=course)
            level_inst = Level.objects.get(level=level)
            
            selected_attendance = request.POST.getlist('attendance[]')
            presented_attendance=list(map(int, selected_attendance))
            
            all_students = Student.objects.filter(course=course_inst, level=level_inst)
            absent_student_email = []
            
            for student in all_students:
                std_id = student.student_id
                user = student.user  
                email = user.username  
                if std_id in presented_attendance:
                    attendance_status = 'Present'
                else:
                    absent_student_email.append(email)
                    attendance_status = 'Absent'
                    
                Attendance.objects.create(student=student, attendance=attendance_status, date=current_date)
            if absent_student_email:
              absent_mail(absent_student_email)
            return redirect('/staff/attendance/')
    return render(request, 'attendance.html', context)
  
@login_required(login_url='/')
def grades(request):
    exams = Examination.objects.all().order_by('-id')
    context = {'exams': exams}
    
    global selected_exam
    global level
    
    if request.method == 'POST':
        data = request.POST
        selected_exam = data.get('exam')
        level = data.get('level')
        Std_name = data.get('student')
        action = data.get('action')
        course = ""
        
        context.update({"level":level , 'selected_exam':selected_exam})

        if action == "bsc":
            course = "BSC Hons"
        elif action == "bba":
            course = "BBA Hons"
        
        students = Student.objects.filter(level__level__contains=level, course__course__contains=course)
        subjects = Subject.objects.filter(level__level__contains=level, course__course__contains=course)
        
        students_not_in_marks = students.exclude(subjectmarks__exam__exam__contains=selected_exam)
             
        context.update({'students': students_not_in_marks, 'subjects': subjects})
            
        if action == 'submit':
            exam = Examination.objects.get(exam = selected_exam)
            student = Student.objects.get(id = Std_name)
            subjects = Subject.objects.filter(level__level__contains="Level 4", course__course__contains=course)
            marks_list = []
            for subject in subjects:
                marks = int(request.POST.get(f"subject{subject.sub_name}"))
                subjectMarks = SubjectMarks.objects.create(student = student , subject = subject , exam = exam , marks = marks)
                marks_list.append(marks)
                
            total_marks = sum(marks_list)
            totalMarkObj = TotalMark.objects.create(student = student , total_mark = total_marks , exam = exam)

            if not students_not_in_marks:
              totalMarkObj = TotalMark.objects.filter(exam = exam).order_by('-total_mark')
              
              previous_total_mark = None
              previous_rank = 0
              
              for total_mark in totalMarkObj:
                if total_mark.total_mark != previous_total_mark:
                  rank = previous_rank+1
                  previous_rank = rank
                  
                  total_mark.rank = rank
                  total_mark.save()
                  
                  previous_total_mark = total_mark.total_mark
                  
    return render(request, 'grades.html', context)

@login_required(login_url='/')
def view_grades(request):
    exams = Examination.objects.all().order_by('-id')
    context = {'exams': exams}

    selected_exam = ""
    level = ""
    search_query = ""

    students = Student.objects.all()
    
    if request.method == 'POST':
        data = request.POST
        selected_exam = data.get('exam')
        level = data.get('level')
        action = data.get('action')
        search_query = data.get('search')
        course = ""

        context.update({'selected_exam': selected_exam ,"level":level})

        if action == "bsc hons":
            course = "BSC Hons"
        elif action == "bba hons":
            course = "BBA Hons"

        students = Student.objects.all()

        if level is not None:
            students = students.filter(level__level__contains=level)

        if course:
            students = students.filter(course__course__contains=course)

        if search_query:
            students = students.filter(name__icontains=search_query)

        context.update({'students': students})

    context.update({'search_query': search_query})
    return render(request, 'view grades.html', context)

@login_required(login_url='/')
def view_marksheet(request, id):
    exams = Examination.objects.all().order_by('-id')
    student = Student.objects.get(id=id)  # Get the selected student
    course = student.course
    level = student.level
    
    if request.method == 'POST':
        data = request.POST
        search = data.get('search')
        
        if search:
          exams = exams.filter(Q(exam__icontains = search)|
                               Q(date__icontains = search))
      
    
    context = {'exams': exams, 'student': student}
    
    totalMarkObject = TotalMark.objects.filter(student = student)
    
    results = []
    
    for exam in exams:
      subjectMarks = SubjectMarks.objects.filter(student = student , exam = exam)
      sub_count = Subject.objects.filter(course__course = course , level__level = level).count()
      total_full_marks = sub_count * 100
      
      try:
        totalMarks = TotalMark.objects.get(student =student , exam = exam)
        total_marks = totalMarks.total_mark
        percentage = (total_marks / total_full_marks) * 100 if total_full_marks != 0 else 0
        rank = totalMarks.rank if totalMarks else None
      except TotalMark.DoesNotExist:
        total_marks = None
        percentage = None
        rank = None
        
      results.append({
        'exam':exam,
        'subjectMarks':subjectMarks,
        'total_marks':total_marks, 
        'percentage':percentage,
        'rank':rank
      })
      context .update({
        'results':results,
        'student':student,
                 })
    
    return render(request, 'marksheet.html', context)
