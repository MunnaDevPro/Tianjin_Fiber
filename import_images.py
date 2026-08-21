import os
import django
from django.core.files import File
from django.utils.text import slugify

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from products.models import Category, Product, ProductImage

# Product details definitions based on categories
PRODUCT_TEMPLATES = {
    "sun shade": [
        {
            "name": "Premium Agricultural Green Sun Shade Net",
            "desc": "<p>This heavy-duty green shade net is manufactured from high-density polyethylene (HDPE) with integrated UV stabilizers. Specifically engineered for agricultural greenhouses, plant nurseries, and rooftop gardens, it reduces heat stress on crops while maintaining optimal sunlight diffusion and ventilation. The reinforced black border with triangular corner protectors prevents edge fraying and ensures secure tensioning.</p>",
            "features": "High-density, UV-stabilized breathable mesh fabric\nTriangular reinforced corner guards with rust-proof aluminum grommets\nMulti-stitched heavy-duty border webbing for maximum tensile strength\nAllows water and airflow while diffusing harsh direct sunlight\nIdeal for horticulture, plant shading, polyhouses, and garden cooling"
        },
        {
            "name": "Earth-Tone Privacy & Pergola Sun Shade Net",
            "desc": "<p>Designed with a natural brown earth-tone finish, this knitted sun shade net offers a balance of privacy screening and solar heat reduction. Suitable for outdoor pergolas, patio enclosures, fencing, and deck shading, it blends seamlessly into wooden landscapes and modern architectural setups while resisting environmental wear and tear.</p>",
            "features": "Earthy brown knit that integrates naturally with outdoor woodwork and landscaping\nHigh light-blocking efficiency suitable for residential privacy screens\nBreathable fabric prevents heat entrapment\nUV resistant and weatherproof for long-term outdoor usage"
        },
        {
            "name": "Heavy-Duty Black Commercial Shade Net",
            "desc": "<p>Engineered for maximum sun block and durability, this black commercial-grade shade net provides superior protection for industrial, commercial, and heavy agricultural use. It delivers maximum UV protection and is designed to withstand extreme weather conditions.</p>",
            "features": "Maximum UV protection and shade percentage\nCommercial-grade reinforced stitching\nTear and fray resistant knitted construction\nPerfect for car parking shades, construction sites, and livestock shading"
        },
        {
            "name": "UV-Stabilized Greenhouse Shade Net",
            "desc": "<p>Optimal solution for temperature and light control in modern greenhouses. This shade net promotes healthy plant growth by diffusing light evenly and protecting delicate plants from sunburn and heat stress.</p>",
            "features": "Engineered for optimal light diffusion\nProtects crops from harsh UV rays and sunburn\nImproves greenhouse ventilation and temperature control\nDurable HDPE construction with long lifespan"
        },
        {
            "name": "Residential Patio & Garden Sun Shade",
            "desc": "<p>Enhance your outdoor living spaces with our premium patio shade net. Lightweight yet incredibly durable, it provides excellent cooling and UV protection for gardens, backyards, and children's play areas.</p>",
            "features": "Lightweight and easy to install\nAesthetic design suitable for homes and gardens\nSignificant temperature reduction for outdoor spaces\nMold and mildew resistant fabric"
        }
    ],
    "rope": [
        {
            "name": "High-Strength Nylon Braided Rope",
            "desc": "<p>Premium braided nylon rope offering exceptional strength, elasticity, and shock absorption. Ideal for demanding applications requiring high tensile strength and resistance to abrasion and UV degradation.</p>",
            "features": "Superior tensile strength and durability\nExcellent shock absorption and elasticity\nResistant to abrasion, UV rays, and most chemicals\nSmooth handling and easy to knot\nPerfect for marine, industrial, and heavy-duty general use"
        },
        {
            "name": "Industrial Grade Manila Rope",
            "desc": "<p>Classic natural fiber manila rope known for its strength, low stretch, and excellent grip. Treated for rot and mildew resistance, making it suitable for landscaping, decorative purposes, and heavy lifting.</p>",
            "features": "100% natural abaca fibers\nExcellent grip and knot-holding ability\nLow stretch characteristic\nTraditional aesthetic appeal\nIdeal for tug-of-war, landscaping, and rustic decor"
        },
        {
            "name": "Marine Polypropylene Mooring Rope",
            "desc": "<p>Lightweight, buoyant, and highly visible polypropylene rope designed specifically for marine environments. It floats on water and offers good resistance to rot, mildew, and marine growth.</p>",
            "features": "Floats on water for easy retrieval\nHighly visible colors for safety\nResistant to rot, mildew, and marine organisms\nLightweight and easy to handle\nSuitable for mooring, towing, and general boating applications"
        },
        {
            "name": "Heavy-Duty Cotton Tie Rope",
            "desc": "<p>Soft, pliable, and comfortable to handle, this heavy-duty cotton rope is perfect for applications where a gentle touch is required. It's biodegradable and easy to dye, making it versatile for crafts and practical uses.</p>",
            "features": "Soft to the touch and easy on hands\nHighly flexible and knots securely\nBiodegradable and eco-friendly natural fibers\nIdeal for crafts, pet toys, and indoor tying applications"
        },
        {
            "name": "Synthetic Winch Tow Rope",
            "desc": "<p>Advanced synthetic winch rope offering higher breaking strength than traditional steel cables of the same diameter. Extremely lightweight and safer to use, as it won't store energy and snap back if broken.</p>",
            "features": "Ultra-high molecular weight polyethylene (UHMWPE) construction\nStronger and lighter than steel wire rope\nSafer handling with no sharp burrs or recoil\nUV and chemical resistant\nDesigned for off-road recovery and heavy towing"
        }
    ]
}

