from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('add-ajax/', views.add_customer_ajax, name='add_customer_ajax'),
]
