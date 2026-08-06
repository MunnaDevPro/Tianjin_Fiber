import os
import django
import urllib.request
import tempfile
import io
from PIL import Image
from django.core.files import File
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from services.models import ServicesHeader, ServiceItem, ProcessSection, ProcessStep, ServicesCTA

def generate_fallback_image(filename):
    print(f"Generating fallback image for {filename}...")
    img = Image.new('RGB', (800, 600), color=(26, 70, 116))
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    return ContentFile(buffer.getvalue(), name=filename)

def download_image(url, filename):
    try:
        print(f"Downloading {filename} from {url}...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = urllib.request.Request(url, headers=headers)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        with urllib.request.urlopen(req, timeout=15) as response:
            temp_file.write(response.read())
        temp_file.close()
        return File(open(temp_file.name, 'rb'), name=filename)
    except Exception as e:
        print(f"Failed to download {filename}: {e}. Using Pillow fallback.")
        return generate_fallback_image(filename)

def run():
    print("Clearing old services data...")
    ServiceItem.objects.all().delete()
    ProcessStep.objects.all().delete()
    ProcessSection.objects.all().delete()
    ServicesHeader.objects.all().delete()
    ServicesCTA.objects.all().delete()

    print("Seeding Services Header...")
    header, _ = ServicesHeader.objects.get_or_create(id=1, defaults={
        'title': 'Manufacturing Services',
        'subtitle': 'Comprehensive solutions tailored to your industrial specifications, backed by decades of manufacturing excellence.'
    })
    # Set header background image
    header_img = download_image('https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=1920', 'services_header.jpg')
    header.bg_image.save('services_header.webp', header_img, save=True)

    print("Seeding Service Items...")
    services_list = [
        {
            'title': 'Custom Agricultural Nets',
            'description': 'High-durability shading and bird protection nets designed specifically for modern agriculture. Engineered to withstand harsh UV exposure and extreme weather conditions.',
            'url': 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&q=80&w=1000'
        },
        {
            'title': 'Industrial Safety Nets',
            'description': 'Heavy-duty fall protection and cargo securing nets. Certified to international safety standards, providing reliable performance in construction and logistics.',
            'url': 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&q=80&w=1000'
        },
        {
            'title': 'Marine & Heavy Duty Ropes',
            'description': 'Premium natural fiber and synthetic ropes engineered for high-stress marine docking, industrial rigging, and cargo tie-downs.',
            'url': 'https://images.unsplash.com/photo-1553531384-cc64ac80f931?auto=format&fit=crop&q=80&w=1000'
        }
    ]

    for index, s in enumerate(services_list):
        item = ServiceItem(
            title=s['title'],
            description=s['description'],
            order=index,
            is_active=True
        )
        img_file = download_image(s['url'], f"service_{index}.jpg")
        item.image.save(f"service_{index}.webp", img_file, save=True)
        print(f"Successfully seeded service item: {s['title']}")

    print("Seeding Process Section...")
    process_sec, _ = ProcessSection.objects.get_or_create(id=1, defaults={
        'title': 'Our Comprehensive Manufacturing',
        'subtitle': 'We follow a rigorous methodology to ensure every product meets the highest standards of quality, durability, and performance.'
    })

    print("Seeding Process Steps...")
    steps_list = [
        {
            'icon': 'users',
            'title': 'Consultation',
            'description': 'Understanding your specific fiber and netting requirements for optimal solutions.'
        },
        {
            'icon': 'settings',
            'title': 'Engineering',
            'description': 'Designing custom specifications tailored to your project\'s unique tensile needs.'
        },
        {
            'icon': 'factory',
            'title': 'Production',
            'description': 'State-of-the-art manufacturing using premium materials and advanced weaving techniques.'
        },
        {
            'icon': 'shield-check',
            'title': 'Quality Control',
            'description': 'Rigorous testing procedures to ensure maximum durability, strength, and safety.'
        },
        {
            'icon': 'truck',
            'title': 'Delivery',
            'description': 'Efficient logistics and careful packaging for secure and timely global shipping.'
        },
        {
            'icon': 'headphones',
            'title': 'Support',
            'description': 'Dedicated after-sales service providing maintenance guidance and continuous support.'
        }
    ]

    for index, step in enumerate(steps_list):
        ProcessStep.objects.create(
            process=process_sec,
            icon=step['icon'],
            title=step['title'],
            description=step['description'],
            order=index,
            is_active=True
        )
        print(f"Successfully seeded process step: {step['title']}")

    print("Seeding Services CTA...")
    ServicesCTA.objects.get_or_create(id=1, defaults={
        'title': 'Need a Custom Specification?',
        'description': 'Our engineering team can develop customized rope and netting solutions to meet your exact tensile strength and environmental requirements.',
        'btn_text': 'Contact Engineering',
        'btn_link': '/contact/'
    })

    print("Services data seeding completed successfully!")

if __name__ == '__main__':
    run()
