from django.shortcuts import render , redirect
from django.views import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from  Staff . models import *
from .utils import *
from django.db.models import Sum

from datetime import datetime , date
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
import uuid
from django.core.paginator import Paginator
from django.db.models import Q


@method_decorator(login_required(login_url='/') , name='dispatch')
class StudentDashboard(View):
  def get_student(self , slug):
    return get_object_or_404(Student, slug = slug)
  
  def get(self ,request, *args , **kwargs):
    student = self.get_student(slug=kwargs.get('slug'))
    user = student.user.id
    first_name, last_name = student.name.split(' ', 1)
    name = [first_name , last_name ]
    
    context = {'name':name}
    
    user = User.objects.get(id = user)
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
    greeting_icon = ""

    if current_time.hour < 12:
          greeting = "Good Morning"
          greeting_icon = "fa-sun"
    elif 12 <= current_time.hour < 18:
          greeting = "Good Afternoon"
          greeting_icon = "fa-sun"
    else:
          greeting = "Good Evening"
          greeting_icon = "fa-moon"
    
    context.update({'student':student ,'uid':kwargs.get('slug') , 'notices':notice, 'notice_count':notice_count , 'assignments':assignments , 'ass_count':ass_count , 'greeting':greeting , 'greeting_icon':greeting_icon})
    
    if not is_verified:
      context['verification_error'] = 'please verify your account'
      
    return render(request , 'student_dashboard.html' , context)
  
  def post(self ,request , *args, **kwargs):
    student = self.get_student(slug=kwargs.get('slug'))
    user = student.user.id
    action = request.POST.get('action')
    if action == 'profile_pic':
      pic= request.FILES.get('profile_pic')
      student.profile_pic = pic
      student.save()
      # messages.success(request , 'Successfully Uploaded Profile Pic')
      return redirect(f"/student/student_dashboard/{kwargs.get('slug')}")
   
    if action == 'verify':
      email = student.user.username
      
      profile = Profile.objects.get(user = user)
      verification_token = profile.token
       
      send_verification(email , verification_token)
      messages.success(request , 'successfully sent verification link to your email address ' )
      return redirect(f"/student/student_dashboard/{kwargs.get('slug')}")
    
    if action == "EditInfo":
      first_name = request.POST.get('firstName')
      last_name = request.POST.get('lastName')
      phone_no = request.POST.get('phoneNo')
      
      full_name = " ".join([first_name , last_name])
      student.name =  full_name
      student.phone_no = phone_no
      student.save()
      return redirect(f"/student/student_dashboard/{kwargs.get('slug')}") 
    return render(request , 'student_dashboard.html' , {})


def sign_out(request):
  logout(request)
  return redirect('/')

@method_decorator(login_required(login_url='/') , name='dispatch')
class VerifyAccount(View):
    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        try:
            profile = Profile.objects.get(token = token)
            profile.is_verified = True
            profile.save()
            return HttpResponse('Congratulation! Successfully Verified Your Account')
        
        except Exception as e:
            print(str(e))  # I moved this line up because it would never be reached after return statement
            return HttpResponse('Sorry Couldnt Verify Your Account')
    
@method_decorator(login_required(login_url='/') , name='dispatch')
class StudentGradeSheet(View):
    def get(self, request, slug, *args, **kwargs):
        try:
            student = Student.objects.get(slug=slug)
            exams = Examination.objects.all().order_by('-id') 
            course = student.course
            level = student.level

            search = request.GET.get('search')
            if search:
                exams = exams.filter(Q(exam__icontains = search) | Q(date__icontains = search))

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

            name = student.name
            first_name = name.split()[0]
            context = {
                'student': student,
                'results': results,
                'uid': slug,
                'first_name' :first_name
            }

            notice_count = Notice.objects.count()
            level_id = student.level
            course_id = student.course

            submitted_assignments = SubmittedAssignment.objects.filter(student=student).values_list('assignment_id', flat=True)
            assignments = Assignment.objects.filter(course=course_id , level=level_id).exclude(id__in=submitted_assignments)

            ass_count = assignments.count()
            context.update({'notice_count':notice_count , 'ass_count':ass_count})

            current_date = date.today()
            try:
                attendance = Attendance.objects.get(student=student , date=current_date)
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

