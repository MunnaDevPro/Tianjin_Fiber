import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from navigation.models import Navbar, Footer, SocialLink
from home.models import HomeHero, HomeFactory, HomeValues, HomeValueItem, HomeMission, HomeFactoryFeature
from about.models import AboutHeader, AboutStory, AboutStoryPoint, AboutExcellence, AboutExcellenceCard, TeamMember, Testimonial
from services.models import ServicesHeader, ServiceItem, ProcessSection, ProcessStep, ServicesCTA
from certificates.models import CertificatesHeader, Certificate, CertificatesCTA
from factory.models import FactoryHeader, FactoryGallerySection, FactoryVideoSection, FactoryCTA
from contactapp.models import ContactPageSettings
from products.models import Category

def run():
    print("Seeding Navigation...")
    Navbar.objects.get_or_create(id=1, defaults={'cta_text': 'Get Quote', 'cta_link': '/contact/'})
    Footer.objects.get_or_create(id=1, defaults={'about_text': 'Tianjin Fiber Net is a leading manufacturer of industrial netting.', 'copyright_text': '© 2026 Tianjin Fiber Net. All Rights Reserved.', 'email': 'info@tianjinfibernet.com', 'phone': '+86 123 4567 8900'})
    
    print("Seeding Home...")
    HomeHero.objects.get_or_create(id=1, defaults={'title_black': 'Uncompromising', 'title_magenta': 'Quality.', 'title_gold': 'Protect.', 'title_prefix': 'Engineered to'})
    HomeFactory.objects.get_or_create(id=1, defaults={'title': 'State-of-the-art Production Facilities', 'description': 'Over 50,000 sqm of advanced production.'})
    HomeValues.objects.get_or_create(id=1, defaults={'title': 'Our Core Values', 'description': 'What drives us forward.'})
    HomeMission.objects.get_or_create(id=1, defaults={'title': 'Our Global Mission', 'description': 'Delivering safety and durability to every industry.'})
    
    print("Seeding About...")
    AboutHeader.objects.get_or_create(id=1, defaults={'title': 'Building the Future of Global Manufacturing', 'subtitle': 'Decades of experience.'})
    AboutStory.objects.get_or_create(id=1, defaults={'title': 'A Legacy of Strength', 'description': 'Our journey began with a vision to redefine quality.'})
    AboutExcellence.objects.get_or_create(id=1, defaults={'title': 'Engineering Excellence at Scale', 'description': 'We pride ourselves on technical perfection.'})
    
    print("Seeding Services...")
    ServicesHeader.objects.get_or_create(id=1, defaults={'title': 'Manufacturing Services', 'subtitle': 'Comprehensive solutions tailored to your needs.'})
    ProcessSection.objects.get_or_create(id=1, defaults={'title': 'Our Comprehensive Manufacturing', 'subtitle': 'Step by step process.'})
    ServicesCTA.objects.get_or_create(id=1, defaults={'title': 'Need a Custom Specification?', 'description': 'Our engineering team is ready.'})
    
    print("Seeding Certificates...")
    CertificatesHeader.objects.get_or_create(id=1, defaults={'title': 'Certified Excellence', 'subtitle': 'Explore our portfolio.'})
    CertificatesCTA.objects.get_or_create(id=1, defaults={'title': 'Need Details About Our Standards?', 'description': 'Request documents here.'})
    
    print("Seeding Factory...")
    FactoryHeader.objects.get_or_create(id=1, defaults={'title': 'State-of-the-Art Manufacturing', 'subtitle': 'Explore our facilities.'})
    FactoryGallerySection.objects.get_or_create(id=1, defaults={'title': 'Explore Our Factory Gallery', 'description': 'Take a visual tour.'})
    FactoryVideoSection.objects.get_or_create(id=1, defaults={'title': 'Watch Our Manufacturing Process', 'description': 'See production in action.'})
    FactoryCTA.objects.get_or_create(id=1, defaults={'title': 'Interested in a Facility Tour?', 'description': 'Schedule one today.'})
    
    print("Seeding Contact...")
    ContactPageSettings.objects.get_or_create(id=1, defaults={'title': 'Contact Us', 'subtitle': 'Get in touch with our team.'})
    
    print("Seeding Default Category...")
    Category.objects.get_or_create(name='Industrial Nets', defaults={'slug': 'industrial-nets'})
    
    print("Done seeding!")

if __name__ == '__main__':
    run()
