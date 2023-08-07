from django.urls import path
from . views import *
urlpatterns = [
  path('staff_dashboard/' , StaffDashboard.as_view() , name='staff_dashboard' ),
  path('student_registration/' , StudentRegistration.as_view() , name='student_registration'),
  path('view_student/' , ViewStudent.as_view() , name='view_student'),
  path('course/' , CourseDetails.as_view() , name='course'),
  path('delete_notice/<int:id>/' , DeleteNotice.as_view() , name='delete_notice'),
  path('assignment/', AssignmentView.as_view() , name='assignment' ),
  path('delete_assignment/<int:id>/' , DeleteAssignment.as_view() , name='delete_assignment'),
  path('attendance/', AttendanceView.as_view() , name='attendance' ),
  path('grades/' , GradesView.as_view() , name='grades'),
  path('view_marksheet/<slug:slug>/' , ViewMarksheet.as_view() , name='view_marksheet'),
  path('view_submission/<slug:slug>/', ViewSubmission.as_view() , name='view_submission'),
   path('student_attendance_record/<slug:slug>/', View_Student_Attendance.as_view(), name='student_attendance_record'),
  
]