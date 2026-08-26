"""
Update factory gallery images and descriptions.
Run from project root: python update_factory_gallery.py
"""
import os, sys, django, shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from factory.models import FactoryImage
from django.core.files import File

ARTIFACT_DIR = r"C:\Users\MD.MUNNA\.gemini\antigravity-ide\brain\bf41df69-eba0-492f-8e29-73321b718a3d"

GALLERY_DATA = [
    {
        "pk": 13,
        "title": "High-Speed Net Weaving Looms",
        "description": "Our state-of-the-art computerized weaving looms operate continuously to produce robust, consistent shade netting and industrial net patterns with micron-level precision. Running 24/7, each loom is calibrated to deliver uniform mesh density, ensuring every roll meets our strict tensile strength and UV-resistance standards.",
        "image_file": os.path.join(ARTIFACT_DIR, "factory_gallery_1_weaving_1787759960565.jpg"),
    },
    {
        "pk": 14,
        "title": "Monofilament Extrusion Lines",
        "description": "Virgin HDPE polymer pellets are precision-melted and extruded into ultra-fine, high-strength monofilaments through our multi-zone extrusion lines. Each filament undergoes simultaneous UV stabilization and color integration, ensuring deep-dye consistency and long-term outdoor durability across all our netting and rope products.",
        "image_file": os.path.join(ARTIFACT_DIR, "factory_gallery_2_extrusion_1787759975661.jpg"),
    },
    {
        "pk": 15,
        "title": "Quality Control & Testing Lab",
        "description": "Every production batch is rigorously tested in our in-house QC laboratory using calibrated Instron tensile testing machines. Our QA engineers measure breaking force, elongation, UV degradation, and mesh aperture consistency — ensuring every product meets or exceeds international standards before it leaves our facility.",
        "image_file": os.path.join(ARTIFACT_DIR, "factory_gallery_3_testing_1787759990337.jpg"),
    },
    {
        "pk": 16,
        "title": "HDPE Raw Materials Warehouse",
        "description": "We maintain a 2,000+ metric ton inventory of premium virgin HDPE and polypropylene polymer pellets, stored in our climate-controlled warehouse. Our dedicated procurement team ensures a continuous, uninterrupted raw material supply chain — enabling us to fulfill large bulk orders and meet urgent delivery timelines reliably.",
        "image_file": os.path.join(ARTIFACT_DIR, "factory_gallery_4_warehouse_1787760015065.jpg"),
    },
    {
        "pk": 17,
        "title": "Edge Finishing & Heat Sealing",
        "description": "Finished shade nets and industrial netting pass through our precision heat-sealing production lines where edges are thermally bonded, reinforced with rope edging, and fitted with rust-resistant aluminum grommets. This critical finishing stage guarantees structural integrity under high-tension installation and harsh outdoor conditions.",
        "image_file": os.path.join(ARTIFACT_DIR, "factory_gallery_5_finishing_1787760030459.jpg"),
    },
    {
        "pk": 18,
        "title": "Export Packaging & Logistics",
        "description": "Finished products are compressed, shrink-wrapped, and securely palletized in our dedicated export packaging zone. Each consignment is barcoded, weighed, and documented with full compliance certificates before container loading. We ship to 30+ countries, ensuring every order arrives on time and in perfect condition.",
        "image_file": os.path.join(ARTIFACT_DIR, "factory_gallery_6_packaging_1787760100366.jpg"),
    },
]

for item in GALLERY_DATA:
    try:
        gallery_item = FactoryImage.objects.get(pk=item["pk"])
        gallery_item.title = item["title"]
        gallery_item.description = item["description"]

        img_path = item["image_file"]
        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                fname = f"gallery_{item['pk']}.jpg"
                gallery_item.image.save(fname, File(f), save=False)
                gallery_item.image_full.save(f"gallery_{item['pk']}_full.jpg", File(open(img_path, 'rb')), save=False)
            print(f"[OK] Updated pk={item['pk']}: {item['title']}")
        else:
            print(f"[WARN] Image not found for pk={item['pk']}, updating text only")

        gallery_item.save()
    except FactoryImage.DoesNotExist:
        print(f"[ERR] FactoryImage pk={item['pk']} not found")
    except Exception as e:
        print(f"[ERR] Error on pk={item['pk']}: {e}")

print("\n[DONE] Factory gallery update complete!")
