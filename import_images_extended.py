import os
import random
import django
from django.core.files import File
from django.utils.text import slugify

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from products.models import Category, Product, ProductImage

SUN_SHADE_PRODUCTS = [
    {
        "name": "Premium Agricultural Green Sun Shade Net (80% Shade)",
        "desc": "<p>Our Premium Agricultural Green Sun Shade Net is engineered from 100% virgin High-Density Polyethylene (HDPE) with advanced UV stabilizers. Designed for long-term outdoor use, it provides 80% shade block, making it ideal for greenhouses, plant nurseries, and crop protection. The breathable knitted construction reduces heat buildup while allowing essential airflow and moisture transmission. Reinforced edges and heavy-duty grommets ensure secure installation and resistance against strong winds.</p>",
        "features": "Manufactured from 100% Virgin HDPE with UV stabilizers\nProvides 80% shade block and optimal light diffusion\nProtects crops from harsh sunlight, heat stress, and hail\nBreathable knitted mesh allows water and air circulation\nReinforced triangular edges with rust-proof aluminum grommets"
    },
    {
        "name": "Earth-Tone Privacy & Pergola Sun Shade Net",
        "desc": "<p>Enhance the aesthetic and comfort of your outdoor living spaces with our Earth-Tone Privacy Sun Shade Net. Featuring a natural brown/mocha color, it blends seamlessly with wooden pergolas, patios, and outdoor landscaping. This net offers a 90% UV block, significantly cooling shaded areas while providing excellent visual privacy. The tear-resistant knitted fabric withstands harsh weather conditions without fading or degrading.</p>",
        "features": "90% UV block and privacy screening\nNatural earth-tone color perfect for residential landscaping\nReduces ambient temperature by up to 15 degrees\nMold, mildew, and weather-resistant fabric\nIdeal for pergolas, deck shading, and fencing"
    },
    {
        "name": "Heavy-Duty Black Commercial Shade Net (95%)",
        "desc": "<p>Built for industrial and commercial applications, this heavy-duty black shade net offers maximum sun block at 95%. It is the preferred choice for car parking lots, construction site fencing, and livestock shading. The dense weave provides superior tensile strength and durability, ensuring longevity even in extreme desert or tropical climates.</p>",
        "features": "Maximum 95% shade block for superior cooling\nCommercial-grade high-tensile strength material\nExcellent for car parking sheds and construction sites\nResists fraying and unraveling when cut\nLong lifespan even under continuous direct sunlight"
    },
    {
        "name": "UV-Stabilized Greenhouse Shade Net (50% Shading)",
        "desc": "<p>A critical component for controlled environment agriculture, this 50% greenhouse shade net allows adequate sunlight for photosynthesis while preventing sunburn on delicate plants. The uniform mesh guarantees consistent light distribution and temperature control, promoting healthier and faster crop yields.</p>",
        "features": "50% shading tailored for optimal photosynthesis\nUniform light diffusion across the greenhouse\nProtects against sunburn, wind, and heavy rain\nReduces irrigation requirements by minimizing evaporation\nLightweight and easy to deploy over hoop houses"
    },
    {
        "name": "Mono-Tape Knitted Agricultural Shade Cloth",
        "desc": "<p>The mono-tape knitted shade cloth combines mono-filament and tape-filament yarns to create a highly durable and dimensionally stable net. This specialized construction offers excellent run-resistance and structural integrity, making it perfect for heavy-duty agricultural shading and windbreak applications.</p>",
        "features": "Hybrid mono-filament and tape-filament construction\nExceptional dimensional stability and tear resistance\nPrevents running or unraveling if punctured\nHighly effective windbreak and dust suppression properties\nSuitable for large-scale agricultural installations"
    },
    {
        "name": "Desert Sand Car Parking Shade Net",
        "desc": "<p>Specifically designed for automotive protection, the Desert Sand Car Parking Shade Net provides up to 95% UV protection to keep vehicle interiors cool and prevent paint fading. The attractive sand color reflects heat effectively and adds an architectural elegance to parking structures.</p>",
        "features": "95% UV protection specifically for vehicle safety\nHighly reflective sand/beige color reduces heat absorption\nArchitectural grade tension fabric\nWater-permeable to prevent water pooling during rain\nIdeal for commercial and residential parking bays"
    },
    {
        "name": "Construction Scaffolding Safety Net",
        "desc": "<p>Ensure job site safety and compliance with our robust Construction Scaffolding Safety Net. This high-visibility netting prevents debris from falling off scaffolding, protects workers from wind and sun exposure, and acts as a visual barrier. It is flame retardant and meets international safety standards.</p>",
        "features": "Heavy-duty debris containment netting\nHigh-visibility color for site safety\nFlame retardant and chemically resistant\nReinforced buttonholes for easy cable tie installation\nProvides wind reduction for workers at height"
    },
    {
        "name": "Windbreak Dust Suppression Shade Net",
        "desc": "<p>Control environmental hazards with our Windbreak and Dust Suppression Net. Designed with a specific aerodynamic porosity, it drastically reduces wind velocity and catches airborne dust particles. Essential for mining sites, open stockpiles, and agricultural borders exposed to strong crosswinds.</p>",
        "features": "Engineered aerodynamic porosity for wind reduction\nEffectively captures and suppresses airborne dust\nProtects crops and soil from wind erosion\nHigh UV resistance for continuous outdoor exposure\nDurable and maintenance-free solution"
    },
    {
        "name": "Multi-Color Striped Balcony Privacy Net",
        "desc": "<p>Add a touch of color and privacy to your apartment balcony with our multi-color striped privacy net. It blocks out prying eyes and harsh sunlight while allowing a gentle breeze to flow through. The vibrant, fade-resistant stripes enhance your outdoor decor.</p>",
        "features": "Vibrant, fade-resistant multi-color stripes\nHigh privacy rating (85% block)\nEasy installation with included tie-cords\nBreathable fabric keeps the balcony cool\nPerfect for apartments, condos, and townhouses"
    },
    {
        "name": "Poultry Farm Heat Reduction Shade Net",
        "desc": "<p>Maintain optimal temperatures in poultry farms and livestock enclosures with our specialized heat reduction shade net. By significantly lowering the internal temperature of the shed, it reduces animal heat stress, improves feed conversion ratios, and lowers mortality rates during summer months.</p>",
        "features": "Specifically designed for livestock and poultry cooling\nLowers shed temperatures by up to 20%\nImproves animal welfare and productivity\nEasy to clean and sanitize\nResistant to ammonia and farm chemicals"
    },
    {
        "name": "Hail Protection Shade Net for Orchards",
        "desc": "<p>Protect your valuable fruit crops from devastating hail damage with our heavy-duty Hail Protection Net. Woven with extra-strong monofilament threads, it absorbs the impact of hailstones while still providing necessary shading and ventilation for the orchard.</p>",
        "features": "High-impact resistance against hailstones\nDouble-reinforced threads for maximum durability\nProvides moderate shading (30-40%) suitable for fruit trees\nProtects against birds and large insects\nLong-lasting investment for orchard security"
    },
    {
        "name": "Tennis Court Privacy Screen Windbreak Net",
        "desc": "<p>Professional-grade tennis court windbreak and privacy screen. Designed to reduce crosswinds that affect gameplay and block visual distractions from outside the court. The dark green or black finish provides an excellent contrasting background for the tennis ball.</p>",
        "features": "Professional-grade wind reduction for sports courts\nProvides a dark, contrasting background for visibility\nReduces visual distractions for players\nHeavy-duty brass grommets spaced evenly for tight installation\nUV stabilized to prevent fading"
    },
    {
        "name": "Aluminet Thermal Screen Shade Cloth (Cooling Net)",
        "desc": "<p>Aluminet is a highly reflective, metalized shade screen that acts like a mirror to deflect harsh sunlight and heat. It is the ultimate cooling net for premium greenhouses and dog show canopies, providing superior temperature reduction compared to standard black or green nets.</p>",
        "features": "Metalized reflective coating deflects solar radiation\nSuperior thermal insulation and cooling effect\nLightweight and highly flexible\nExcellent for premium greenhouses and pet enclosures\nPrevents frost damage during cold nights by reflecting radiant heat"
    },
    {
        "name": "High-Tensile UV Treated Pond Shade Net",
        "desc": "<p>Protect aquaculture and fish ponds from excessive sunlight and predatory birds with our Pond Shade Net. Reducing sunlight penetration helps control algae blooms and maintains optimal water temperatures for fish health.</p>",
        "features": "Controls algae growth by reducing sunlight penetration\nKeeps water temperatures stable for aquaculture\nActs as a barrier against predatory birds\nChemically inert and safe for marine life\nHigh-tensile strength to cover large spans"
    },
    {
        "name": "Premium White Reflective Sun Shade Net",
        "desc": "<p>Our Premium White Shade Net provides excellent light diffusion without altering the light spectrum, making it ideal for flowering plants and retail garden centers. The white color reflects heat, keeping the area underneath significantly cooler while appearing bright and inviting.</p>",
        "features": "Reflects heat while providing bright, diffused light\nDoes not alter the color spectrum of sunlight\nIdeal for retail garden centers and flowering plants\nAesthetically clean and bright appearance\nMade from high-quality UV-stabilized HDPE"
    }
]

