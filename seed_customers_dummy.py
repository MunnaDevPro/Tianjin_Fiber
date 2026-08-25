import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from customers.models import Customer

def seed():
    Customer.objects.all().delete()
    print("Deleted existing customers.")

    customers_data = [
        {
            "company_name": "Global Tech Solutions Ltd",
            "contact_person": "James Harrison",
            "position": "Procurement Director",
            "country": "United Kingdom",
            "city": "London",
            "email": "j.harrison@globaltech.co.uk",
            "phone": "+44 20 7946 0958",
            "whatsapp": "+44 7700 900077",
            "website": "https://globaltechsolutions.co.uk",
            "linkedin": "https://linkedin.com/in/jamesharrison",
            "product_interest": "Looking for large scale fiber optic cables for our new datacenter expansion in Manchester.",
            "customer_type": "Customer",
            "lead_source": "Website",
            "status": "Active",
            "first_contact_date": date.today() - timedelta(days=45),
            "last_contact_date": date.today() - timedelta(days=2),
            "next_followup_date": date.today() + timedelta(days=5),
            "notes": "Very positive call last week. Requested technical specifications for the high-density cables. Quote sent.",
        },
        {
            "company_name": "Nordic Infrastructure AB",
            "contact_person": "Lars Johansson",
            "position": "Senior Buyer",
            "country": "Sweden",
            "city": "Stockholm",
            "email": "lars.j@nordicinfra.se",
            "phone": "+46 8 555 0123",
            "whatsapp": "",
            "website": "https://nordicinfra.se",
            "linkedin": "",
            "product_interest": "Telecommunication towers and steel support structures.",
            "customer_type": "Prospect",
            "lead_source": "Exhibition",
            "status": "Warm",
            "first_contact_date": date.today() - timedelta(days=120),
            "last_contact_date": date.today() - timedelta(days=15),
            "next_followup_date": date.today() + timedelta(days=1),
            "notes": "Met at the EuroTech Expo. They are planning a Q3 infrastructure upgrade. Need to follow up this week.",
        },
        {
            "company_name": "Apex Construction Partners",
            "contact_person": "Sarah Mitchell",
            "position": "Project Manager",
            "country": "United States",
            "city": "New York",
            "email": "smitchell@apexconstruct.com",
            "phone": "+1 212 555 0199",
            "whatsapp": "+1 917 555 0188",
            "website": "https://apexconstruct.com",
            "linkedin": "https://linkedin.com/company/apex-construction",
            "product_interest": "Industrial steel pipes and scaffolding materials.",
            "customer_type": "Lead",
            "lead_source": "LinkedIn",
            "status": "Hot",
            "first_contact_date": date.today() - timedelta(days=5),
            "last_contact_date": date.today() - timedelta(days=1),
            "next_followup_date": date.today(),
            "notes": "Urgent requirement for an ongoing project. Sent initial pricing list, awaiting approval.",
        },
        {
            "company_name": "Emirates Telecom Corp",
            "contact_person": "Tariq Al-Fayed",
            "position": "Head of Sourcing",
            "country": "United Arab Emirates",
            "city": "Dubai",
            "email": "tariq.alfayed@etelcom.ae",
            "phone": "+971 4 332 5555",
            "whatsapp": "+971 50 123 4567",
            "website": "https://etelcom.ae",
            "linkedin": "",
            "product_interest": "Complete turnkey networking solutions and fiber optics.",
            "customer_type": "Partner",
            "lead_source": "Referral",
            "status": "Active",
            "first_contact_date": date.today() - timedelta(days=300),
            "last_contact_date": date.today() - timedelta(days=10),
            "next_followup_date": date.today() + timedelta(days=30),
            "notes": "Long-term partner. Next quarterly review scheduled for next month.",
        },
        {
            "company_name": "TechFab Solutions GmbH",
            "contact_person": "Hans Weber",
            "position": "Chief Engineer",
            "country": "Germany",
            "city": "Munich",
            "email": "h.weber@techfab.de",
            "phone": "+49 89 1234 5678",
            "whatsapp": "",
            "website": "https://techfab.de",
            "linkedin": "https://linkedin.com/in/hansweber",
            "product_interest": "Custom fabricated metal enclosures.",
            "customer_type": "Lead",
            "lead_source": "Cold Reachout",
            "status": "Pending",
            "first_contact_date": date.today() - timedelta(days=20),
            "last_contact_date": date.today() - timedelta(days=20),
            "next_followup_date": date.today() + timedelta(days=2),
            "notes": "Sent introductory email and brochure. No response yet, schedule a follow-up call.",
        },
    ]

    for data in customers_data:
        Customer.objects.create(**data)
        print(f"Created customer: {data['company_name']}")

    print("Seeding complete.")

if __name__ == '__main__':
    seed()