def import_images(base_path):
    print(f"Starting import from {base_path}...")
    
    # Process categories
    categories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    
    for cat_folder in categories:
        cat_path = os.path.join(base_path, cat_folder)
        print(f"\nProcessing category folder: {cat_folder}")
        
        # Determine category name and map to templates
        is_rope = "rope" in cat_folder.lower()
        cat_name = "Ropes & Twines" if is_rope else "Sun Shade Nets"
        template_key = "rope" if is_rope else "sun shade"
        templates = PRODUCT_TEMPLATES[template_key]
        
        # Create or get category
        category, created = Category.objects.get_or_create(
            name=cat_name,
            defaults={
                'slug': slugify(cat_name),
                'hero_text': f"High Quality {cat_name} for all your needs."
            }
        )
        if created:
            print(f"Created new category: {cat_name}")
            
        # Get all images in this folder
        image_files = [f for f in os.listdir(cat_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        image_files.sort()
        
        if not image_files:
            print(f"No images found in {cat_path}")
            continue
            
        print(f"Found {len(image_files)} images.")
        
        # Divide images among the 5 templates
        images_per_product = max(1, len(image_files) // len(templates))
        
        for i, template in enumerate(templates):
            # Calculate slice of images for this product
            start_idx = i * images_per_product
            # If it's the last product, give it all remaining images
            end_idx = (i + 1) * images_per_product if i < len(templates) - 1 else len(image_files)
            
            product_images = image_files[start_idx:end_idx]
            
            if not product_images:
                continue
                
            main_img_filename = product_images[0]
            additional_img_filenames = product_images[1:]
            
            # Create product
            slug = slugify(template["name"])
            product, p_created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'category': category,
                    'name': template["name"],
                    'description': template["desc"],
                    'features': template["features"],
                    'is_active': True
                }
            )
            
            if p_created:
                print(f"  Created product: {product.name}")
                
                # Set main image
                main_img_path = os.path.join(cat_path, main_img_filename)
                with open(main_img_path, 'rb') as f:
                    product.main_image.save(main_img_filename, File(f), save=True)
                
                # Add additional images
                for order, add_img in enumerate(additional_img_filenames):
                    add_img_path = os.path.join(cat_path, add_img)
                    with open(add_img_path, 'rb') as f:
                        pi = ProductImage(product=product, order=order)
                        pi.image.save(add_img, File(f), save=True)
                
                print(f"    Added main image and {len(additional_img_filenames)} additional images.")
            else:
                print(f"  Product already exists: {product.name}")

if __name__ == "__main__":
    import_path = r"c:\Users\MD.MUNNA\Desktop\UK_portfolio\project\proucts image"
    import_images(import_path)
    print("\nImport completed successfully!")
