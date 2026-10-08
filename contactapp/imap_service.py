import imaplib
import email
from email.header import decode_header
import email.utils
import hashlib
from datetime import datetime
from django.utils import timezone
from .models import HostingerEmailSettings, ReceivedEmail
from .email_service import get_hostinger_config


def decode_mime_string(header_val):
    """
    Decodes RFC 2047 MIME encoded header string into clean Unicode text.
    """
    if not header_val:
        return ""
    try:
        decoded_fragments = decode_header(header_val)
        result = []
        for text, encoding in decoded_fragments:
            if isinstance(text, bytes):
                enc = encoding or 'utf-8'
                try:
                    result.append(text.decode(enc, errors='replace'))
                except Exception:
                    result.append(text.decode('latin-1', errors='replace'))
            else:
                result.append(str(text))
        return "".join(result).strip()
    except Exception:
        return str(header_val).strip()


def extract_body_and_attachments(msg):
    """
    Extracts plain text body, HTML body, and attachment names from an email message.
    """
    body_text = ""
    body_html = ""
    attachment_names = []

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))

            # Attachment detection
            filename = part.get_filename()
            if filename:
                decoded_fname = decode_mime_string(filename)
                if decoded_fname:
                    attachment_names.append(decoded_fname)

            # Body parsing
            if "attachment" not in content_disposition:
                if content_type == "text/plain" and not body_text:
                    try:
                        payload = part.get_payload(decode=True)
                        charset = part.get_content_charset() or 'utf-8'
                        body_text = payload.decode(charset, errors='replace')
                    except Exception:
                        pass
                elif content_type == "text/html" and not body_html:
                    try:
                        payload = part.get_payload(decode=True)
                        charset = part.get_content_charset() or 'utf-8'
                        body_html = payload.decode(charset, errors='replace')
                    except Exception:
                        pass
    else:
        content_type = msg.get_content_type()
        try:
            payload = msg.get_payload(decode=True)
            charset = msg.get_content_charset() or 'utf-8'
            decoded = payload.decode(charset, errors='replace') if payload else ""
            if content_type == "text/html":
                body_html = decoded
            else:
                body_text = decoded
        except Exception:
            body_text = str(msg.get_payload() or "")

    return body_text.strip(), body_html.strip(), attachment_names


def parse_email_date(date_str):
    """
    Parses RFC 2822 email date into a timezone-aware datetime.
    """
    if not date_str:
        return timezone.now()
    try:
        dt = email.utils.parsedate_to_datetime(date_str)
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        return dt
    except Exception:
        return timezone.now()


