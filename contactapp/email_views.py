from email.utils import parseaddr

from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.timesince import timesince
from django.views.decorators.http import require_POST, require_GET

from customers.models import Customer
from .email_service import send_hostinger_email, test_hostinger_smtp_connection, get_hostinger_config
from .imap_service import sync_hostinger_inbox
from .models import SentEmailLog, ReceivedEmail

MAX_ATTACHMENT_TOTAL = 25 * 1024 * 1024  # 25 MB (Hostinger limit)
PAGE_SIZE = 50


def _mail_context(request, **extra):
    """Shared context for all mail pages (admin chrome + mailbox status + folder counts)."""
    config = get_hostinger_config()
    context = {
        **admin.site.each_context(request),
        'config': config,
        'is_ready': bool(config['user'] and config['password']),
        'unread_count': ReceivedEmail.objects.filter(is_read=False).count(),
        'inbox_count': ReceivedEmail.objects.count(),
        'sent_count': SentEmailLog.objects.count(),
    }
    context.update(extra)
    return context


def _invalid_addresses(*fields):
    """Returns addresses that are not valid emails (accepts 'Name <email>' format)."""
    invalid = []
    for field in fields:
        for raw in (field or '').replace(';', ',').split(','):
            raw = raw.strip()
            if not raw:
                continue
            addr = parseaddr(raw)[1]
            try:
                validate_email(addr)
            except ValidationError:
                invalid.append(raw)
    return invalid


@staff_member_required
def inbox_page(request):
    """
    Mailbox page with two folders: Inbox (received via IMAP) and Sent (sent via SMTP).
    """
    folder = request.GET.get('folder', 'inbox')
    if folder not in ('inbox', 'sent'):
        folder = 'inbox'
    q = request.GET.get('q', '').strip()
    active_filter = request.GET.get('filter', 'all').strip()

    if folder == 'sent':
        items = SentEmailLog.objects.all()
        if q:
            items = items.filter(
                Q(recipient__icontains=q) | Q(cc__icontains=q) |
                Q(subject__icontains=q) | Q(message__icontains=q)
            )
        if active_filter == 'failed':
            items = items.filter(status='Failed')
        elif active_filter == 'attachment':
            items = items.exclude(attachment_name='')
        else:
            active_filter = 'all'
    else:
        items = ReceivedEmail.objects.all()
        if q:
            items = items.filter(
                Q(sender_name__icontains=q) | Q(sender_email__icontains=q) |
                Q(subject__icontains=q) | Q(snippet__icontains=q)
            )
        if active_filter == 'unread':
            items = items.filter(is_read=False)
        elif active_filter == 'attachment':
            items = items.filter(has_attachment=True)
        else:
            active_filter = 'all'

    page_obj = Paginator(items, PAGE_SIZE).get_page(request.GET.get('page'))

    context = _mail_context(
        request,
        title='Sent' if folder == 'sent' else 'Inbox',
        folder=folder,
        page_obj=page_obj,
        items=page_obj.object_list,
        search_query=q,
        active_filter=active_filter,
        now_ymd=timezone.localdate().strftime('%Y%m%d'),
    )
    return render(request, 'admin/email_inbox.html', context)


@staff_member_required
@require_POST
def sync_inbox_ajax(request):
    """Pulls fresh emails from Hostinger IMAP."""
    result = sync_hostinger_inbox(limit=40)
    return JsonResponse(result, status=200 if result.get('success') else 400)


@staff_member_required
@require_GET
def get_email_detail_ajax(request, email_id):
    """Returns full received-email payload and marks the message as read."""
    email_obj = get_object_or_404(ReceivedEmail, id=email_id)
    if not email_obj.is_read:
        email_obj.is_read = True
        email_obj.save(update_fields=['is_read'])

    return JsonResponse({
        'success': True,
        'id': email_obj.id,
        'sender_name': email_obj.sender_name or email_obj.sender_email,
        'sender_email': email_obj.sender_email,
        'recipient': email_obj.recipient,
        'subject': email_obj.subject or '(No Subject)',
        'received_at': email_obj.received_at.strftime('%b %d, %Y, %I:%M %p'),
        'body_html': email_obj.body_html,
        'body_text': email_obj.body_text,
        'has_attachment': email_obj.has_attachment,
        'attachment_names': email_obj.attachment_names,
        'is_read': email_obj.is_read,
        'unread_count': ReceivedEmail.objects.filter(is_read=False).count(),
    })


