import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

print("EMAIL_HOST_USER:", settings.EMAIL_HOST_USER)
print("EMAIL_RECIPIENT:", settings.EMAIL_RECIPIENT)
print("DEFAULT_FROM_EMAIL:", settings.DEFAULT_FROM_EMAIL)

try:
    subject = "SMTP Setup Test"
    text_content = "This is a test email checking SMTP connection settings."
    html_content = "<p>This is a <b>test email</b> checking SMTP connection settings.</p>"
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.EMAIL_RECIPIENT],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    print("Success! Test email sent successfully.")
except Exception as e:
    print("Failed to send email:", e)
