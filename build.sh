#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Flush only app data (keep auth users) then reload fixture
python manage.py shell -c "
from products.models import Category, Product, ProductImage
from factory.models import FactoryHeader, FactoryGallerySection, FactoryImage, FactoryVideoSection, FactoryVideo, FactoryCTA
from navigation.models import Navbar, Footer, SocialLink

# Clear Products & Categories
ProductImage.objects.all().delete()
Product.objects.all().delete()
Category.objects.all().delete()

# Clear Factory Section Data
FactoryHeader.objects.all().delete()
FactoryGallerySection.objects.all().delete()
FactoryImage.objects.all().delete()
FactoryVideoSection.objects.all().delete()
FactoryVideo.objects.all().delete()
FactoryCTA.objects.all().delete()

print('Cleared old product, category, and factory data completely')
"

python manage.py loaddata local_data.json