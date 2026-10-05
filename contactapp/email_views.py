from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Q
from .email_service import send_hostinger_email, test_hostinger_smtp_connection, get_hostinger_config
from .imap_service import sync_hostinger_inbox
from .models import SentEmailLog, HostingerEmailSettings, ReceivedEmail
from customers.models import Customer


@staff_member_required
def inbox_page(request):
    """
    Renders the dedicated Hostinger Webmail Inbox in the Admin Dashboard.
    """
    admin_context = admin.site.each_context(request)
    config = get_hostinger_config()
    is_ready = bool(config['user'] and config['password'])

    # Search and Filter parameters
    q = request.GET.get('q', '').strip()
    active_filter = request.GET.get('filter', 'all').strip()

    emails = ReceivedEmail.objects.all()

    if q:
        emails = emails.filter(
            Q(sender_name__icontains=q) |
            Q(sender_email__icontains=q) |
            Q(subject__icontains=q) |
            Q(snippet__icontains=q)
        )

    if active_filter == 'unread':
        emails = emails.filter(is_read=False)
    elif active_filter == 'attachment':
        emails = emails.filter(has_attachment=True)

    unread_count = ReceivedEmail.objects.filter(is_read=False).count()
    total_count = ReceivedEmail.objects.count()

    # Pre-select first email if available
    first_email = emails.first() if emails.exists() else None

    context = {
        **admin_context,
        'title': 'Hostinger Inbox (Webmail)',
        'subtitle': 'Incoming correspondence received on sales@tjropenet.com',
        'config': config,
        'is_ready': is_ready,
        'emails': emails[:60],
        'first_email': first_email,
        'unread_count': unread_count,
        'total_count': total_count,
        'search_query': q,
        'active_filter': active_filter,
    }
    return render(request, 'admin/email_inbox.html', context)


@staff_member_required
@require_POST
def sync_inbox_ajax(request):
    """
    Triggered via AJAX button to pull fresh emails from Hostinger IMAP.
    """
    result = sync_hostinger_inbox(limit=40)
    status_code = 200 if result.get('success') else 400
    return JsonResponse(result, status=status_code)


@staff_member_required
@require_GET
def get_email_detail_ajax(request, email_id):
    """
    Returns full email detail payload and marks the message as read.
    """
    email_obj = get_object_or_404(ReceivedEmail, id=email_id)
    if not email_obj.is_read:
        email_obj.is_read = True
        email_obj.save(update_fields=['is_read'])

    unread_count = ReceivedEmail.objects.filter(is_read=False).count()

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
        'unread_count': unread_count,
    })


@staff_member_required
@require_POST
def toggle_email_read_ajax(request, email_id):
    """
    Toggles read / unread status for a received email.
    """
    email_obj = get_object_or_404(ReceivedEmail, id=email_id)
    email_obj.is_read = not email_obj.is_read
    email_obj.save(update_fields=['is_read'])
    unread_count = ReceivedEmail.objects.filter(is_read=False).count()
    return JsonResponse({'success': True, 'is_read': email_obj.is_read, 'unread_count': unread_count})


@staff_member_required
@require_GET
def get_email_notifications_ajax(request):
    """
    Returns unread incoming email count and recent unread email previews
    for the top navbar notification bell and sidebar badge.
    Automatically checks Hostinger IMAP if ?sync=1 or every 15s in background.
    """
    check_sync = request.GET.get('sync', '0') == '1'
    synced_new = 0
    new_messages = []

    from django.core.cache import cache
    import time
    last_sync_time = cache.get('hostinger_last_imap_sync_ts', 0)
    now_ts = time.time()

    # Auto-sync if explicitly requested or at least 15s elapsed since last check
    if check_sync or (now_ts - last_sync_time >= 15):
        cache.set('hostinger_last_imap_sync_ts', now_ts, timeout=60)
        try:
            sync_res = sync_hostinger_inbox(limit=15)
            if sync_res.get('success'):
                synced_new = sync_res.get('synced_new', 0)
                new_messages = sync_res.get('new_messages', [])
        except Exception:
            pass

    unread_count = ReceivedEmail.objects.filter(is_read=False).count()
    recent_unread = list(
        ReceivedEmail.objects.filter(is_read=False)
        .order_by('-received_at')[:6]
    )

    from django.utils.timesince import timesince
    formatted_items = []
    for item in recent_unread:
        formatted_items.append({
            'id': item.id,
            'sender_name': item.sender_name or item.sender_email,
            'sender_email': item.sender_email,
            'subject': item.subject or '(No Subject)',
            'snippet': (item.snippet or '')[:90],
            'time_ago': timesince(item.received_at) + ' ago',
            'has_attachment': item.has_attachment,
        })

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
    Renders the dedicated Hostinger Email Composer & Hub page in the Admin Dashboard.
    """
    admin_context = admin.site.each_context(request)
    config = get_hostinger_config()
    is_ready = bool(config['user'] and config['password'])

    initial_to = request.GET.get('to', '').strip()
    initial_subject = request.GET.get('subject', '').strip()

    recent_customers = Customer.objects.exclude(email__isnull=True).exclude(email='').order_by('-created_at')[:20]
    recent_sent = SentEmailLog.objects.all().order_by('-sent_at')[:10]
    recent_inbox = ReceivedEmail.objects.all()[:6]
    unread_inbox_count = ReceivedEmail.objects.filter(is_read=False).count()

    context = {
        **admin_context,
        'title': 'Hostinger Email Center',
        'subtitle': 'Compose and send emails directly through your Hostinger SMTP account',
        'config': config,
        'is_ready': is_ready,
        'initial_to': initial_to,
        'initial_subject': initial_subject,
        'recent_customers': recent_customers,
        'recent_sent': recent_sent,
        'recent_inbox': recent_inbox,
        'unread_inbox_count': unread_inbox_count,
    }
    return render(request, 'admin/email_compose.html', context)



@staff_member_required
@require_POST
def send_dashboard_email_ajax(request):
    """
    Handles AJAX email composition and delivery via Hostinger SMTP.
    """
    to_email = request.POST.get('to', '').strip()
    cc_email = request.POST.get('cc', '').strip()
    bcc_email = request.POST.get('bcc', '').strip()
    subject = request.POST.get('subject', '').strip()
    message = request.POST.get('message', '').strip()
    attachment = request.FILES.get('attachment')

    if not to_email:
        return JsonResponse({'success': False, 'message': 'Please provide at least one recipient email address.'}, status=400)

    if not subject:
        return JsonResponse({'success': False, 'message': 'Email subject cannot be blank.'}, status=400)

    if not message:
        return JsonResponse({'success': False, 'message': 'Email body message cannot be blank.'}, status=400)

    success, result_message = send_hostinger_email(
        recipient=to_email,
        subject=subject,
        message=message,
        cc=cc_email,
        bcc=bcc_email,
        attachment=attachment,
        user=request.user
    )

    if success:
        return JsonResponse({'success': True, 'message': result_message})
    else:
        return JsonResponse({'success': False, 'message': result_message}, status=400)


@staff_member_required
@require_POST
def test_hostinger_connection_ajax(request):
    """
    Tests SMTP connection handshake with Hostinger servers.
    """
    success, message = test_hostinger_smtp_connection()
    status_code = 200 if success else 400
    return JsonResponse({'success': success, 'message': message}, status=status_code)


@staff_member_required
@require_GET
def get_hostinger_status_ajax(request):
    """
    Returns current active Hostinger configuration info for the compose modal.
    """
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
