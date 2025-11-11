# A - Import Required Modules
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CustomerdetailedProfile

# B - Signal: Create CustomerdetailedProfile When User Is Created
@receiver(post_save, sender=User)
def create_customerdetailed_profile(sender, instance, created, **kwargs):
    if created:
        CustomerdetailedProfile.objects.create(user=instance)
