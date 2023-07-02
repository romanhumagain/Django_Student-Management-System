from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login
from Staff.models import *

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from Staff.models import *

def index(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        password = data.get('password')

        user = User.objects.filter(username = email)
        if not user.exists():
            messages.error(request, "Invalid Email")
            return redirect('/')
        
        # Authenticate using email as the username and password
        authenticated_user = authenticate(request, username=email, password=password)
        
        if authenticated_user is not None:
            login(request, authenticated_user)
            return redirect('/staff/staff_dashboard/')
        
        # Authentication failed
        if authenticated_user is None:
            messages.error(request, "Invalid Email/Password ")
            return redirect('/')
    
    return render(request, 'index.html')