@staff_member_required
@require_GET
def get_sent_detail_ajax(request, log_id):
    """Returns full payload of a sent email."""
    log = get_object_or_404(SentEmailLog, id=log_id)
    return JsonResponse({
        'success': True,
        'id': log.id,
        'recipient': log.recipient,
        'cc': log.cc,
        'bcc': log.bcc,
        'subject': log.subject or '(No Subject)',
        'message': log.message,
        'attachment_name': log.attachment_name,
        'status': log.status,
        'error_message': log.error_message or '',
        'sent_by': log.sent_by.get_username() if log.sent_by else '',
        'sent_at': log.sent_at.strftime('%b %d, %Y, %I:%M %p'),
    })


@staff_member_required
@require_POST
def toggle_email_read_ajax(request, email_id):
    """Toggles read / unread status for a received email."""
    email_obj = get_object_or_404(ReceivedEmail, id=email_id)
    email_obj.is_read = not email_obj.is_read
    email_obj.save(update_fields=['is_read'])
    unread_count = ReceivedEmail.objects.filter(is_read=False).count()
    return JsonResponse({'success': True, 'is_read': email_obj.is_read, 'unread_count': unread_count})


@staff_member_required
@require_GET
def get_email_notifications_ajax(request):
    """
    Returns unread incoming email count and recent unread previews
    for the navbar bell and sidebar badge.
    Checks Hostinger IMAP if ?sync=1 or at most every 15s.
    """
    check_sync = request.GET.get('sync', '0') == '1'
    synced_new = 0
    new_messages = []

    from django.core.cache import cache
    import time
    last_sync_time = cache.get('hostinger_last_imap_sync_ts', 0)
    now_ts = time.time()

    if check_sync or (now_ts - last_sync_time >= 15):
        cache.set('hostinger_last_imap_sync_ts', now_ts, timeout=60)
        try:
            sync_res = sync_hostinger_inbox(limit=15)
            if sync_res.get('success'):
                synced_new = sync_res.get('synced_new', 0)
                new_messages = sync_res.get('new_messages', [])
        except Exception:
            pass

    unread_qs = ReceivedEmail.objects.filter(is_read=False)
    unread_count = unread_qs.count()
    formatted_items = [{
        'id': item.id,
        'sender_name': item.sender_name or item.sender_email,
        'sender_email': item.sender_email,
        'subject': item.subject or '(No Subject)',
        'snippet': (item.snippet or '')[:90],
        'time_ago': timesince(item.received_at) + ' ago',
        'has_attachment': item.has_attachment,
    } for item in unread_qs.order_by('-received_at')[:6]]

    return JsonResponse({
        'success': True,
        'unread_count': unread_count,
        'synced_new': synced_new,
        'new_messages': new_messages,
        'notifications': formatted_items,
    })


