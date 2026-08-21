import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from services.models import ProcessStep

short_steps = [
    {
        "title": "Material Selection & Extrusion",
        "desc": "Sourcing 100% Virgin HDPE and premium polymers to extrude high-tenacity, UV-stabilized yarns."
    },
    {
        "title": "Knitting & Braiding Technology",
        "desc": "Utilizing advanced warp knitting machines and heavy-duty braiders for maximum tensile strength."
    },
    {
        "title": "Custom Engineering & Sizing",
        "desc": "Tailoring dimensions, shading percentages, and specifications for specific project requirements."
    },
    {
        "title": "Reinforcement & Finishing",
        "desc": "Applying heavy-duty webbing and rust-proof grommets for long-term structural integrity."
    },
    {
        "title": "Rigorous Quality Assurance (QA)",
        "desc": "Conducting strict stress and UV resistance tests to meet international safety standards."
    },
    {
        "title": "Global Logistics & Support",
        "desc": "Secure compression packaging and dedicated technical support for our international clients."
    }
]

def update_process_steps_short():
    steps = list(ProcessStep.objects.all().order_by('order'))
    for i, step_data in enumerate(short_steps):
        if i < len(steps):
            step = steps[i]
            step.description = step_data["desc"]
            step.save()
            print(f"Updated step {i+1} with shorter text.")

if __name__ == "__main__":
    update_process_steps_short()
    print("Process descriptions shortened successfully!")
