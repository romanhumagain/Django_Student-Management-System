from django.http import HttpResponse
import datetime
from django.shortcuts import get_object_or_404, render , redirect
from Staff.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . utils import *
import random , string
from django.db.models import Q
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
import uuid
from django.db.models import Sum , Q
from django.core.paginator import Paginator 
from django.views import View


@method_decorator(login_required(login_url='/') , name='dispatch')
class StaffDashboard(View):
  
  def get(self, request):
    data = request.GET
    action = data.get('action')
    if action == 'search':
      name = data.get('name')
      search_date = data.get('date')
      stdid = data.get('stdid')
      
      try:
        student = Student.objects.get(student_id = stdid , name = name )
      except ObjectDoesNotExist:
          messages.error(request , name +" with student id-"+stdid+" doesn't exists" )
          return redirect("/staff/staff_dashboard/")
      try:  
        attendance = Attendance.objects.get(student = student , date = search_date)
      except ObjectDoesNotExist:
          messages.error(request , "Attendance not taken on "+search_date )
          return redirect("/staff/staff_dashboard/")
      
      attendance_status = attendance.attendance  
      if attendance_status == "Present":
          messages.success(request , name+" was Present on "+search_date )
          return redirect('/staff/staff_dashboard/')
      else:
          messages.error(request , name+" was Absent on "+search_date )
          return redirect('/staff/staff_dashboard/')
    
    notice = Notice.objects.all()
    context = {'notices':notice}
    return render(request, 'dashboard.html',context)
  
  def post (self , request):
    data = request.POST
    action = data.get('action')
    
    if action == "post_notice":
      notice = data.get('notice')
      posted_date = date.today()
      print(posted_date)
      notice = Notice.objects.create(notice = notice, posted_date=posted_date)
      return redirect('/staff/staff_dashboard/')
      
    return render(request, 'dashboard.html',{})

@method_decorator(login_required(login_url='/') , name='dispatch')
class StudentRegistration(View):
  def get(self , request):
    
    return render(request , 'registration.html')
  def post(self , request):
    upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lower_case = " abcdefghijklmnopqrstuvwxyz"
    digits = "123456789"
    
    String = upper_case+lower_case+digits
    length = 12
    password = "".join(random.sample(String,length))
    
    last_student = Student.objects.all().order_by('-student_id').first()
    
    if last_student is None:
      student_id = "".join(random.choices(string.digits, k=4))
    else:
      student_id = int(last_student.student_id)+1
  
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
      
    send_password(email , password , intake)
    messages.success(request , f'Successfully Registered {name}')
    return redirect('/staff/student_registration/')
    
    return render(request , 'registration.html')


@method_decorator(login_required(login_url='/'),name="dispatch")
class CourseDetails(View):
  
  def get(self , request):
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
    return render(request , 'course.html' , context)
  
  def post(self, request):
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
  
  
@method_decorator(login_required(login_url='/'),name="dispatch")
class DeleteNotice(View):
  def get(self, request, *args , **kwargs):
    notice = Notice.objects.get(id = self.kwargs.get('id'))
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
    current_date = date.today()
    assignment = Assignment.objects.create(course = course , level = level , assignment = assignment , posted_date=current_date, due_date =due_date , due_time = due_time)
    
    email_address = []
    students = Student.objects.filter(course = course , level = level)
    
    for student in students:
      email = student.user.username
      email_address.append(email)
      
    from datetime import datetime  # Note the corrected import statement
    # parse the strings to datetime objects
    due_date = datetime.strptime(due_date, '%Y-%m-%d')

    # parse the string to a datetime object
    due_time = datetime.strptime(due_time, '%H:%M')

    # now you can format the datetime objects
    formatted_due_date = due_date.strftime('%B %d, %Y')  # e.g., 'August 01, 2023'
    formatted_due_time = due_time.strftime('%I:%M %p')  # e.g., '11:59 PM'

    message = f"You have been assigned an assignment which has a deadline of <strong>{formatted_due_date} at {formatted_due_time}</strong>. Please ensure to complete and submit it by the given due date.<br>Kind Regards, <br>MySchool"
    subject = "Regarding Assignment"
    
    
    send_email(email_address , subject , message , attachment=None )
    messages.success(request , 'successfully posted assignment')
    return redirect('/staff/assignment/')
  
  assignment = Assignment.objects.all().order_by('level')
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
              
            messages.success(request,"Attendance successfully taken !!")
            return redirect('/staff/attendance/')
          
    return render(request, 'attendance.html', context)
  
