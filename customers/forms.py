from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'customer_id', 'company_name', 'contact_person', 'position',
            'country', 'city', 'email', 'phone', 'whatsapp', 'website',
            'linkedin', 'product_interest', 'customer_type', 'lead_source',
            'first_contact_date', 'last_contact_date', 'next_followup_date',
            'status', 'notes'
        ]
        widgets = {
            'first_contact_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'last_contact_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'next_followup_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'product_interest': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'customer_id': 'e.g. CUST-2026-001 (Leave blank to auto-generate)',
            'company_name': 'e.g. Acme Corporation',
            'contact_person': 'e.g. John Doe',
            'position': 'e.g. Purchase Manager / Procurement Lead',
            'country': 'e.g. United Kingdom',
            'city': 'e.g. London',
            'email': 'e.g. buyer@acme.com',
            'phone': 'e.g. +44 20 7946 0958',
            'whatsapp': 'e.g. +44 7700 900077',
            'website': 'e.g. https://acme.com',
            'linkedin': 'e.g. https://linkedin.com/company/acme',
            'product_interest': 'e.g. Heavy Machineries, Steel Pipes, or general fabrication requests...',
            'notes': 'e.g. Client requested a catalog; schedule call next Monday...',
        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['placeholder'] = placeholder
                # Apply bootstrap class for fields that don't have it set already
                existing_class = self.fields[field_name].widget.attrs.get('class', '')
                if 'form-control' not in existing_class:
                    self.fields[field_name].widget.attrs['class'] = f"{existing_class} form-control".strip()
