# A - Import Required Modules
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import PrProfile

# B - Signal: Create PrProfile When User Is Created
@receiver(post_save, sender=User)
def create_pr_profile(sender, instance, created, **kwargs):
    if created:
        PrProfile.objects.create(user=instance)


