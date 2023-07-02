from django.urls import path
from . views import *
urlpatterns = [
  path('staff_dashboard/' , staff_dashboard , name='staff_dashboard' ),
  path('student_registration/' , student_registration , name='student_registration'),
  path('view_student/' , view_student , name='view_student')
]