#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Flush only app data (keep auth users) then reload fixture
python manage.py shell -c "
from products.models import Category, Product, ProductImage
from navigation.models import Navbar, Footer, SocialLink
ProductImage.objects.all().delete()
Product.objects.all().delete()
Category.objects.all().delete()
print('Cleared old product/category data')
"

python manage.py loaddata local_data.json