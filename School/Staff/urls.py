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
  path('grades/' , grades , name='grades'),
  path('view_grades/' , view_grades , name='view_grades'),
  path('view_marksheet/<int:id>/' , view_marksheet , name='view_marksheet'),
  path('view_submission/<int:id>/', view_submission , name='view_submission'),
]