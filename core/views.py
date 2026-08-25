import random
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
        
        # Get all active products sorted by category with Sun Shade weighted more
        all_products = list(Product.objects.filter(is_active=True).select_related('category'))

        shade_products = [p for p in all_products if 'sun shade' in p.category.name.lower()]
        rope_products  = [p for p in all_products if 'rope' in p.category.name.lower() or 'twine' in p.category.name.lower()]
        hw_products    = [p for p in all_products if 'hardware' in p.category.name.lower() or 'ladder' in p.category.name.lower()]

        # Shuffle each category internally
        random.shuffle(shade_products)
        random.shuffle(rope_products)
        random.shuffle(hw_products)

        # Interleave: Sun Shade 2 → Rope 1 → Shade 2 → Hardware 1 → repeat
        # This gives Sun Shade ~50% presence without duplicating any product
        interleaved = []
        si, ri, hi = 0, 0, 0  # indices for shade, rope, hardware
        pattern = [2, 1, 2, 1]   # shade, rope, shade, hardware
        sources = [shade_products, rope_products, shade_products, hw_products]
        idxs    = [si, ri, si, hi]

        while si < len(shade_products) or ri < len(rope_products) or hi < len(hw_products):
            for take, src in zip(pattern, sources):
                if src is shade_products:
                    for _ in range(take):
                        if si < len(shade_products):
                            interleaved.append(shade_products[si]); si += 1
                elif src is rope_products:
                    for _ in range(take):
                        if ri < len(rope_products):
                            interleaved.append(rope_products[ri]); ri += 1
                else:
                    for _ in range(take):
                        if hi < len(hw_products):
                            interleaved.append(hw_products[hi]); hi += 1
            # Break if all exhausted
            if si >= len(shade_products) and ri >= len(rope_products) and hi >= len(hw_products):
                break

        context['products'] = interleaved
        return context

class CategoryDetailView(View):
    template_name = 'core/category_detail.html'

    def get(self, request, slug):
        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
        category = Category.objects.get(slug=slug)
        all_products = category.products.filter(is_active=True).order_by('order', 'name')
        paginator = Paginator(all_products, 20)  # 20 products per page
        page_number = request.GET.get('page', 1)
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {
            'category': category,
            'page_obj': page_obj,
            'paginator': paginator,
        })

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
        from services.models import BusinessModelSection
        context = super().get_context_data(**kwargs)
        context['header'] = ServicesHeader.objects.first()
        context['services'] = ServiceItem.objects.filter(is_active=True)
        context['process'] = ProcessSection.objects.first()
        context['cta'] = ServicesCTA.objects.first()
        context['business_models'] = BusinessModelSection.objects.first()
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
                from django.core.mail import EmailMultiAlternatives
                from django.template.loader import render_to_string
                import datetime

                recipient = getattr(settings, 'EMAIL_RECIPIENT', 'munnahowlader06@gmail.com')
                subject = f"New Contact/Quote: {contact_msg.subject}"
                
                context = {
                    'contact': contact_msg,
                    'current_year': datetime.datetime.now().year
                }
                
                html_content = render_to_string('core/emails/contact_email.html', context)
                text_content = f"Name: {contact_msg.name}\nEmail: {contact_msg.email}\nPhone: {contact_msg.phone}\nSubject: {contact_msg.subject}\n\nMessage:\n{contact_msg.message}"
                
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[recipient],
                )
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=False)
            except Exception as e:
                print(f"Error sending email: {e}")
            return JsonResponse({'success': True, 'message': 'Thank you! Your message has been sent.'})
        
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

def custom_page_not_found_view(request, exception=None):
    return render(request, '404.html', status=404)
