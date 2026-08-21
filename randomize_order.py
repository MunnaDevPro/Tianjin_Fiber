import os
import random
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from products.models import Product

def randomize_product_order():
    products = list(Product.objects.all())
    print(f"Found {len(products)} products. Randomizing order...")
    
    # Randomize the list
    random.shuffle(products)
    
    # Update the order field based on the new random sequence
    for i, product in enumerate(products, start=1):
        product.order = i
        product.save(update_fields=['order'])
        
    print("Successfully randomized the order of all products!")

if __name__ == "__main__":
    randomize_product_order()
