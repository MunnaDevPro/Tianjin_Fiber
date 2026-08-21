import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from services.models import BusinessModelSection, BusinessModelItem

def update_business_models():
    section = BusinessModelSection.objects.first()
    if not section:
        return
        
    section.subtitle = "Partner with us for world-class manufacturing capabilities. Whether you are an established global brand requiring precise adherence to custom blueprints, or a growing distributor looking to private-label our proven product lines, we have a specialized division ready to scale your business."
    section.save()
    
    # Update OEM
    oem = BusinessModelItem.objects.filter(title="OEM").first()
    if oem:
        oem.description = "Complete end-to-end custom manufacturing. You retain full intellectual property rights over your designs. We provide the robust manufacturing infrastructure, strict raw material sourcing (100% Virgin HDPE), and rigorous Quality Assurance to bring your exact blueprints to life at scale."
        oem.features = "Design IP: 100% Client Owned\nManufacturing: Advanced In-house Facilities\nPrototyping: Dedicated R&D Support\nMaterial Sourcing: Custom to Specs\nConfidentiality: Strict NDA Binding"
        oem.save()
        
    # Update ODM
    odm = BusinessModelItem.objects.filter(title="ODM").first()
    if odm:
        odm.description = "Rapid market entry with zero R&D costs. Select from our extensive, field-tested catalog of premium sun shade nets and heavy-duty ropes. We will manufacture, package, and label these proven products under your exclusive brand identity, ensuring you deliver quality without the development overhead."
        odm.features = "Design IP: Factory Engineered\nManufacturing: Advanced In-house Facilities\nTime to Market: Accelerated (Ready-made)\nCustomization: Logo & Packaging\nRisk Factor: Minimal (Proven Products)"
        odm.save()
        
    print("Business models updated to be highly professional and informative.")

if __name__ == "__main__":
    update_business_models()
