from django.urls import path
from .views import *
urlpatterns = [
  path('student_dashboard/<slug:slug>/' , student_dashboard , name='student_dashboard'),
  path('signout/' , sign_out , name='signout'),
  path('verify_account/<str:token>/' , verify_account , name='verify_account'),
  path('gradesheet/<slug:slug>/' , gradesheet , name="gradesheet"),
  path('std_assignment/<slug:slug>/' , view_assignment , name='std_assignment'),
  path('std_attendance/<slug:slug>/' , view_attendance , name="std_attendance"),
  # path('download/marksheet/<int:user_id>/<int:exam_id>/', download_marksheet, name='download_marksheet'),
]