from django.urls import path
from . views import *
urlpatterns = [
  path('staff_dashboard/' , staff_dashboard , name='staff_dashboard' ),
  path('student_registration/' , student_registration , name='student_registration'),
  path('view_student/' , view_student , name='view_student'),
  path('course/' , course_details , name='course'),
  path('delete_notice/<int:id>/' , delete_notice , name='delete_notice'),
  path('assignment/', assignment , name='assignment' ),
  path('delete_assignment/<int:id>/' , delete_assignment , name='delete_assignment'),
  path('attendance/', attendance , name='attendance' ),
]