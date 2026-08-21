import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from services.models import ProcessStep

new_steps = [
    {
        "title": "Material Selection & Extrusion",
        "desc": "Sourcing 100% Virgin HDPE and premium polymers. Through advanced extrusion, we create high-tenacity monofilament yarns with integrated UV stabilizers."
    },
    {
        "title": "Knitting & Braiding Technology",
        "desc": "Utilizing state-of-the-art warp knitting machines for shade nets and heavy-duty braiders for ropes, ensuring consistent mesh sizes and maximum tensile strength."
    },
    {
        "title": "Custom Engineering & Sizing",
        "desc": "Tailoring specifications, shading percentages (30%-95%), and dimensions based on precise agricultural, commercial, or marine project requirements."
    },
    {
        "title": "Reinforcement & Finishing",
        "desc": "Applying heavy-duty border webbing, multi-stitched hemming, and rust-proof aluminum grommet installation to guarantee long-term structural integrity."
    },
    {
        "title": "Rigorous Quality Assurance (QA)",
        "desc": "Conducting intensive stress, UV resistance, and load-bearing tests to ensure every batch meets strict international safety and durability standards."
    },
    {
        "title": "Global Logistics & Support",
        "desc": "Secure compression packaging for efficient global shipping, backed by dedicated technical support and installation guidance for our international clients."
    }
]

def update_process_steps():
    steps = list(ProcessStep.objects.all().order_by('order'))
    if len(steps) != 6:
        print(f"Warning: Expected 6 steps, found {len(steps)}")
    
    for i, step_data in enumerate(new_steps):
        if i < len(steps):
            step = steps[i]
            step.title = step_data["title"]
            step.description = step_data["desc"]
            step.save()
            print(f"Updated step {i+1}: {step.title}")
        else:
            # If for some reason there are fewer than 6, create new ones
            ProcessStep.objects.create(
                title=step_data["title"],
                description=step_data["desc"],
                order=i+1,
                icon_class="fas fa-check" # fallback icon
            )
            print(f"Created step {i+1}: {step_data['title']}")

if __name__ == "__main__":
    update_process_steps()
    print("Process section updated successfully with real manufacturing data!")
