from django.db import models

class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ('Lead', 'Lead'),
        ('Prospect', 'Prospect'),
        ('Customer', 'Customer'),
        ('Partner', 'Partner'),
    ]
    
    LEAD_SOURCE_CHOICES = [
        ('Website', 'Website'),
        ('Referral', 'Referral'),
        ('Cold Reachout', 'Cold Reachout'),
        ('LinkedIn', 'LinkedIn'),
        ('Exhibition', 'Exhibition'),
        ('Other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Pending', 'Pending'),
        ('Hot', 'Hot (Highly Interested)'),
        ('Warm', 'Warm'),
        ('Cold', 'Cold'),
    ]

    customer_id = models.CharField(max_length=50, unique=True, blank=True, verbose_name="Customer ID")
    company_name = models.CharField(max_length=255, verbose_name="Company Name")
    contact_person = models.CharField(max_length=255, verbose_name="Contact Person")
    position = models.CharField(max_length=150, blank=True, verbose_name="Position")
    country = models.CharField(max_length=100, blank=True, verbose_name="Country")
    city = models.CharField(max_length=100, blank=True, verbose_name="City")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Phone")
    whatsapp = models.CharField(max_length=50, blank=True, verbose_name="WhatsApp")
    website = models.URLField(blank=True, null=True, verbose_name="Website")
    linkedin = models.URLField(blank=True, null=True, verbose_name="LinkedIn")
    product_interest = models.TextField(blank=True, verbose_name="Product Interest")
    customer_type = models.CharField(max_length=50, choices=CUSTOMER_TYPE_CHOICES, default='Lead', verbose_name="Customer Type")
    lead_source = models.CharField(max_length=50, choices=LEAD_SOURCE_CHOICES, default='Website', verbose_name="Lead Source")
    first_contact_date = models.DateField(blank=True, null=True, verbose_name="First Contact Date")
    last_contact_date = models.DateField(blank=True, null=True, verbose_name="Last Contact Date")
    next_followup_date = models.DateField(blank=True, null=True, verbose_name="Next Follow-up Date")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active', verbose_name="Status")
    notes = models.TextField(blank=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.customer_id:
            import random
            from django.utils import timezone
            date_str = timezone.now().strftime("%Y%m%d")
            while True:
                rand_num = random.randint(1000, 9999)
                candidate_id = f"CUST-{date_str}-{rand_num}"
                if not Customer.objects.filter(customer_id=candidate_id).exists():
                    self.customer_id = candidate_id
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company_name} ({self.contact_person})"
