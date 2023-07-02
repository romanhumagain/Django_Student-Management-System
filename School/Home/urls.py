from django.urls import path
from Home.views import *

urlpatterns = [
  path('' ,index , name='home' )
]