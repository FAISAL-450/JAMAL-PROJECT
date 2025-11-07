from django.db import models
from django.contrib.auth.models import User

# 🔹 Profile for Project users
class ProjectProfile(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('developer', 'Developer'),
        ('qa', 'QA'),
        ('support', 'Support'),
    ]
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='project_profile'
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='support'
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        ordering = ['user__username']
        verbose_name = "Project Profile"
        verbose_name_plural = "Project Profiles"


# 🔸 Project Model
class Project(models.Model):
    # Actual Fields
    name_of_project = models.CharField(max_length=255)
    project_address = models.CharField(max_length=500)
    contact_person_name = models.CharField(max_length=255)
    contact_person_number = models.CharField(max_length=20)

    # Extra Fields
    team = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_of_project

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"







