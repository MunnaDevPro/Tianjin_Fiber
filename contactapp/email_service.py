import smtplib
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import HostingerEmailSettings, SentEmailLog


def get_hostinger_config():
    """
    Returns configured Hostinger email credentials from Database (Singleton)
    with seamless fallback to Django settings / .env.
    """
    db_config = HostingerEmailSettings.objects.first()
    if db_config and db_config.is_active and db_config.smtp_user:
        return {
            'host': db_config.smtp_host or 'smtp.hostinger.com',
            'port': db_config.smtp_port or 465,
            'user': db_config.smtp_user.strip(),
            'password': db_config.smtp_password or '',
            'use_ssl': db_config.use_ssl,
            'use_tls': db_config.use_tls,
            'sender_name': db_config.sender_name or 'Tianbao Group',
            'signature': db_config.default_signature or '',
            'source': 'Database (HostingerEmailSettings)'
        }

    # Fallback to settings / environment variables
    env_user = getattr(settings, 'HOSTINGER_EMAIL_USER', None) or getattr(settings, 'EMAIL_HOST_USER', '')
    env_pass = getattr(settings, 'HOSTINGER_EMAIL_PASSWORD', None) or getattr(settings, 'EMAIL_HOST_PASSWORD', '')
    env_host = getattr(settings, 'HOSTINGER_EMAIL_HOST', None) or getattr(settings, 'EMAIL_HOST', 'smtp.hostinger.com')
    env_port = getattr(settings, 'HOSTINGER_EMAIL_PORT', None) or getattr(settings, 'EMAIL_PORT', 465)
    env_ssl = getattr(settings, 'HOSTINGER_EMAIL_USE_SSL', None)
    if env_ssl is None:
        env_ssl = True if env_port == 465 else False
    env_tls = getattr(settings, 'HOSTINGER_EMAIL_USE_TLS', None)
    if env_tls is None:
        env_tls = True if env_port == 587 else False

    return {
        'host': env_host,
        'port': env_port,
        'user': env_user.strip() if env_user else '',
        'password': env_pass or '',
        'use_ssl': env_ssl,
        'use_tls': env_tls,
        'sender_name': 'Tianbao Group',
        'signature': "Best Regards,\nTianbao Group\nhttps://tjropenet.com",
        'source': 'Environment (.env)'
    }


def test_hostinger_smtp_connection():
    """
    Tests SMTP connection and authentication against Hostinger mail servers.
    """
    config = get_hostinger_config()
    if not config['user'] or not config['password']:
        return False, "Hostinger email credentials (username & password) are not configured yet."

    host = config['host']
    port = int(config['port'])
    user = config['user']
    password = config['password']
    use_ssl = config['use_ssl']

    try:
        if use_ssl or port == 465:
            server = smtplib.SMTP_SSL(host, port, timeout=12)
        else:
            server = smtplib.SMTP(host, port, timeout=12)
            if config['use_tls']:
                server.starttls()

        server.login(user, password)
        server.quit()
        return True, f"Successfully authenticated with Hostinger SMTP ({user})!"
    except smtplib.SMTPAuthenticationError as e:
        return False, f"Hostinger Authentication Failed: Please check your email and password. Details: {e}"
    except smtplib.SMTPConnectError as e:
        return False, f"Could not connect to {host}:{port}. Details: {e}"
    except Exception as e:
        return False, f"Hostinger SMTP Connection Error: {str(e)}"


def _split_addresses(value):
    if not value:
        return []
    return [a.strip() for a in value.replace(';', ',').split(',') if a.strip()]


def send_hostinger_email(recipient, subject, message, cc=None, bcc=None, attachment=None,
                         user=None, attachments=None, in_reply_to=None):
    """
    Sends an email via Hostinger's SMTP server and logs the transaction.

    `attachment` (single file) is kept for backward compatibility;
    `attachments` accepts a list of uploaded files.
    `in_reply_to` (original Message-ID) threads the reply in the recipient's mail client.
    """
    files = list(attachments or [])
    if attachment:
        files.insert(0, attachment)
    attachment_label = ', '.join(f.name for f in files)[:255]

    config = get_hostinger_config()
    if not config['user'] or not config['password']:
        error_msg = "Hostinger email username or password is missing. Please configure Hostinger Email Settings first."
        SentEmailLog.objects.create(
            recipient=(recipient or '')[:255],
            cc=(cc or '')[:255],
            bcc=(bcc or '')[:255],
            subject=(subject or '')[:255],
            message=message,
            attachment_name=attachment_label,
            status='Failed',
            error_message=error_msg,
            sent_by=user
        )
        return False, error_msg

    host = config['host']
    port = int(config['port'])
    user_email = config['user']
    password = config['password']
    use_ssl = config['use_ssl']
    use_tls = config['use_tls']
    sender_name = config['sender_name']

    from_header = f"{sender_name} <{user_email}>" if sender_name else user_email

    # Parse recipients
    to_list = _split_addresses(recipient)
    cc_list = _split_addresses(cc)
    bcc_list = _split_addresses(bcc)

    if not to_list:
        return False, "Recipient email address is required."

    def _log(status, error_message=None):
        SentEmailLog.objects.create(
            recipient=', '.join(to_list)[:255],
            cc=', '.join(cc_list)[:255],
            bcc=', '.join(bcc_list)[:255],
            subject=(subject or '')[:255],
            message=message,
            attachment_name=attachment_label,
            status=status,
            error_message=error_message,
            sent_by=user
        )

    try:
        backend = EmailBackend(
            host=host,
            port=port,
            username=user_email,
            password=password,
            use_tls=use_tls,
            use_ssl=use_ssl,
            fail_silently=False,
            timeout=15
        )

        headers = {}
        if in_reply_to:
            headers['In-Reply-To'] = in_reply_to
            headers['References'] = in_reply_to

        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=from_header,
            to=to_list,
            cc=cc_list or None,
            bcc=bcc_list or None,
            headers=headers or None,
            connection=backend
        )

        for f in files:
            email.attach(f.name, f.read(), getattr(f, 'content_type', None))

        email.send(fail_silently=False)
        _log('Sent')
        return True, f"Email sent to {', '.join(to_list)}."

    except Exception as e:
        error_details = str(e)
        _log('Failed', error_details)
        return False, f"Failed to send email: {error_details}"
