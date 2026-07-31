import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Product

descriptions = {
    'Shade Net (Green)': """
        <h2>High-Quality Green Shade Net</h2>
        <p>Our premium dark green shade net is designed specifically for <strong>agriculture and professional gardening</strong>. It offers unparalleled protection against harsh sunlight, reducing heat stress on sensitive plants and promoting optimal growth conditions.</p>
        <h3>Key Benefits:</h3>
        <ul>
            <li><strong>UV Stabilized:</strong> Treated to resist degradation from ultraviolet rays, ensuring a long lifespan.</li>
            <li><strong>Optimal Shading:</strong> Provides a perfect balance of light diffusion and temperature control.</li>
            <li><strong>Durable Construction:</strong> Made from high-density polyethylene (HDPE) for maximum tear resistance.</li>
            <li><strong>Breathable Fabric:</strong> Allows air and moisture to pass through freely.</li>
        </ul>
        <p>Whether you are managing a large-scale agricultural project or a personal greenhouse, this shade net is your reliable partner.</p>
    """,
    'Coffee Shade Net': """
        <h2>Aesthetic Coffee Colored Shade Net</h2>
        <p>This uniquely colored shade net combines functionality with <strong>architectural elegance</strong>. Perfect for outdoor patios, pergolas, and commercial spaces where visual appeal is as important as sun protection.</p>
        <h3>Product Highlights:</h3>
        <ul>
            <li><strong>Elegant Design:</strong> Blends seamlessly with natural and wooden structures.</li>
            <li><strong>High UV Blockage:</strong> Blocks up to 90% of harmful UV rays.</li>
            <li><strong>Easy Installation:</strong> Comes with reinforced edges and rust-proof grommets.</li>
        </ul>
        <p>Transform your outdoor living area into a cool, comfortable, and stylish retreat.</p>
    """,
    'PE Tarpaulin': """
        <h2>Durable PE Tarpaulin</h2>
        <p>Our PE (Polyethylene) Tarpaulin is a versatile, <strong>lightweight yet heavy-duty</strong> waterproof cover. It is the go-to solution for everyday temporary roofing, agricultural covering, and general weather protection.</p>
        <h3>Features:</h3>
        <ul>
            <li><strong>100% Waterproof:</strong> Double-sided coating ensures zero water penetration.</li>
            <li><strong>Tear-Resistant:</strong> Woven core fabric provides exceptional strength.</li>
            <li><strong>Weatherproof:</strong> Resistant to rot, mold, and extreme weather conditions.</li>
        </ul>
        <p>Ideal for construction sites, camping, farming, and general outdoor storage needs.</p>
    """,
    'PVC Heavy Duty Tarpaulin': """
        <h2>Industrial Grade PVC Tarpaulin</h2>
        <p>Engineered for the toughest environments, our heavy-duty PVC coated tarpaulin is built for <strong>industrial and commercial use</strong>. It provides superior strength, longevity, and resistance to harsh elements.</p>
        <h3>Why Choose PVC?</h3>
        <ul>
            <li><strong>Extreme Durability:</strong> Thick PVC coating over a strong polyester mesh base.</li>
            <li><strong>Flame Retardant Options:</strong> Available with fire-resistant treatments for safety compliance.</li>
            <li><strong>Heavy Load Bearing:</strong> Withstands high winds, heavy snow, and physical abrasion.</li>
            <li><strong>Easy to Clean:</strong> Smooth surface allows for quick washing and maintenance.</li>
        </ul>
        <p>The ultimate choice for trucking covers, industrial tents, and long-term outdoor protection.</p>
    """,
    'Woven Tape PVC Tarpaulin': """
        <h2>Woven Tape PVC Tarpaulin</h2>
        <p>A specialized hybrid tarpaulin that utilizes a woven tape structure combined with a robust PVC coating. This unique manufacturing process results in a cover that is both <strong>incredibly strong and surprisingly flexible</strong>.</p>
        <h3>Product Specifications:</h3>
        <ul>
            <li><strong>Enhanced Flexibility:</strong> Easier to handle and fold than standard heavy-duty PVC.</li>
            <li><strong>High Tensile Strength:</strong> The woven tape core prevents stretching and tearing under tension.</li>
            <li><strong>All-Weather Protection:</strong> Fully waterproof and UV stabilized.</li>
        </ul>
        <p>Perfect for custom fabrication, large-scale event tents, and agricultural applications requiring frequent handling.</p>
    """,
    'Plant Cold Protection Cover': """
        <h2>Winter Plant Protection Cover</h2>
        <p>Safeguard your valuable crops and delicate garden plants from frost, freezing temperatures, and harsh winter winds with our specialized cold protection covers. Made from <strong>breathable, insulating non-woven fabric</strong>.</p>
        <h3>Key Advantages:</h3>
        <ul>
            <li><strong>Frost Prevention:</strong> Creates a microclimate that retains ground heat.</li>
            <li><strong>Breathable Material:</strong> Allows sunlight, air, and water to reach the plant, preventing suffocation.</li>
            <li><strong>Pest Protection:</strong> Acts as a physical barrier against insects and birds during early spring.</li>
            <li><strong>Lightweight:</strong> Will not crush or damage young seedlings.</li>
        </ul>
        <p>Ensure your garden survives the winter and thrives in the spring.</p>
    """,
    'Gardening Mat': """
        <h2>Premium Weed Control Gardening Mat</h2>
        <p>Our heavy-duty landscaping and gardening mat is the ultimate solution for <strong>chemical-free weed control</strong>. Designed for professional landscapers and serious gardeners.</p>
        <h3>Features & Benefits:</h3>
        <ul>
            <li><strong>Blocks Weeds:</strong> Dense woven fabric blocks sunlight, preventing weed seeds from germinating.</li>
            <li><strong>Water Permeable:</strong> Allows irrigation water and liquid fertilizers to reach the soil.</li>
            <li><strong>Soil Conservation:</strong> Helps retain soil moisture and prevents erosion.</li>
            <li><strong>Long-lasting:</strong> UV treated for years of reliable outdoor use.</li>
        </ul>
        <p>Keep your garden beds neat, tidy, and low-maintenance all season long.</p>
    """,
    'Sun Shade Sail': """
        <h2>Architectural Sun Shade Sail</h2>
        <p>Elevate your outdoor space with our stylish and highly functional sun shade sails. These tensioned fabric structures provide <strong>modern aesthetic appeal and excellent sun protection</strong> for residential and commercial areas.</p>
        <h3>Design Highlights:</h3>
        <ul>
            <li><strong>High UV Blockage:</strong> Protects your family and guests from harmful solar radiation.</li>
            <li><strong>Breathable Fabric:</strong> Allows hot air to escape, keeping the shaded area significantly cooler.</li>
            <li><strong>Reinforced Edges:</strong> Heavy-duty webbing and stainless steel D-rings for secure, tight installation.</li>
            <li><strong>Versatile Shapes:</strong> Available in triangular, square, and rectangular designs.</li>
        </ul>
        <p>Create a stunning focal point over your pool, patio, or playground.</p>
    """
}

# Default rich description for any product not in the dictionary
default_desc = """
    <h2>Premium Quality Product</h2>
    <p>This product is manufactured using state-of-the-art technology to ensure the <strong>highest quality standards</strong>. It is designed to meet the rigorous demands of our international clients.</p>
    <ul>
        <li><strong>Durable Material:</strong> Built to last in demanding environments.</li>
        <li><strong>Quality Assured:</strong> Rigorously tested before shipping.</li>
        <li><strong>Eco-Friendly:</strong> Manufactured with sustainable practices.</li>
    </ul>
"""

updated_count = 0
for product in Product.objects.all():
    # Only update if the current description is short (meaning it hasn't been updated yet)
    new_desc = descriptions.get(product.name, default_desc)
    product.description = new_desc.strip()
    product.save()
    updated_count += 1
    print(f"Updated: {product.name}")

print(f"Successfully updated {updated_count} products.")