ROPE_PRODUCTS = [
    {
        "name": "High-Strength Nylon Braided Rope",
        "desc": "<p>Premium braided nylon rope offering exceptional strength, elasticity, and shock absorption. Ideal for demanding applications requiring high tensile strength and resistance to abrasion and UV degradation. This rope is the top choice for heavy-duty tying, towing, and industrial rigging.</p>",
        "features": "Superior tensile strength and durability\nExcellent shock absorption and elasticity\nResistant to abrasion, UV rays, and most chemicals\nSmooth handling and easy to knot\nPerfect for marine, industrial, and heavy-duty general use"
    },
    {
        "name": "Industrial Grade Manila Rope",
        "desc": "<p>Classic natural fiber manila rope known for its strength, low stretch, and excellent grip. Manufactured from high-quality abaca fibers, it is treated for rot and mildew resistance, making it suitable for landscaping, decorative purposes, and heavy lifting in traditional settings.</p>",
        "features": "100% natural abaca fibers\nExcellent grip and knot-holding ability\nLow stretch characteristic\nTraditional aesthetic appeal\nIdeal for tug-of-war, landscaping, and rustic decor"
    },
    {
        "name": "Marine Polypropylene Mooring Rope",
        "desc": "<p>Lightweight, buoyant, and highly visible polypropylene rope designed specifically for marine environments. It floats on water and offers good resistance to rot, mildew, and marine growth, making it an essential safety and utility tool for boaters.</p>",
        "features": "Floats on water for easy retrieval\nHighly visible colors for safety\nResistant to rot, mildew, and marine organisms\nLightweight and easy to handle\nSuitable for mooring, towing, and general boating applications"
    },
    {
        "name": "Heavy-Duty Cotton Tie Rope",
        "desc": "<p>Soft, pliable, and comfortable to handle, this heavy-duty cotton rope is perfect for applications where a gentle touch is required. It's biodegradable and easy to dye, making it versatile for crafts, interior design, and practical tying uses where synthetic ropes are not desired.</p>",
        "features": "Soft to the touch and easy on hands\nHighly flexible and knots securely\nBiodegradable and eco-friendly natural fibers\nIdeal for crafts, pet toys, and indoor tying applications\nCan be easily dyed to custom colors"
    },
    {
        "name": "Synthetic Winch Tow Rope (UHMWPE)",
        "desc": "<p>Advanced synthetic winch rope offering higher breaking strength than traditional steel cables of the same diameter. Extremely lightweight and safer to use, as it won't store energy and snap back if broken. Upgrade your 4x4 or ATV winch with this professional-grade recovery rope.</p>",
        "features": "Ultra-high molecular weight polyethylene (UHMWPE) construction\nStronger and lighter than steel wire rope\nSafer handling with no sharp burrs or recoil\nUV, chemical, and water resistant\nDesigned for off-road recovery and heavy towing"
    },
    {
        "name": "Twisted Polyester Anchor Line",
        "desc": "<p>High-quality twisted polyester rope providing the perfect balance of strength and flexibility. Unlike nylon, polyester has very low stretch, making it ideal for anchor lines, rigging, and applications where dimensional stability is crucial under heavy loads.</p>",
        "features": "Low stretch for precise load control\nHigh resistance to UV degradation and abrasion\nRetains strength when wet\nSmooth and comfortable to handle\nIdeal for anchor lines, halyards, and general rigging"
    },
    {
        "name": "Diamond Braid Multi-Purpose Utility Rope",
        "desc": "<p>A versatile and economical diamond braid rope featuring a polypropylene core and a durable outer sheath. This general-purpose utility cord is essential for camping, tying down cargo, DIY projects, and emergency preparedness kits.</p>",
        "features": "Economical multi-purpose design\nDiamond braid construction for snag resistance\nLightweight and easy to store\nResistant to oil, rot, and mildew\nPerfect for camping, tie-downs, and household use"
    },
    {
        "name": "High-Tenacity Kevlar/Aramid Fire Resistant Rope",
        "desc": "<p>Engineered for extreme environments, this Kevlar/Aramid rope offers unparalleled heat resistance and tensile strength. It will not melt or support combustion, making it the ultimate choice for fire rescue, high-temperature industrial applications, and extreme sports.</p>",
        "features": "Extreme heat and fire resistance (up to 400°C/752°F)\nIncredible tensile strength to weight ratio\nLow elongation and zero creep\nHighly resistant to cuts and abrasions\nEssential for rescue operations and aerospace applications"
    },
    {
        "name": "Sisal Natural Fiber Scratch Post & Craft Rope",
        "desc": "<p>A stiff, durable natural fiber rope extracted from the agave plant. Sisal is free of chemicals and oils, making it the absolute best material for constructing or repairing cat scratching posts, as well as for organic gardening and rustic home decor.</p>",
        "features": "100% natural, untreated sisal fibers\nStiff and durable texture\nCompletely safe and non-toxic for pets\nBiodegradable and environmentally friendly\nPerfect for cat trees, agriculture, and crafting"
    },
    {
        "name": "Jute Twine for Gardening and Packaging",
        "desc": "<p>Soft, pliable, and entirely organic, our premium Jute Twine is a staple for gardeners and crafters alike. It provides gentle support for climbing plants and tomatoes without cutting into stems, and adds a beautiful rustic touch to gift wrapping and packaging.</p>",
        "features": "Soft natural fibers won't damage plant stems\nFully biodegradable and compostable\nExcellent knot security\nVintage, rustic aesthetic\nIdeal for gardening, floristry, and gift wrapping"
    },
    {
        "name": "Double Braided Dock Line with Spliced Eye",
        "desc": "<p>Ready-to-use premium marine dock line. The double-braided nylon construction ensures maximum strength and controlled stretch to absorb shock loads from wakes and tides. It features a professionally spliced 12-inch eye on one end for easy cleat attachment.</p>",
        "features": "Double-braided nylon for superior shock absorption\nProfessionally spliced 12-inch eye loop\nResistant to marine growth, salt water, and UV rays\nSoft on boat finishes and comfortable to handle\nAvailable in various lengths and diameters for all vessel sizes"
    },
    {
        "name": "Colorful Paracord (550 Parachute Cord)",
        "desc": "<p>The ultimate survival and utility cord. Our 550 Paracord features a tough nylon sheath with 7 inner strands that can be removed for finer tasks like sewing or fishing. Available in highly visible and tactical colors, it is indispensable for camping, hiking, and survival bracelets.</p>",
        "features": "550 lbs minimum breaking strength\n7-strand removable inner core\nMildew, rot, and UV resistant\nLightweight and dries quickly\nPerfect for survival kits, crafting, and camping"
    },
    {
        "name": "Heavy-Duty PE (Polyethylene) Packing Rope",
        "desc": "<p>A rugged, waterproof, and highly durable polyethylene rope designed for heavy packaging, bundling, and industrial tying. It offers excellent knot retention and resists degradation from moisture and common chemicals.</p>",
        "features": "100% waterproof and buoyant\nResistant to most acids, alkalis, and oils\nHigh knot strength and retention\nEconomical solution for high-volume bundling\nWidely used in logistics, fishing, and agriculture"
    },
    {
        "name": "Baling Twine for Agricultural Hay",
        "desc": "<p>High-performance synthetic baling twine engineered for smooth running in all types of baling machinery. It offers consistent knot strength and high UV stabilization to ensure hay bales remain secure during long-term outdoor storage.</p>",
        "features": "Optimized for use in automatic baling machines\nHigh UV stabilization for outdoor storage\nConsistent tensile strength prevents bale breakage\nResistant to rot and rodents\nAvailable in high-visibility colors"
    },
    {
        "name": "Reflective Tent Guyline Rope",
        "desc": "<p>Enhance campsite safety with our highly reflective tent guylines. Woven with reflective tracer threads, this rope illuminates brightly when hit by a flashlight, preventing nighttime tripping hazards. Features a strong core for secure tent pitching in high winds.</p>",
        "features": "Highly reflective tracers for nighttime visibility\nLow stretch core for secure tent tensioning\nLightweight and compact\nIncludes aluminum tensioners for easy adjustment\nEssential for camping, backpacking, and outdoor canopies"
    }
]

