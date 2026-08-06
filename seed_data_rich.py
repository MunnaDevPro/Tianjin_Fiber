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

from products.models import Category, Product
from about.models import TeamMember, Testimonial

# Helper function to generate valid solid image using Pillow
def generate_fallback_image(filename):
    print(f"Generating fallback image for {filename}...")
    img = Image.new('RGB', (800, 800), color=(26, 70, 116))  # Site professional blue color
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    return ContentFile(buffer.getvalue(), name=filename)

# Helper function to download image and return as django File
def download_image(url, filename):
    try:
        print(f"Downloading {filename} from {url}...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = urllib.request.Request(url, headers=headers)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        with urllib.request.urlopen(req, timeout=10) as response:
            temp_file.write(response.read())
        temp_file.close()
        return File(open(temp_file.name, 'rb'), name=filename)
    except Exception as e:
        print(f"Failed to download {filename}: {e}. Using Pillow fallback.")
        return generate_fallback_image(filename)

def run():
    print("Clearing old dummy data (Team, Testimonials, Categories, Products)...")
    TeamMember.objects.all().delete()
    Testimonial.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()

    print("Seeding Categories...")
    cat_data = [
        {
            'name': 'Industrial Nets',
            'slug': 'industrial-nets',
            'hero_text': 'Heavy-duty netting solutions for construction, safety, and logistics.',
            'url': 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&q=80&w=1200'
        },
        {
            'name': 'Agricultural Nets',
            'slug': 'agricultural-nets',
            'hero_text': 'Premium shade and protection netting designed for modern sustainable farming.',
            'url': 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&q=80&w=1200'
        },
        {
            'name': 'Marine & Industrial Ropes',
            'slug': 'marine-industrial-ropes',
            'hero_text': 'High-tensile natural and synthetic ropes engineered for extreme environments.',
            'url': 'https://images.unsplash.com/photo-1553531384-cc64ac80f931?auto=format&fit=crop&q=80&w=1200'
        }
    ]

    categories = {}
    for index, c in enumerate(cat_data):
        cat = Category(
            name=c['name'],
            slug=c['slug'],
            hero_text=c['hero_text'],
            order=index
        )
        img_file = download_image(c['url'], f"{c['slug']}.jpg")
        cat.hero_image.save(f"{c['slug']}.webp", img_file, save=True)
        categories[c['slug']] = cat
        print(f"Created Category: {cat.name}")

    print("Seeding Products...")
    prod_data = [
        {
            'category': 'industrial-nets',
            'name': 'Safety Fall Protection Netting',
            'slug': 'safety-fall-protection-netting',
            'description': '<p>High-grade polypropylene fall protection netting designed to secure high-elevation construction sites and industrial warehouses.</p>',
            'features': "High tensile strength\nUV stabilized material\nCertified safety borders\nAnti-fray weave",
            'url': 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&q=80&w=800'
        },
        {
            'category': 'industrial-nets',
            'name': 'Heavy Duty Cargo Securing Net',
            'slug': 'heavy-duty-cargo-securing-net',
            'description': '<p>Premium cargo securing netting perfect for transport vehicles, shipping containers, and heavy load retention.</p>',
            'features': "Reinforced boundary ropes\nHeavy-duty mesh structure\nWeather and chemical resistant\nAvailable in custom sizes",
            'url': 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&q=80&w=800'
        },
        {
            'category': 'agricultural-nets',
            'name': 'Premium Crop Shade Netting',
            'slug': 'premium-crop-shade-netting',
            'description': '<p>Protect delicate plants from extreme heat, direct sunlight, and wind damage with our professional shade netting.</p>',
            'features': "Available in 50% to 90% shade rates\nRot proof HDPE material\nLightweight and easy installation\nEnhanced crop yield protection",
            'url': 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&q=80&w=800'
        },
        {
            'category': 'agricultural-nets',
            'name': 'High-Density Anti-Bird Netting',
            'slug': 'high-density-anti-bird-netting',
            'description': '<p>Safeguard your orchards and vineyards from bird damage without harming the wildlife. Lightweight yet incredibly strong.</p>',
            'features': "Fine mesh prevents smallest birds\nHigh-density polyethylene\nDoes not block sunlight or rain\nRe-usable for multiple seasons",
            'url': 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&q=80&w=800'
        },
        {
            'category': 'marine-industrial-ropes',
            'name': 'Double-Braided Nylon Dock Line',
            'slug': 'double-braided-nylon-dock-line',
            'description': '<p>Superb marine-grade nylon ropes that offer excellent shock absorption and strength under extreme heavy docking situations.</p>',
            'features': "Superior shock absorption\nHighly flexible and knot-friendly\nResistant to marine rot, oils & chemicals\nPre-spliced eyelets available",
            'url': 'https://images.unsplash.com/photo-1553531384-cc64ac80f931?auto=format&fit=crop&q=80&w=800'
        },
        {
            'category': 'marine-industrial-ropes',
            'name': 'Natural Biodegradable Sisal Rope',
            'slug': 'natural-biodegradable-sisal-rope',
            'description': '<p>Traditional eco-friendly sisal rope made from 100% natural agave fibers. Offers great grip and classic industrial feel.</p>',
            'features': "100% natural agave fibers\nFully biodegradable and non-toxic\nExcellent grip & knot retention\nPerfect for agricultural ties and crafts",
            'url': 'https://images.unsplash.com/photo-1553531384-cc64ac80f931?auto=format&fit=crop&q=80&w=800'
        }
    ]

    for index, p in enumerate(prod_data):
        prod = Product(
            category=categories[p['category']],
            name=p['name'],
            slug=p['slug'],
            description=p['description'],
            features=p['features'],
            order=index
        )
        img_file = download_image(p['url'], f"{p['slug']}.jpg")
        prod.main_image.save(f"{p['slug']}.webp", img_file, save=True)
        print(f"Created Product: {prod.name}")

    print("Seeding Team Members...")
    team_data = [
        {
            'name': 'Cameron Williamson',
            'role': 'Founder & Managing Director',
            'url': 'https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&q=80&w=400'
        },
        {
            'name': 'Jacob Jones',
            'role': 'VP of Global Operations',
            'url': 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&q=80&w=400'
        },
        {
            'name': 'Eleanor Pena',
            'role': 'Chief Technical Officer',
            'url': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=400'
        },
        {
            'name': 'Arlene McCoy',
            'role': 'Lead Material Engineer',
            'url': 'https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&q=80&w=400'
        }
    ]

    for index, t in enumerate(team_data):
        member = TeamMember(
            name=t['name'],
            role=t['role'],
            order=index,
            is_active=True
        )
        img_file = download_image(t['url'], f"team_{index}.jpg")
        member.image.save(f"team_{index}.webp", img_file, save=True)
        print(f"Created Team Member: {member.name}")

    print("Seeding Testimonials...")
    testimonial_data = [
        {
            'name': 'Marvin McKinney',
            'role': 'Procurement Director, Global Build Co.',
            'text': "Tianbao's industrial netting has transformed our site safety standards. The tensile strength and weather resistance of their crop netting are unmatched, standing strong even through storm seasons.",
            'url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=150'
        },
        {
            'name': 'Leslie Alexander',
            'role': 'Managing Partner, AgroGrow Ltd.',
            'text': "We imported over 50,000 square meters of custom agricultural shade netting. The entire bulk order was extruded, packed, and delivered directly to our regional warehouses right on schedule.",
            'url': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=150'
        },
        {
            'name': 'Wade Warren',
            'role': 'Operations Manager, Marine Logistics Inc.',
            'text': "Their double-braided nylon ropes have high shock absorption. They hold our docking vessels steady in high-current zones. Simply outstanding performance and lifetime.",
            'url': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&q=80&w=150'
        },
        {
            'name': 'Kristin Watson',
            'role': 'Quality Control Lead, SafeNet Solutions',
            'text': "We ran extensive stress-testing on Tianbao's netting rolls. They met and exceeded all of our rigorous load-bearing safety specifications. We've made them our primary source manufacturer.",
            'url': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=150'
        }
    ]

    for index, t in enumerate(testimonial_data):
        test = Testimonial(
            name=t['name'],
            role=t['role'],
            text=t['text'],
            order=index,
            is_active=True
        )
        img_file = download_image(t['url'], f"testimonial_{index}.jpg")
        test.image.save(f"testimonial_{index}.webp", img_file, save=True)
        print(f"Created Testimonial: {test.name}")

    print("Database seeding completed successfully!")

if __name__ == '__main__':
    run()