@method_decorator(login_required(login_url='/') , name='dispatch')
class ViewAssignment(View):
    def get_student_and_present_date(self, slug):
        student = get_object_or_404(Student, slug=slug)
        current_date = date.today()
        return student, current_date
    
    def get(self, request, *args, **kwargs):
        student, current_date = self.get_student_and_present_date(kwargs.get('slug'))

        notice_count = Notice.objects.count()
        absent_error = None
        pending_status = None
        
        try:
            attendance = Attendance.objects.get(student=student, date=current_date)
            attendance_status = attendance.attendance 
            if attendance_status == "Absent":
                absent_error = "Absent"
            else:
                absent_error = None
        except Attendance.DoesNotExist:
            pending_status = "Pending"
        
        level_id = student.level
        course_id = student.course

        assignments = Assignment.objects.filter(course=course_id, level=level_id).exclude(submittedassignment__student=student)
        ass_count = assignments.count()

        assignment_submissions = SubmittedAssignment.objects.filter(student=student)

        context = {
            'student': student,
            'uid': kwargs.get('slug'),
            'assignments': assignments,
            'notice_count': notice_count,
            'ass_count': ass_count,
            'submitted_assignments': assignment_submissions,
            'absent_error': absent_error,
            'pending_status': pending_status,
        }
        
        return render(request, 'std_assignment.html', context)
      
    def post(self, request, *args , **kwargs):
        student, current_date = self.get_student_and_present_date(kwargs.get('slug'))

        current_time = datetime.now().time()
        current_date_time = datetime.now()

        data = request.POST
        assignment_id = data.get('assignment')
        assignment_description = data.get('assignmentDesc')
        assignment_file = request.FILES.get('assignmentFile')
        assignment = get_object_or_404(Assignment, id=assignment_id)
        due_date = assignment.due_date
        due_time = assignment.due_time
        
        due_date_time = datetime.combine(due_date, due_time)

        assignment_status = "Late Submission" if current_date_time >= due_date_time else "Submitted"
        
        assignment_submission = SubmittedAssignment.objects.create(
            student=student,
            assignment=assignment,
            submitted_date=current_date,
            submitted_time=current_time,
            submitted_assignment=assignment_file,
            assignment_description=assignment_description,
            submission_status=assignment_status
        )

        return redirect('std_assignment', slug=kwargs.get('slug'))
    
@method_decorator(login_required(login_url='/') , name='dispatch')
class ViewAttendance(View):
    def get_student_and_records(self , slug):
      student = Student.objects.get(slug = slug)
      attendance_records = Attendance.objects.filter(student= student).order_by('-date')
      return student , attendance_records
    
    def generate_context(self , request, slug , student , attendance_records ):
      context = {}
      paginator = Paginator(attendance_records ,3 )
      page_number = request.GET.get('page')
      page_obj = paginator.get_page(page_number)
      
      attendance_count= attendance_records.count()
      present_attendance_count = 0
      for attendance in attendance_records:
          if attendance.attendance == "Present":
              present_attendance_count += 1

          if attendance_count != 0:
              present_attendance_percentage = (present_attendance_count / attendance_count) * 100
              context.update({"present_attendance_percentage":present_attendance_percentage})
          else:
              context.update({'attendance_status':"Attendance Not Taken"})

      notice_count = Notice.objects.count()
      level_id = student.level
      course_id = student.course
      submitted_assignments = SubmittedAssignment.objects.filter(student=student).values_list('assignment_id', flat=True)
      assignments = Assignment.objects.filter(course=course_id , level=level_id).exclude(id__in=submitted_assignments)

      ass_count = assignments.count()
      current_date = date.today()
      try:
          attendance = Attendance.objects.get(student=student , date=current_date)
          attendance_status =  attendance.attendance 
          if attendance_status == "Absent":
              context.update({'absent_error': "Absent"})
          else:
              context.update({'absent_error':None})
      except Attendance.DoesNotExist:
          context.update({'pending_status': "Pending"})

      context.update({'notice_count':notice_count , 'ass_count':ass_count})

      context.update({
              'attendance_records': page_obj,
              'uid': slug
          })
      return context
    
    def get(self , request , slug , *args , **kwargs):
      student , attendance_records = self.get_student_and_records(slug=slug)
      context = self.generate_context(request , slug , student , attendance_records )
      search = request.GET.get('search')
      if search:
        page_obj = attendance_records.filter(date__icontains = search)
        context['attendance_records'] = page_obj
      return render(request, 'std_attendance.html', context)
    
    def post(self, request , *args , **kwargs):
      return render(request, 'std_attendance.html', {})
      
  
  
# for printing the marksheet , but remaining to apply
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def download_marksheet(request, user_id, exam_id):
    user = User.objects.get(id = user_id)
    # Fetch the student's marksheet
    student = Student.objects.get(user = user)
    exam = Examination.objects.get(id=exam_id)
    subjectMarks = SubjectMarks.objects.filter(student=student, exam=exam)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Marksheet-{student}-{exam_id}.pdf"'

    # Using SimpleDocTemplate to add more sophistication
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Styles for paragraphs
    styles = getSampleStyleSheet()
    styleH = styles['Heading1']
    styleN = styles['Normal']

    # List to hold elements to add to PDF
    story = []

    # Adding heading and student details
    story.append(Paragraph('Marksheet', styleH))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f'Student Name: {student.name}', styleN))
    story.append(Paragraph(f'Exam Name: {exam.exam}', styleN))
    story.append(Paragraph(f'Exam Date: {exam.date}', styleN))
    story.append(Spacer(1, 12))

    # Preparing data for table
    data = [['Subject', 'Marks']]
    for subject_mark in subjectMarks:
        data.append([subject_mark.subject.sub_name, subject_mark.marks])

    # Creating a table and adding it to story
    t = Table(data)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                           ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                           ('FONTSIZE', (0, 0), (-1, 0), 14),

                           ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                           ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    story.append(t)

    # Building the PDF
    doc.build(story)
    return response

