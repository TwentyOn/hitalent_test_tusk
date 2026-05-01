from core.celery import app
from django.core.mail import send_mail
from django.conf import settings


@app.task
def send_activation_key(email, activation_key):
    subject = 'Proxy-access service'
    body = f"""
    Greetings!
    
    Your new activation key: {activation_key}
    
    Enjoy using it!
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    to_emails = [email]
    send_mail(
        subject=subject,
        message=body,
        from_email=from_email,
        recipient_list=to_emails,
    )
