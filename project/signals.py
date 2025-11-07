from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Project

# A - Handle Project Creation
@receiver(post_save, sender=Project)
def handle_project_create(sender, instance, created, **kwargs):
    if created:
        print(f"📦 [CREATE] New project created: '{instance.name_of_project}' by {instance.created_by.username}")

# B - Handle Project Update
@receiver(post_save, sender=Project)
def handle_project_update(sender, instance, created, **kwargs):
    if not created:
        print(f"✏️ [UPDATE] Project updated: '{instance.name_of_project}' by {instance.created_by.username}")

# C - Handle Project Deletion
@receiver(post_delete, sender=Project)
def handle_project_delete(sender, instance, **kwargs):
    print(f"🗑️ [DELETE] Project deleted: '{instance.name_of_project}' by {instance.created_by.username}")

