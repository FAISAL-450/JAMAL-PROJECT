from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    # 🔹 Actual Fields-(used in forms and templates)
    name_of_project = models.CharField(max_length=255)
    project_address = models.CharField(max_length=500)
    contact_person_name = models.CharField(max_length=255)
    contact_person_number = models.CharField(max_length=20)

    # 🔸 Extra Fields-(used in backend logic)
    team_members = models.ManyToManyField(User, related_name='team_projects', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_of_project

    class Meta:
        ordering = ['-created_at']  # Optional: newest projects first
        verbose_name = "Project"
        verbose_name_plural = "Projects"





