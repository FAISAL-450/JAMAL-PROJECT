from django.db import models
from django.contrib.auth.models import User

# Role list for contractor app
ROLE_CHOICES = [
    ('planner', 'Planner'),
]

class ContractorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='contractor_profile'
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='planner',
        help_text="Defines the user's role in contractor operations"
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        ordering = ['user__username']
        verbose_name = "Contractor Role Profile"
        verbose_name_plural = "Contractor Role Profiles"

class Contractor(models.Model):
    contractor_company = models.CharField(
        max_length=100,
        help_text="Name of the Contractor Company"
    )
    name_of_contractor = models.CharField(
        max_length=100,
        help_text="Name of the Contractor"
    )
    contractor_address = models.CharField(
        max_length=200,
        help_text="Contractor address"
    )
    contractor_phone_number = models.CharField(
        max_length=20,
        help_text="Phone number of the contractor"
    )
    team = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        help_text="Team responsible for this contractor"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_contractors',
        help_text="User who created this contractor"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contractor_company

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contractor"
        verbose_name_plural = "Contractors"

