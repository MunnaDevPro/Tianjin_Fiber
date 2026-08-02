from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .data import PRODUCTS, VALUES, FAQS, SERVICES

from .models import Category, Product

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetching a few featured products for home page, or just all of them
        context['products'] = Product.objects.all()[:8]
        context['values'] = VALUES
        context['faqs'] = FAQS
        return context

from django.views.generic import DetailView

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'core/category_detail.html'
    context_object_name = 'category'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'core/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch related products from same category, excluding the current product
        context['related_products'] = Product.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        return context
class AboutView(TemplateView):
    template_name = 'core/about.html'

class CertificatesView(TemplateView):
    template_name = 'core/certificates.html'

class ServicesView(TemplateView):
    template_name = 'core/services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = SERVICES
        return context

class ContactView(View):
    def get(self, request):
        return render(request, 'core/contact.html', {'form': ContactForm()})
        
    def post(self, request):
        import json
        try:
            data = json.loads(request.body)
            form = ContactForm(data)
        except json.JSONDecodeError:
            # Fallback if form-data is used instead of JSON
            form = ContactForm(request.POST)

        if form.is_valid():
            contact_msg = form.save()
            
            # Attempt to send email
            try:
                send_mail(
                    subject=f"New Contact: {contact_msg.subject}",
                    message=f"Name: {contact_msg.name}\nEmail: {contact_msg.email}\nPhone: {contact_msg.phone}\n\nMessage:\n{contact_msg.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL], # Send to self
                    fail_silently=True, # Prevent crashes if email backend isn't setup
                )
            except Exception:
                pass # Email fail shouldn't break UI
                
            return JsonResponse({'success': True, 'message': 'Thank you! Your message has been sent.'})
        
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

