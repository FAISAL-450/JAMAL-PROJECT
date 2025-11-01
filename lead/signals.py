import logging
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Lead
from customerdetailed.models import Profile

# Set up logging
logger = logging.getLogger(__name__)

# 🔁 Auto-fill customer details before saving a Lead
@receiver(pre_save, sender=Lead)
def autofill_customer_details(sender, instance, **kwargs):
    if instance.customer_name:
        try:
            logger.info(f"Signal triggered for customer: {instance.customer_name.name}")
            instance.customer_email = instance.customer_name.email
            instance.customer_phone = instance.customer_name.phone
            instance.customer_company = instance.customer_name.company
        except Exception as e:
            logger.error(f"Error autofilling customer details: {e}")

# 👤 Create Profile automatically when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.create(
                user=instance,
                team='Unassigned'  # Prevents NOT NULL error
            )
            logger.info(f"Profile created for new user: {instance.username}")
        except Exception as e:
            logger.error(f"Failed to create Profile for {instance.username}: {e}")

