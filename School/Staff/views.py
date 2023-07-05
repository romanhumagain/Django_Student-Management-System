from django.shortcuts import render , redirect
from Staff.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . utils import *
import random , string
from django.db.models import Q

# Create your views here.
# @login_required(login_url='/')
def staff_dashboard(request):
  
  return render(request, 'dashboard.html')

# @login_required(login_url='/')
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
    user.set_password(password)
    user.save()
    
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

def view_student(request):
  student = Student.objects.all().order_by('level__level')
  context = {}
  action = request.GET.get('action')
  
  if action == "all":
    student = Student.objects.all().order_by('level__level')
  if action == "bsc": 
    student = Student.objects.filter(course__course__icontains = 'BSC Hons').order_by('level__level')
  if action == "bba": 
    student = Student.objects.filter(course__course__icontains = 'BBA Hons').order_by('level__level') 
  
  search = request.GET.get('search')
  if search:
    student = student.filter( Q(name__icontains = search)|
                              Q(level__level__icontains = search ))

  if not student:
    context['error_message'] = 'No result found !'
    
  context.update({'querySet':student})
  return render(request , 'view student.html' , context)

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