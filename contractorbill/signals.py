# A - Import Required Modules
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ContractorbillProfile

# B - Signal: Create ContractorbillProfile When User Is Created
@receiver(post_save, sender=User)
def create_contractorbill_profile(sender, instance, created, **kwargs):
    if created:
        ContractorbillProfile.objects.create(user=instance)
