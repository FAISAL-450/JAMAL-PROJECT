from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Lead
from customerdetailed.models import Profile  # ✅ Correct location

# 🔁 Auto-fill customer details before saving a Lead
@receiver(pre_save, sender=Lead)
def autofill_customer_details(sender, instance, **kwargs):
    if instance.customer_name:
        print(f"🔥 Signal triggered for: {instance.customer_name.name}")
        instance.customer_email = instance.customer_name.email
        instance.customer_phone = instance.customer_name.phone
        instance.customer_company = instance.customer_name.company

# 👤 Create Profile automatically when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            team='Unassigned'  # Prevents NOT NULL error
        )
