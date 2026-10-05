from django.urls import path
from . import email_views

app_name = 'hostinger_mail'

urlpatterns = [
    path('', email_views.inbox_page, name='inbox_root'),
    path('inbox/', email_views.inbox_page, name='inbox'),
    path('inbox/sync/', email_views.sync_inbox_ajax, name='sync_inbox'),
    path('inbox/<int:email_id>/', email_views.get_email_detail_ajax, name='email_detail'),
    path('inbox/<int:email_id>/toggle-read/', email_views.toggle_email_read_ajax, name='toggle_read'),
    path('compose/', email_views.email_compose_page, name='compose_page'),
    path('send/', email_views.send_dashboard_email_ajax, name='send_email'),
    path('test-connection/', email_views.test_hostinger_connection_ajax, name='test_connection'),
    path('status/', email_views.get_hostinger_status_ajax, name='status'),
    path('notifications/', email_views.get_email_notifications_ajax, name='notifications'),
]
