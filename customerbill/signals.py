# A - Import Required Modules
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CustomerbillProfile

# B - Signal: Create CustomerbillProfile When User Is Created
@receiver(post_save, sender=User)
def create_customerbill_profile(sender, instance, created, **kwargs):
    if created:
        CustomerbillProfile.objects.create(user=instance)
