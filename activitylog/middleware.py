import requests
from django.utils import timezone
from .models import UserSession

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def parse_user_agent(ua_string):
    if not ua_string:
        return "Unknown Device", "Unknown Browser"
    
    os_name = "Unknown OS"
    if "Windows" in ua_string:
        os_name = "Windows"
    elif "Macintosh" in ua_string or "Mac OS X" in ua_string:
        os_name = "macOS"
    elif "iPhone" in ua_string:
        os_name = "iPhone"
    elif "iPad" in ua_string:
        os_name = "iPad"
    elif "Android" in ua_string:
        os_name = "Android"
    elif "Linux" in ua_string:
        os_name = "Linux"

    browser = "Unknown Browser"
    if "Edge" in ua_string or "Edg" in ua_string:
        browser = "Edge"
    elif "Chrome" in ua_string and "Safari" in ua_string:
        browser = "Chrome"
    elif "Safari" in ua_string and "Chrome" not in ua_string:
        browser = "Safari"
    elif "Firefox" in ua_string:
        browser = "Firefox"
    elif "Trident" in ua_string or "MSIE" in ua_string:
        browser = "Internet Explorer"
        
    return os_name, browser

def get_ip_location(ip):
    if ip in ('127.0.0.1', '::1') or ip.startswith('192.168.') or ip.startswith('10.'):
        return "Localhost / Development"
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                city = data.get('city', '')
                country = data.get('country', '')
                region = data.get('regionName', '')
                parts = [p for p in (city, region, country) if p]
                return ", ".join(parts) if parts else "Unknown Location"
    except Exception:
        pass
    return "Unknown Location"

class UserSessionTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Track session only for logged-in users after the request is processed
        if hasattr(request, 'user') and request.user.is_authenticated:
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key

            ip = get_client_ip(request)
            ua = request.META.get('HTTP_USER_AGENT', '')
            os_name, browser = parse_user_agent(ua)

            # Update or create the session tracking object
            session_log, created = UserSession.objects.get_or_create(
                session_key=session_key,
                defaults={
                    'user': request.user,
                    'ip_address': ip,
                    'user_agent': ua,
                    'device_info': os_name,
                    'browser_info': browser,
                    'location': get_ip_location(ip),
                    'is_active': True,
                }
            )

            if not created:
                # If session log exists, make sure it is marked active and update activity time
                session_log.is_active = True
                session_log.last_activity = timezone.now()
                session_log.save()

        return response