def sync_hostinger_inbox(limit=30, folder='INBOX'):
    """
    Connects to Hostinger IMAP server via SSL, fetches latest messages,
    and persists them into ReceivedEmail database without duplicate records.
    """
    db_config = HostingerEmailSettings.objects.first()
    config = get_hostinger_config()

    if not config['user'] or not config['password']:
        return {
            'success': False,
            'message': 'Hostinger email credentials (username & password) are not configured.'
        }

    imap_host = getattr(db_config, 'imap_host', 'imap.hostinger.com') or 'imap.hostinger.com'
    imap_port = int(getattr(db_config, 'imap_port', 993) or 993)
    use_ssl = getattr(db_config, 'use_imap_ssl', True)
    user_email = config['user']
    password = config['password']

    mail = None
    try:
        if use_ssl or imap_port == 993:
            mail = imaplib.IMAP4_SSL(imap_host, imap_port, timeout=15)
        else:
            mail = imaplib.IMAP4(imap_host, imap_port, timeout=15)

        mail.login(user_email, password)
        status, _ = mail.select(folder)
        if status != 'OK':
            return {
                'success': False,
                'message': f"Could not open mailbox folder '{folder}'."
            }

        # Search all messages in folder
        status, search_data = mail.search(None, 'ALL')
        if status != 'OK' or not search_data or not search_data[0]:
            return {
                'success': True,
                'synced_new': 0,
                'total_inbox': 0,
                'message': 'Mailbox is empty.'
            }

        msg_ids = search_data[0].split()
        total_inbox = len(msg_ids)

        # Slice to fetch only the newest `limit` messages
        fetch_ids = msg_ids[-limit:] if len(msg_ids) > limit else msg_ids
        # Process from newest to oldest
        fetch_ids = list(reversed(fetch_ids))

        existing_ids = set(ReceivedEmail.objects.values_list('message_id', flat=True))
        new_count = 0
        new_messages = []

        for msg_id_bytes in fetch_ids:
            msg_id_str = msg_id_bytes.decode()

            # Quick check: fetch only headers first to see if message_id already exists in DB
            try:
                hdr_status, hdr_data = mail.fetch(msg_id_bytes, '(BODY.PEEK[HEADER.FIELDS (MESSAGE-ID FROM SUBJECT DATE)])')
                if hdr_status == 'OK' and hdr_data and isinstance(hdr_data[0], tuple):
                    hdr_msg = email.message_from_bytes(hdr_data[0][1])
                    quick_msg_id = hdr_msg.get('Message-ID', '').strip()
                    if quick_msg_id and quick_msg_id in existing_ids:
                        continue
            except Exception:
                pass
            
            # Fetch full message (PEEK keeps the message unread on the Hostinger server)
            res_status, msg_data = mail.fetch(msg_id_bytes, '(BODY.PEEK[])')
            if res_status != 'OK' or not msg_data:
                continue

            raw_email = None
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    raw_email = response_part[1]
                    break

            if not raw_email:
                continue

            msg = email.message_from_bytes(raw_email)

            # Parse headers
            message_id_header = msg.get('Message-ID', '').strip()
            raw_from = msg.get('From', '')
            raw_to = msg.get('To', '')
            raw_subject = msg.get('Subject', '')
            raw_date = msg.get('Date', '')

            subject = decode_mime_string(raw_subject) or "(No Subject)"
            sender_name, sender_email = email.utils.parseaddr(raw_from)
            sender_name = decode_mime_string(sender_name)
            if not sender_email and raw_from:
                sender_email = raw_from

            recipient = decode_mime_string(raw_to)
            received_at = parse_email_date(raw_date)

            # Deterministic unique ID fallback
            if not message_id_header:
                fingerprint = f"{sender_email}-{subject}-{raw_date}"
                message_id_header = f"auto-{hashlib.sha256(fingerprint.encode()).hexdigest()[:24]}@hostinger"

            # Check if already synced
            if message_id_header in existing_ids or ReceivedEmail.objects.filter(message_id=message_id_header).exists():
                existing_ids.add(message_id_header)
                continue

            body_text, body_html, attachment_names = extract_body_and_attachments(msg)

            # Generate snippet for preview list
            import re
            snippet_source = body_text or body_html or ""
            clean_snippet = re.sub(r'\[image:[^\]]*\]', '', snippet_source, flags=re.IGNORECASE)
            snippet = " ".join(clean_snippet.split())[:260]

            new_obj = ReceivedEmail.objects.create(
                message_id=message_id_header,
                uid=msg_id_str,
                sender_name=sender_name or sender_email,
                sender_email=sender_email.lower(),
                recipient=recipient,
                subject=subject,
                snippet=snippet,
                body_text=body_text,
                body_html=body_html,
                has_attachment=bool(attachment_names),
                attachment_names=", ".join(attachment_names),
                folder=folder,
                received_at=received_at,
                is_read=False
            )
            existing_ids.add(message_id_header)
            new_count += 1
            new_messages.append({
                'id': new_obj.id,
                'sender_name': new_obj.sender_name,
                'sender_email': new_obj.sender_email,
                'subject': new_obj.subject,
                'snippet': (new_obj.snippet or '')[:100],
            })

        unread_count = ReceivedEmail.objects.filter(is_read=False).count()

        return {
            'success': True,
            'synced_new': new_count,
            'total_inbox': total_inbox,
            'unread_count': unread_count,
            'new_messages': new_messages,
            'message': f"Synchronized {new_count} new messages from Hostinger Inbox."
        }

    except imaplib.IMAP4.error as e:
        return {
            'success': False,
            'message': f"Hostinger IMAP Authentication Error: {str(e)}"
        }
    except Exception as e:
        return {
            'success': False,
            'message': f"Hostinger IMAP Connection Failed: {str(e)}"
        }
    finally:
        if mail:
            try:
                mail.close()
            except Exception:
                pass
            try:
                mail.logout()
            except Exception:
                pass
