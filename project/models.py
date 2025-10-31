from django.db import models
class Project(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    name_of_project = models.CharField(max_length=255)  # Project name
    project_address = models.CharField(max_length=500)  # Project address as CharField
    contact_person_name = models.CharField(max_length=255)  # Name of contact person
    contact_person_number = models.CharField(max_length=20)  # Contact number of contact person
    
    def __str__(self):
        return f"{self.name_of_project}"

