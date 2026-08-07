import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import datetime

# Mock Contact Message object
class MockContactMessage:
    def __init__(self):
        self.name = "John Doe"
        self.email = "johndoe@example.com"
        self.phone = "+880 1234 567890"
        self.subject = "Urgent Quote for Hemp Ropes"
        self.message = "Hello,\n\nWe would like to request a quotation for 500 units of high-quality Tianjin Fiber Net Hemp Ropes. Please send us the pricing list and lead time details.\n\nBest regards,\nJohn Doe"

try:
    contact_msg = MockContactMessage()
    recipient = getattr(settings, 'EMAIL_RECIPIENT', 'munnahowlader06@gmail.com')
    subject = f"New Contact/Quote: {contact_msg.subject}"
    
    context = {
        'contact': contact_msg,
        'current_year': datetime.datetime.now().year
    }
    
    html_content = render_to_string('core/emails/contact_email.html', context)
    text_content = f"Name: {contact_msg.name}\nEmail: {contact_msg.email}\nPhone: {contact_msg.phone}\nSubject: {contact_msg.subject}\n\nMessage:\n{contact_msg.message}"
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
    print("Success! Mock quote enquiry email sent successfully in HTML format.")
except Exception as e:
    print("Failed to send mock email:", e)
