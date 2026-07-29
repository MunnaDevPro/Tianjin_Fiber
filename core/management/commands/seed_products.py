import os
import requests
from io import BytesIO
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from core.models import Category, Product, ProductImage
from core.data import PRODUCTS

class Command(BaseCommand):
    help = 'Seeds the database with initial products from data.py'

    def handle(self, *args, **kwargs):
        # Create a default category
        category, created = Category.objects.get_or_create(
            name="Smart Electronics",
            slug="smart-electronics",
            hero_text="Discover our premium range of smart home devices."
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created category: Smart Electronics'))

        for p_data in PRODUCTS:
            product, p_created = Product.objects.get_or_create(
                slug=slugify(p_data['name']),
                defaults={
                    'name': p_data['name'],
                    'category': category,
                    'description': p_data['description'],
                    'features': '\n'.join(p_data.get('features', []))
                }
            )
            
            if p_created:
                self.stdout.write(f"Created product: {product.name}")
                
                # Fetch main image
                if p_data.get('image'):
                    try:
                        self.stdout.write(f"  Downloading main image for {product.name}...")
                        response = requests.get(p_data['image'])
                        if response.status_code == 200:
                            file_name = f"{product.slug}_main.jpg"
                            product.main_image.save(file_name, ContentFile(response.content), save=True)
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"  Failed to download image: {e}"))
                
                # Fetch additional images (thumbnails)
                for idx, thumb_url in enumerate(p_data.get('thumbnails', [])):
                    try:
                        self.stdout.write(f"  Downloading thumbnail {idx+1} for {product.name}...")
                        response = requests.get(thumb_url)
                        if response.status_code == 200:
                            file_name = f"{product.slug}_thumb_{idx}.jpg"
                            p_image = ProductImage(product=product)
                            p_image.image.save(file_name, ContentFile(response.content), save=True)
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"  Failed to download thumbnail: {e}"))

        self.stdout.write(self.style.SUCCESS('Successfully seeded products!'))
