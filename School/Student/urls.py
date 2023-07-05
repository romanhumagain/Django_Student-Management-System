from django.urls import path
from .views import *
urlpatterns = [
  path('student_dashboard/<int:uid>/' , student_dashboard , name='student_dashboard'),
  path('signout/' , sign_out , name='signout'),
]