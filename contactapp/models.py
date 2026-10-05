from django.db import models
from django.contrib.auth.models import User
from core.models import SingletonModel
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class ContactPageSettings(SingletonModel):
    title = models.CharField(max_length=200, default="Contact Us")
    subtitle = models.TextField(default="Get in touch with our team.")
    bg_image = ProcessedImageField(upload_to='contact/', processors=[ResizeToFill(1920, 600)], format='WEBP', options={'quality': 80}, null=True, blank=True)
    
    address = models.TextField(default="123 Industrial Ave, Tianjin, China")
    email = models.EmailField(default="info@tianjinfibernet.com")
    phone = models.CharField(max_length=50, default="+86 123 4567 8900")
    business_hours = models.TextField(default="Mon-Fri: 9:00 AM - 6:00 PM")
    map_iframe = models.TextField(blank=True, help_text="Google Maps iframe embed code")

    def __str__(self):
        return "Contact Page Settings"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class HostingerEmailSettings(SingletonModel):
    smtp_host = models.CharField(max_length=200, default='smtp.hostinger.com', verbose_name="Hostinger SMTP Host")
    smtp_port = models.IntegerField(default=465, verbose_name="SMTP Port", help_text="Default is 465 for SSL or 587 for TLS")
    smtp_user = models.CharField(max_length=255, blank=True, verbose_name="Hostinger Email (Username)", help_text="Your Hostinger email address, e.g. info@tjropenet.com")
    smtp_password = models.CharField(max_length=255, blank=True, verbose_name="Hostinger Email Password", help_text="Your Hostinger email password")
    use_ssl = models.BooleanField(default=True, verbose_name="Use SSL (Port 465)")
    use_tls = models.BooleanField(default=False, verbose_name="Use TLS (Port 587)")
    sender_name = models.CharField(max_length=150, default="Tianbao Group", blank=True, verbose_name="Default Sender Name")
    default_signature = models.TextField(blank=True, default="Best Regards,\nTianbao Group\nhttps://tjropenet.com", verbose_name="Default Email Signature")
    # IMAP Incoming Settings
    imap_host = models.CharField(max_length=200, default='imap.hostinger.com', verbose_name="Hostinger IMAP Host (Incoming)")
    imap_port = models.IntegerField(default=993, verbose_name="IMAP Port", help_text="Default is 993 for SSL")
    use_imap_ssl = models.BooleanField(default=True, verbose_name="Use IMAP SSL")
    is_active = models.BooleanField(default=True, verbose_name="Enable Hostinger SMTP")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hostinger Email Setting"
        verbose_name_plural = "Hostinger Email Settings"

    def __str__(self):
        return f"Hostinger Email Config ({self.smtp_user or 'Not configured'})"


class ReceivedEmail(models.Model):
    message_id = models.CharField(max_length=255, unique=True, db_index=True, verbose_name="Message ID")
    uid = models.CharField(max_length=100, blank=True, verbose_name="IMAP UID")
    sender_name = models.CharField(max_length=255, blank=True, verbose_name="Sender Name")
    sender_email = models.CharField(max_length=255, db_index=True, verbose_name="Sender Email")
    recipient = models.CharField(max_length=255, blank=True, verbose_name="Recipient")
    subject = models.CharField(max_length=500, blank=True, verbose_name="Subject")
    snippet = models.CharField(max_length=300, blank=True, verbose_name="Snippet Preview")
    body_text = models.TextField(blank=True, verbose_name="Body (Plain Text)")
    body_html = models.TextField(blank=True, verbose_name="Body (HTML)")
    has_attachment = models.BooleanField(default=False, verbose_name="Has Attachment")
    attachment_names = models.CharField(max_length=500, blank=True, verbose_name="Attachment Names")
    is_read = models.BooleanField(default=False, db_index=True, verbose_name="Is Read")
    is_starred = models.BooleanField(default=False, verbose_name="Is Starred")
    folder = models.CharField(max_length=50, default='INBOX', verbose_name="Folder")
    received_at = models.DateTimeField(db_index=True, verbose_name="Received Date")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Synced At")

    class Meta:
        verbose_name = "Received Email"
        verbose_name_plural = "Received Emails (Inbox)"
        ordering = ['-received_at']

    def __str__(self):
        return f"From: {self.sender_name or self.sender_email} - {self.subject[:35]}"


class SentEmailLog(models.Model):
    STATUS_CHOICES = [
        ('Sent', 'Sent'),
        ('Failed', 'Failed'),
    ]

    recipient = models.CharField(max_length=255, verbose_name="Recipient Email(s)")
    cc = models.CharField(max_length=255, blank=True, verbose_name="Cc")
    bcc = models.CharField(max_length=255, blank=True, verbose_name="Bcc")
    subject = models.CharField(max_length=255, verbose_name="Subject")
    message = models.TextField(verbose_name="Message Content")
    attachment_name = models.CharField(max_length=255, blank=True, verbose_name="Attachment Name")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Sent', verbose_name="Delivery Status")
    error_message = models.TextField(blank=True, null=True, verbose_name="Error Details")
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sent By")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Sent At")

    class Meta:
        verbose_name = "Sent Email Log"
        verbose_name_plural = "Sent Email Logs"
        ordering = ['-sent_at']

    def __str__(self):
        return f"To: {self.recipient} - {self.subject[:30]} ({self.status})"
