import os
import django
import io
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from certificates.models import Certificate

def generate_professional_certificate(title, cert_num, standard_name, filename):
    print(f"Drawing certificate for: {title}...")
    width, height = 800, 1150
    # Create soft cream background
    img = Image.new('RGB', (width, height), color='#fdfbf7') 
    draw = ImageDraw.Draw(img)
    
    # Draw double border (Navy and Gold)
    draw.rectangle([15, 15, width-15, height-15], outline='#1a4674', width=8)
    draw.rectangle([25, 25, width-25, height-25], outline='#c0964b', width=2)
    
    # Corner ornaments
    draw.rectangle([20, 20, 30, 30], fill='#c0964b')
    draw.rectangle([width-30, 20, width-20, 30], fill='#c0964b')
    draw.rectangle([20, height-30, 30, height-20], fill='#c0964b')
    draw.rectangle([width-30, height-30, width-20, height-20], fill='#c0964b')
    
    # Load system serif/sans fonts
    try:
        font_serif_lg = ImageFont.truetype("georgia.ttf", 44)
        font_serif_md = ImageFont.truetype("georgia.ttf", 22)
        font_sans_bold = ImageFont.truetype("arial.ttf", 26)
        font_sans_sm = ImageFont.truetype("arial.ttf", 16)
        font_signature = ImageFont.truetype("georgia.ttf", 20)
    except IOError:
        font_serif_lg = font_serif_md = font_sans_bold = font_sans_sm = font_signature = ImageFont.load_default()
        
    # Write certificate text
    draw.text((width/2, 110), "TIANBAO MANUFACTURING GROUP", fill='#1a4674', font=font_sans_sm, anchor="mm")
    draw.text((width/2, 135), "TIANJIN FIBER NET CO., LTD.", fill='#1a4674', font=font_sans_sm, anchor="mm")
    
    # Decorative line
    draw.line([width/2 - 100, 165, width/2 + 100, 165], fill='#c0964b', width=2)
    
    # Title
    draw.text((width/2, 240), "CERTIFICATE", fill='#1a4674', font=font_serif_lg, anchor="mm")
    draw.text((width/2, 290), "OF CONFORMANCE & QUALITY", fill='#c0964b', font=font_serif_md, anchor="mm")
    
    # Certification body statement
    draw.text((width/2, 390), "This document certifies that the manufacturing processes for", fill='#475569', font=font_serif_md, anchor="mm")
    draw.text((width/2, 425), title, fill='#1a4674', font=font_sans_bold, anchor="mm")
    draw.text((width/2, 460), "have been audited and found to conform with international standard", fill='#475569', font=font_serif_md, anchor="mm")
    
    # Standard Box
    draw.rectangle([100, 510, width-100, 600], fill='#1a4674')
    draw.text((width/2, 555), standard_name, fill='#ffffff', font=font_sans_bold, anchor="mm")
    
    # Details section
    details = [
        f"Certificate Registration Number: {cert_num}",
        "Assessment Scope: Tensile strength compliance, UV stabilizer rating,",
        "environmental safety controls, and raw fiber quality management.",
        "Issued by: SGS Testing Laboratories & Compliance Board"
    ]
    
    y_start = 660
    for line in details:
        draw.text((width/2, y_start), line, fill='#334155', font=font_sans_sm, anchor="mm")
        y_start += 35
        
    # Gold Seal
    draw.ellipse([120, 840, 240, 960], fill='#c0964b', outline='#1a4674', width=2)
    draw.ellipse([130, 850, 230, 950], outline='#ffffff', width=2)
    draw.text((180, 890), "OFFICIAL", fill='#ffffff', font=font_sans_sm, anchor="mm")
    draw.text((180, 910), "SEAL", fill='#ffffff', font=font_sans_sm, anchor="mm")
    
    # Signature line
    draw.line([width - 320, 900, width - 120, 900], fill='#475569', width=1)
    draw.text((width - 220, 880), "Dr. Arthur Vance", fill='#1a4674', font=font_signature, anchor="mm")
    draw.text((width - 220, 920), "Auditing Committee", fill='#64748b', font=font_sans_sm, anchor="mm")
    
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=95)
    return ContentFile(buffer.getvalue(), name=filename)

def run():
    print("Clearing old certificates...")
    Certificate.objects.all().delete()

    certs = [
        {
            'title': 'ISO 9001:2015 Quality Management System',
            'cert_num': 'TX-9001-QMS-2026',
            'standard': 'ISO 9001:2015 COMPLIANCE'
        },
        {
            'title': 'CE Declaration of Conformity',
            'cert_num': 'TX-CE-DEC-5849',
            'standard': 'EN 1263-1 SAFETY NETS'
        },
        {
            'title': 'ISO 14001:2015 Environmental Certification',
            'cert_num': 'TX-14001-EMS-7741',
            'standard': 'ISO 14001:2015 EMS'
        },
        {
            'title': 'SGS Material Safety Compliance Certificate',
            'cert_num': 'SGS-MS-9983-2026',
            'standard': 'SGS HIGH TENSILE TEST'
        },
        {
            'title': 'Oeko-Tex Standard 100 Textile Safety',
            'cert_num': 'OTX-100-SAFE-221',
            'standard': 'OEKO-TEX STANDARD 100'
        },
        {
            'title': 'ISO 45001:2018 Health & Safety Standards',
            'cert_num': 'TX-45001-OHS-394',
            'standard': 'ISO 45001:2018 OHS'
        },
        {
            'title': 'FDA Food Grade Contact Compliance',
            'cert_num': 'FDA-FGC-7712-2026',
            'standard': 'FDA 21 CFR COMPLIANCE'
        },
        {
            'title': 'RoHS Environmental Protection Directive',
            'cert_num': 'ROHS-DIR-4028-2026',
            'standard': 'ROHS DIRECTIVE 2011/65/EU'
        },
        {
            'title': 'High-Tensile Strength Test Certificate',
            'cert_num': 'HTS-TEST-8811-2026',
            'standard': 'ISO 2307:2019 ROPE TEST'
        }
    ]

    for index, c in enumerate(certs):
        img_file = generate_professional_certificate(c['title'], c['cert_num'], c['standard'], f"cert_real_{index}.jpg")
        cert = Certificate(title=c['title'], order=index)
        cert.image.save(f"cert_real_{index}.webp", img_file, save=True)
        print(f"Successfully seeded professional certificate: {c['title']}")

if __name__ == '__main__':
    run()
