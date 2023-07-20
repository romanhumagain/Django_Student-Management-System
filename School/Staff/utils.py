from django.core.mail import EmailMultiAlternatives ,send_mail
from datetime import date
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

def absent_mail(absent_student_email):
    current_date = date.today()
    send_mail(
        subject="Regarding Absent",
        message = f"You were absent on {current_date}. Please provide a valid reason for your absence. Thank you.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=absent_student_email,
        fail_silently=False
    )
    
def send_email(to_email , subject , message , attachment):
    
    email = EmailMultiAlternatives(
       subject=subject,
       body=message,
       from_email=settings.EMAIL_HOST_USER,
       to=[to_email,],
    )
    
    if not attachment is None:
       email.attach(attachment.name ,attachment.read(), attachment.content_type )
       
    email.content_subtype = 'html'
    email.send()
   
   
    

