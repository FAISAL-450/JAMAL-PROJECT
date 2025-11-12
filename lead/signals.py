# A - Import Required Modules
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import LeadProfile

# B - Signal: Create LeadProfile When User Is Created
@receiver(post_save, sender=User)
def create_lead_profile(sender, instance, created, **kwargs):
    if created:
        LeadProfile.objects.create(user=instance)