@staff_member_required
def email_compose_page(request):
    """
    Compose page. Supports:
      ?to=&subject=          prefill
      ?reply=<received id>   reply to a received email (threaded, quoted)
      ?forward=<received id> forward a received email
    """
    initial_to = request.GET.get('to', '').strip()
    initial_subject = request.GET.get('subject', '').strip()
    initial_body = ''
    in_reply_to = ''
    mode = 'new'

    reply_id = request.GET.get('reply')
    forward_id = request.GET.get('forward')
    source_id = reply_id or forward_id
    if source_id and str(source_id).isdigit():
        src = ReceivedEmail.objects.filter(id=source_id).first()
        if src:
            subject = src.subject or ''
            body = src.body_text
            if not body and src.body_html:
                body = strip_tags(src.body_html).strip()
            if not body:
                body = src.snippet or ''
            date_str = src.received_at.strftime('%a, %b %d, %Y at %I:%M %p')
            sender = f"{src.sender_name} <{src.sender_email}>" if src.sender_name else src.sender_email
            if reply_id:
                mode = 'reply'
                initial_to = src.sender_email
                initial_subject = subject if subject.lower().startswith('re:') else f"Re: {subject}"
                quoted = '\n'.join(f"> {line}" for line in body.splitlines())
                initial_body = f"\n\n\nOn {date_str}, {sender} wrote:\n{quoted}"
                if not src.message_id.startswith('auto-'):
                    in_reply_to = src.message_id
            else:
                mode = 'forward'
                initial_subject = subject if subject.lower().startswith('fwd:') else f"Fwd: {subject}"
                initial_body = (
                    f"\n\n\n---------- Forwarded message ----------\n"
                    f"From: {sender}\nDate: {date_str}\nSubject: {subject}\nTo: {src.recipient}\n\n{body}"
                )

    recent_customers = Customer.objects.exclude(email__isnull=True).exclude(email='').order_by('-created_at')[:40]
    recent_inbox = ReceivedEmail.objects.order_by('-received_at')[:8]
    recent_sent = SentEmailLog.objects.order_by('-sent_at')[:8]
    unread_inbox_count = ReceivedEmail.objects.filter(is_read=False).count()

    context = _mail_context(
        request,
        title='Compose' if mode == 'new' else ('Reply' if mode == 'reply' else 'Forward'),
        folder='compose',
        mode=mode,
        initial_to=initial_to,
        initial_subject=initial_subject,
        initial_body=initial_body,
        in_reply_to=in_reply_to,
        recent_customers=recent_customers,
        recent_inbox=recent_inbox,
        recent_sent=recent_sent,
        unread_inbox_count=unread_inbox_count,
    )
    return render(request, 'admin/email_compose.html', context)


@staff_member_required
@require_POST
def send_dashboard_email_ajax(request):
    """Handles AJAX email composition and delivery via Hostinger SMTP."""
    to_email = request.POST.get('to', '').strip()
    cc_email = request.POST.get('cc', '').strip()
    bcc_email = request.POST.get('bcc', '').strip()
    subject = request.POST.get('subject', '').strip()
    message = request.POST.get('message', '').strip()
    in_reply_to = request.POST.get('in_reply_to', '').strip() or None

    # 'attachments' (multiple) from the compose page, 'attachment' (single) from other dashboard forms
    files = request.FILES.getlist('attachments') + request.FILES.getlist('attachment')

    if not to_email:
        return JsonResponse({'success': False, 'message': 'Please provide at least one recipient email address.'}, status=400)
    if not subject:
        return JsonResponse({'success': False, 'message': 'Email subject cannot be blank.'}, status=400)
    if not message:
        return JsonResponse({'success': False, 'message': 'Email body message cannot be blank.'}, status=400)
    invalid = _invalid_addresses(to_email, cc_email, bcc_email)
    if invalid:
        return JsonResponse({'success': False, 'message': f"Invalid email address: {', '.join(invalid)}"}, status=400)
    if sum(f.size for f in files) > MAX_ATTACHMENT_TOTAL:
        return JsonResponse({'success': False, 'message': 'Attachments exceed the 25 MB limit.'}, status=400)

    success, result_message = send_hostinger_email(
        recipient=to_email,
        subject=subject,
        message=message,
        cc=cc_email,
        bcc=bcc_email,
        attachments=files,
        user=request.user,
        in_reply_to=in_reply_to,
    )
    return JsonResponse({'success': success, 'message': result_message}, status=200 if success else 400)


@staff_member_required
@require_POST
def test_hostinger_connection_ajax(request):
    """Tests SMTP connection handshake with Hostinger servers."""
    success, message = test_hostinger_smtp_connection()
    return JsonResponse({'success': success, 'message': message}, status=200 if success else 400)


@staff_member_required
@require_GET
def get_hostinger_status_ajax(request):
    """Returns current Hostinger configuration info (used by the dashboard compose modal)."""
    config = get_hostinger_config()
    is_ready = bool(config['user'] and config['password'])
    return JsonResponse({
        'is_configured': is_ready,
        'sender_email': config['user'] if is_ready else 'Not Configured',
        'sender_name': config['sender_name'],
        'default_signature': config['signature'],
        'source': config['source'],
        'smtp_host': config['host'],
        'smtp_port': config['port'],
    })
