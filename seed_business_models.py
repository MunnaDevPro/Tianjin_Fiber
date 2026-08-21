import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from services.models import BusinessModelSection, BusinessModelItem

def seed_business_models():
    # Create or update section
    section, created = BusinessModelSection.objects.get_or_create(
        id=1,
        defaults={
            'title': 'OEM & ODM Solutions',
            'subtitle': 'Whether you have your own unique product design or want to leverage our existing high-quality manufacturing lines under your own brand, we offer flexible models to suit your business needs.'
        }
    )
    
    # Clear existing to prevent duplicates during testing
    BusinessModelItem.objects.all().delete()
    
    # Create OEM
    BusinessModelItem.objects.create(
        section=section,
        title="OEM",
        full_name="Original Equipment Manufacturer",
        quote="Your Design, Our Manufacturing",
        description="You provide the exact design, specifications, materials, and colors. We manufacture the product strictly according to your requirements. Perfect for businesses with custom product innovations.",
        icon="pen-tool",
        features="Design: Yours\nManufacturing: Ours\nCustomization: Highly Customized",
        color_theme="blue",
        order=1
    )
    
    # Create ODM
    BusinessModelItem.objects.create(
        section=section,
        title="ODM",
        full_name="Original Design Manufacturer",
        quote="Our Design, Your Brand",
        description="Choose from our existing catalog of proven, high-quality designs and sell them under your own brand name and logo. The fastest way to bring premium products to market.",
        icon="tag",
        features="Design: Ours (Ready-made)\nManufacturing: Ours\nBrand: Yours",
        color_theme="magenta",
        order=2
    )
    
    print("Business models seeded successfully!")

if __name__ == "__main__":
    seed_business_models()
