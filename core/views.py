from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.views import View
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from products.models import Category, Product
from home.models import HomeHero, HomeFactory, HomeValues, HomeMission
from about.models import AboutHeader, AboutStory, AboutExcellence, TeamMember, Testimonial
from services.models import ServicesHeader, ServiceItem, ProcessSection, ServicesCTA
from certificates.models import CertificatesHeader, Certificate, CertificatesCTA
from factory.models import FactoryHeader, FactoryGallerySection, FactoryVideoSection, FactoryCTA
from contactapp.models import ContactPageSettings

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero'] = HomeHero.objects.first()
        context['factory'] = HomeFactory.objects.first()
        context['values_section'] = HomeValues.objects.first()
        context['mission'] = HomeMission.objects.first()
        
        # We need products for the carousel, let's just get active ones
        context['products'] = Product.objects.filter(is_active=True)
        return context

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
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id)[:4]
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = AboutHeader.objects.first()
        context['story'] = AboutStory.objects.first()
        context['excellence'] = AboutExcellence.objects.first()
        context['team'] = TeamMember.objects.filter(is_active=True)
        context['testimonials'] = Testimonial.objects.filter(is_active=True)
        return context

class CertificatesView(TemplateView):
    template_name = 'core/certificates.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = CertificatesHeader.objects.first()
        context['certificates'] = Certificate.objects.filter(is_active=True)
        context['cta'] = CertificatesCTA.objects.first()
        return context

class ServicesView(TemplateView):
    template_name = 'core/services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = ServicesHeader.objects.first()
        context['services'] = ServiceItem.objects.filter(is_active=True)
        context['process'] = ProcessSection.objects.first()
        context['cta'] = ServicesCTA.objects.first()
        return context

class FactoryView(TemplateView):
    template_name = 'core/factory.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = FactoryHeader.objects.first()
        context['gallery'] = FactoryGallerySection.objects.first()
        if context['gallery']:
            context['images'] = context['gallery'].images.filter(is_active=True)
        else:
            context['images'] = []
            
        context['videos_section'] = FactoryVideoSection.objects.first()
        if context['videos_section']:
            context['videos'] = context['videos_section'].videos.filter(is_active=True)
        else:
            context['videos'] = []
            
        context['cta'] = FactoryCTA.objects.first()
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
            form = ContactForm(request.POST)

        if form.is_valid():
            contact_msg = form.save()
            try:
                send_mail(
                    subject=f"New Contact: {contact_msg.subject}",
                    message=f"Name: {contact_msg.name}\nEmail: {contact_msg.email}\nPhone: {contact_msg.phone}\n\nMessage:\n{contact_msg.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            return JsonResponse({'success': True, 'message': 'Thank you! Your message has been sent.'})
        
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
