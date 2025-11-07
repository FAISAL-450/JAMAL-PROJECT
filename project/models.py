from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name_of_project = models.CharField(max_length=255)
    project_address = models.CharField(max_length=500)
    contact_person_name = models.CharField(max_length=255)
    contact_person_number = models.CharField(max_length=20)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name_of_project