@login_required(login_url='/')
def grades(request):
    exams = Examination.objects.all().order_by('-id')
    context = {'exams': exams}
    
    global selected_exam
    global level
    global course 
    if request.method == 'POST':
        data = request.POST
        selected_exam = data.get('exam')
        level = data.get('level')
        Std_name = data.get('student')
        action = data.get('action')
        
        context.update({"level":level , 'selected_exam':selected_exam})

        if action == "BSC Hons":
            course = "BSC Hons"
        elif action == "BBA Hons":
            course = "BBA Hons"
        
        level_obj = Level.objects.get(level = level)
        print(f"Course: {course}")  # Debug line
        course_obj = Course.objects.get(course = course)
        
        students = Student.objects.filter(level=level_obj, course=course_obj)
        subjects = Subject.objects.filter(level=level_obj, course=course_obj)
        
        students_not_in_marks = students.exclude(subjectmarks__exam__exam__contains=selected_exam)
             
        context.update({'students': students_not_in_marks, 'subjects': subjects})
            
        if action == 'submit':
            exam = Examination.objects.get(exam = selected_exam)
            student = Student.objects.get(id = Std_name)
            subjects = Subject.objects.filter(level=level_obj, course=course_obj)
            marks_list = []
            if course_obj is not None:
              for subject in subjects:
                  marks = int(request.POST.get(f"subject{subject.sub_name}"))
                  subjectMarks = SubjectMarks.objects.create(student = student , subject = subject , exam = exam , marks = marks)
                  marks_list.append(marks)
            else:
                print(f"No Course found with the name: {course}")
                # Handle this case in some way, perhaps by returning an error message in the context

            total_marks = sum(marks_list)
            totalMarkObj = TotalMark.objects.create(student = student , total_mark = total_marks , exam = exam , level=level_obj, course=course_obj)

            if not students_not_in_marks:
              totalMarkObj = TotalMark.objects.filter(exam = exam , level=level_obj, course=course_obj).order_by('-total_mark')
              
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
def view_marksheet(request, slug):
    exams = Examination.objects.all().order_by('-id')
    student = Student.objects.get(slug=slug)  # Get the selected student
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
      first_name = student.name.split()[0]
      context .update({
        'results':results,
        'student':student,
        'first_name': first_name,
                 })
    return render(request, 'marksheet.html', context)
  
def view_submission(request, slug):
    assignment = Assignment.objects.get(slug=slug)
    submitted_assignment = SubmittedAssignment.objects.filter(assignment=assignment)

    paginator = Paginator(submitted_assignment , 5)
    page_number = request.GET.get('page' , 1)
    page_obj = paginator.get_page(page_number)
    
    search = request.GET.get('search')
    if search:
        page_obj = submitted_assignment.filter(student__name__icontains = search)

    context = {'submitted_assignment': page_obj}

    return render(request, 'view_submission.html', context)

# @login_required(login_url='/')
class ViewStudent(View):
  def get(self , request):
    
    students = Student.objects.all().order_by('level' , 'student_id')
    
    data = request.GET
    level = data.get('level')
    action = data.get('action')
    search = data.get('search')
    course = ""  
    if action == "bsc": 
        course = "BSC"
        students = Student.objects.filter(course__course__icontains = 'BSC Hons' , level__level__contains = level).order_by('level')
    elif action == "bba":
        course = "BBA" 
        students = Student.objects.filter(course__course__icontains = 'BBA Hons' , level__level__contains = level).order_by('level') 
    
    if search:
      searched = search.split()
      for word in searched:
        students = students.filter(Q(name__icontains = word)|
                                   Q(level__level__contains = word))    
    
    
    context = {'students':students , "level" :level , 'course':course}
    return render(request , "view_std.html" , context)
  
  def post(self, request):
    
    assignment = None 
    
    data = request.POST
    to_email = data.get('to')
    subject = data.get('subject') 
    message = data.get('message')   
    
    attachment = request.FILES.get('attachment')
    
    send_email([to_email] , subject , message , attachment)
    messages.success(request , "Successfully Sent Email !!")
    return redirect('view_student')
    return render(request , 'view_std')
  
class View_Student_Attendance(View):
    def get(self, request, slug):
        student = Student.objects.get(slug = slug)
        context = {'student':student}
        attendance_records = Attendance.objects.filter(student = student).order_by('-date')
        
        paginator = Paginator(attendance_records, 3)
        page_number = request.GET.get("page" , 1)
        page_obj = paginator.get_page(page_number)
        
        
        search = request.GET.get('search')
        if search:
          page_obj = attendance_records.filter(date__icontains= search)
          
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
            
        current_date = date.today()
        
            
        context.update({'attendance_records':page_obj , 'uid':slug})

        return render(request, 'view_std_attendance.html', context)

    def post(self, request, slug):
        return render(request, 'view_std_attendance.html')

  
    

