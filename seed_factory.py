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

from factory.models import FactoryHeader, FactoryGallerySection, FactoryImage, FactoryVideoSection, FactoryVideo, FactoryCTA

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
    print("Clearing old factory data...")
    FactoryImage.objects.all().delete()
    FactoryVideo.objects.all().delete()
    FactoryGallerySection.objects.all().delete()
    FactoryVideoSection.objects.all().delete()
    FactoryHeader.objects.all().delete()
    FactoryCTA.objects.all().delete()

    print("Seeding Factory Header...")
    header, _ = FactoryHeader.objects.get_or_create(id=1, defaults={
        'title': 'State-of-the-Art Manufacturing',
        'subtitle': 'Explore our advanced manufacturing facilities where precision meets scale. We leverage cutting-edge technology to produce the highest quality nets and ropes.'
    })
    header_img = download_image('https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=1920', 'factory_header.jpg')
    header.bg_image.save('factory_header.webp', header_img, save=True)

    print("Seeding Factory Gallery Section...")
    gallery_sec, _ = FactoryGallerySection.objects.get_or_create(id=1, defaults={
        'title': 'Explore Our Factory Gallery',
        'description': 'Take a visual tour through our advanced manufacturing facilities. From raw material sourcing to final packaging, see the dedication that goes into every fiber.'
    })

    print("Seeding 6 Gallery Images...")
    images_list = [
        {
            'title': 'High-Speed Weaving Looms',
            'description': 'Our state-of-the-art weaving looms operate around the clock to produce robust and consistent netting patterns with high precision and anti-fray weave.',
            'url': 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=800'
        },
        {
            'title': 'Automated Monofilament Extrusion',
            'description': 'Raw polymers are melted, blended with UV stabilizers, and extruded into extremely fine, high-strength monofilaments that form the base of our products.',
            'url': 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&q=80&w=800'
        },
        {
            'title': 'Tensile Strength Testing Lab',
            'description': 'Every production batch undergoes strict load testing in our laboratory to certify break strength, elasticity, and compliance with safety standards.',
            'url': 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&q=80&w=800'
        },
        {
            'title': 'Raw Materials Warehouse',
            'description': 'We store premium quality virgin HDPE and high-grade fibers in our climate-controlled warehouse to ensure absolute consistency in our raw supplies.',
            'url': 'https://images.unsplash.com/photo-1587293852726-70cdb56c2866?auto=format&fit=crop&q=80&w=800'
        },
        {
            'title': 'Precision Heat Sealing Lines',
            'description': 'Heavy-duty tarpaulins and custom agriculture netting sizes are heat-sealed and bordered with reinforced grommets for maximum longevity.',
            'url': 'https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?auto=format&fit=crop&q=80&w=800'
        },
        {
            'title': 'Global Logistics & Packaging',
            'description': 'Finished netting and rope rolls are compressed, shrink-wrapped, and securely palletized for container shipping to our partners worldwide.',
            'url': 'https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&q=80&w=800'
        }
    ]

    for index, img_data in enumerate(images_list):
        img_obj = FactoryImage(
            gallery=gallery_sec,
            title=img_data['title'],
            description=img_data['description'],
            order=index,
            is_active=True
        )
        # Download images
        f_thumb = download_image(img_data['url'], f"gallery_thumb_{index}.jpg")
        f_full = download_image(img_data['url'], f"gallery_full_{index}.jpg")
        img_obj.image.save(f"gallery_thumb_{index}.webp", f_thumb, save=False)
        img_obj.image_full.save(f"gallery_full_{index}.webp", f_full, save=False)
        img_obj.save()
        print(f"Successfully seeded gallery image: {img_data['title']}")

    print("Seeding Factory Video Section...")
    video_sec, _ = FactoryVideoSection.objects.get_or_create(id=1, defaults={
        'title': 'Watch Our Manufacturing Process',
        'description': 'Step onto the factory floor and witness the precision, scale, and advanced technology that goes into crafting every product we deliver.'
    })

    print("Seeding 4 Videos...")
    videos_list = [
        {
            'title': 'Extrusion & Spinning Lines',
            'description': 'Raw polymers are melted and extruded into high-strength monofilaments. This critical step ensures the foundational durability of all our netting products.',
            'youtube_url': 'https://www.youtube.com/embed/T07Ib_nTPoE'
        },
        {
            'title': 'Automated Net Weaving Technology',
            'description': 'Watch our heavy-duty German knitting machines weave thousands of fibers simultaneously into robust agricultural and safety nets.',
            'youtube_url': 'https://www.youtube.com/embed/V6vCae7P9t0'
        },
        {
            'title': 'Tensile Stress Testing Procedures',
            'description': 'Witness the strict testing procedures in our QC lab where ropes and nets are pulled to their limits to certify safety thresholds.',
            'youtube_url': 'https://www.youtube.com/embed/2_N1X8Jb9_8'
        },
        {
            'title': 'Logistics, Packing & Container Loading',
            'description': 'See how our global shipping team packs, compresses, and loads bulk orders securely onto container trucks for ports.',
            'youtube_url': 'https://www.youtube.com/embed/J7i_lIuT2W8'
        }
    ]

    for index, v_data in enumerate(videos_list):
        FactoryVideo.objects.create(
            video_section=video_sec,
            title=v_data['title'],
            description=v_data['description'],
            youtube_url=v_data['youtube_url'],
            order=index,
            is_active=True
        )
        print(f"Successfully seeded video: {v_data['title']}")

    print("Seeding Factory CTA...")
    FactoryCTA.objects.get_or_create(id=1, defaults={
        'title': 'Interested in a Facility Tour?',
        'description': 'We welcome our partners to visit our manufacturing facilities. Contact our team to schedule an in-person or virtual tour of our production lines.',
        'btn_text': 'Schedule a Tour',
        'btn_link': '/contact/'
    })

    print("Factory data seeding completed successfully!")

if __name__ == '__main__':
    run()
