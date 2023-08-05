from django.urls import path
from .views import *
urlpatterns = [
  path('student_dashboard/<slug:slug>/' , StudentDashboard.as_view() , name='student_dashboard'),
  path('signout/' , sign_out , name='signout'),
  path('verify_account/<str:token>/' , VerifyAccount.as_view() , name='verify_account'),
  path('gradesheet/<slug:slug>/' , StudentGradeSheet.as_view() , name="gradesheet"),
  path('std_assignment/<slug:slug>/' , ViewAssignment.as_view() , name='std_assignment'),
  path('std_attendance/<slug:slug>/' , ViewAttendance.as_view() , name="std_attendance"),
  # path('download/marksheet/<int:user_id>/<int:exam_id>/', download_marksheet, name='download_marksheet'),
]