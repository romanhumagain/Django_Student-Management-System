from django.core.mail import send_mail
from django.conf import settings

def send_verification(email , token):
  send_mail(
    subject="Verify Your Account ",
    message= f'please click this link to verify your account: http://127.0.0.1:8000/student/verify_account/{token}/',
    from_email=settings.EMAIL_HOST_USER,
    recipient_list=[email,],
    fail_silently=True,
  )