def import_images_extended(base_path):
    print(f"Starting extended import from {base_path}...")
    
    # 1. Clear existing products in these categories to avoid messy duplicates and dummy data
    print("Clearing existing products in 'Sun Shade Nets' and 'Ropes & Twines'...")
    Category.objects.filter(name__in=["Sun Shade Nets", "Ropes & Twines"]).delete()
    print("Old data cleared.")
    
    # Process categories
    categories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    
    for cat_folder in categories:
        cat_path = os.path.join(base_path, cat_folder)
        print(f"\nProcessing category folder: {cat_folder}")
        
        is_rope = "rope" in cat_folder.lower()
        cat_name = "Ropes & Twines" if is_rope else "Sun Shade Nets"
        templates = ROPE_PRODUCTS if is_rope else SUN_SHADE_PRODUCTS
        
        # Create category
        category = Category.objects.create(
            name=cat_name,
            slug=slugify(cat_name),
            hero_text=f"Explore our premium, production-ready {cat_name} for professional applications."
        )
        print(f"Created new category: {cat_name}")
            
        # Get all images
        image_files = [f for f in os.listdir(cat_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        image_files.sort()
        
        if not image_files:
            print(f"No images found in {cat_path}")
            continue
            
        print(f"Found {len(image_files)} real images to distribute among {len(templates)} products.")
        
        # We will loop through templates and assign images randomly from the pool to simulate real large catalog
        for template in templates:
            # Pick 1 main image
            main_img_filename = random.choice(image_files)
            
            # Pick 3-5 additional images
            num_additional = random.randint(3, 5)
            # Make sure we don't pick the main image for additional (mostly)
            pool_for_additional = [img for img in image_files if img != main_img_filename]
            additional_img_filenames = random.sample(pool_for_additional, min(num_additional, len(pool_for_additional)))
            
            slug = slugify(template["name"])
            product = Product.objects.create(
                category=category,
                name=template["name"],
                slug=slug,
                description=template["desc"],
                features=template["features"],
                is_active=True
            )
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

if __name__ == "__main__":
    import_path = r"c:\Users\MD.MUNNA\Desktop\UK_portfolio\project\proucts image"
    import_images_extended(import_path)
    print("\nProduction-Ready Extended Import completed successfully!")
