from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_password(email, password , intake):
    message = f"Email: <strong>{email}</strong> <br/>Password: <strong>{password}</strong> <br/> Please use this email and password to access your account. You can also change your password from your profile section."
    message += f"<br/><br/>You have successfully registered for {intake}"
    
    email = EmailMultiAlternatives(
        subject="Congratulation! you are successfully registered !",
        from_email=settings.EMAIL_HOST_USER,
        body=message,
        to=[email]
    )
    email.content_subtype = 'html'
    email.send()

