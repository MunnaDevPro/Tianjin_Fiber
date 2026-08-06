import os
import django
import urllib.request
import tempfile
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from certificates.models import Certificate

def run():
    print("Clearing old certificates...")
    Certificate.objects.all().delete()

    certs = [
        {
            'title': 'ISO 9001:2015 Quality Management System',
            'url': 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?auto=format&fit=crop&q=80&w=800'
        },
        {
            'title': 'CE Declaration of Conformity',
            'url': 'https://images.unsplash.com/photo-1606326608606-aa0b62935f2b?auto=format&fit=crop&q=80&w=800'
        },
        {
            'title': 'ISO 14001:2015 Environmental Certification',
            'url': 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&q=80&w=800'
        },
        {
            'title': 'SGS Material Safety Compliance Certificate',
            'url': 'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&q=80&w=800'
        },
        {
            'title': 'Oeko-Tex Standard 100 Textile Safety',
            'url': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&q=80&w=800'
        },
        {
            'title': 'ISO 45001:2018 Health & Safety Standards',
            'url': 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&q=80&w=800'
        },
        {
            'title': 'FDA Food Grade Contact Compliance',
            'url': 'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?auto=format&fit=crop&q=80&w=800'
        },
        {
            'title': 'RoHS Environmental Protection Directive',
            'url': 'https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?auto=format&fit=crop&q=80&w=800'
        },
        {
            'title': 'High-Tensile Strength Test Certificate',
            'url': 'https://images.unsplash.com/photo-1606326608606-aa0b62935f2b?auto=format&fit=crop&q=80&w=800'
        }
    ]

    for index, c in enumerate(certs):
        print(f"Downloading {c['title']}...")
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            req = urllib.request.Request(c['url'], headers=headers)
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            with urllib.request.urlopen(req, timeout=15) as response:
                temp_file.write(response.read())
            temp_file.close()
            
            django_file = File(open(temp_file.name, 'rb'), name=f"cert_{index}.jpg")
            cert = Certificate(title=c['title'], order=index)
            cert.image.save(f"cert_{index}.webp", django_file, save=True)
            print(f"Successfully seeded {c['title']}")
        except Exception as e:
            print(f"Failed to seed {c['title']}: {e}")

if __name__ == '__main__':
    run()
