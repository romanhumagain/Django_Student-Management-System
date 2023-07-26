from django.urls import path
from .views import *
urlpatterns = [
  path('student_dashboard/<int:uid>/' , student_dashboard , name='student_dashboard'),
  path('signout/' , sign_out , name='signout'),
  path('verify_account/<str:token>/' , verify_account , name='verify_account'),
  path('gradesheet/<int:id>/' , gradesheet , name="gradesheet"),
  path('std_assignment/<int:id>/' , view_assignment , name='std_assignment'),
  path('std_attendance/<int:id>/' , view_attendance , name="std_attendance"),
]