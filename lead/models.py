from django.db import models
from customerdetailed.models import CustomerDetailed

class Lead(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('rejected', 'Rejected'),
    ]

    LEAD_SOURCE_CHOICES = [
        ('organic', 'Organic Search'),
        ('paid_ads', 'Paid Ads'),
        ('social', 'Social Media'),
        ('email', 'Email Campaign'),
        ('referral', 'Referral'),
        ('event', 'Event/Trade Show'),
        ('website', 'Website Form'),
        ('cold', 'Cold Call/Email'),
        ('affiliate', 'Affiliate Marketing'),
        ('content', 'Content Marketing'),
        ('sms', 'SMS Campaign'),
        ('chatbot', 'Chatbot Interaction'),
        ('partner', 'Channel Partner'),
        ('retargeting', 'Retargeting Campaign'),
        ('video', 'Video Marketing'),
        ('inbound_call', 'Inbound Call'),
        ('outbound_call', 'Outbound Call'),
        ('direct_mail', 'Direct Mail'),
        ('app', 'Mobile App'),
        ('demo', 'Product Demo'),
        ('survey', 'Survey Response'),
        ('linkedin', 'LinkedIn Outreach'),
        ('youtube', 'YouTube Channel'),
        ('podcast', 'Podcast Mention'),
        ('forum', 'Online Forum or Community'),
    ]

    customer_name = models.ForeignKey(
        CustomerDetailed,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='lead_customer_name',
        verbose_name="Customer Name"
    )
    customer_email = models.EmailField(blank=True)
    customer_phone = models.CharField(max_length=20, blank=True)
    customer_company = models.CharField(max_length=100, blank=True)

    source = models.CharField(max_length=30, choices=LEAD_SOURCE_CHOICES, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} ({self.customer_email})"
