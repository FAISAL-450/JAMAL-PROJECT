from django.db import models
from django.contrib.auth.models import User

# Role list for-customerdetailed-app
ROLE_CHOICES = [
    ('support', 'Support'),
]

class CustomerdetailedProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='customerdetailed_profile'
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='support',
        help_text="Defines the user's role in customer operations"
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        ordering = ['user__username']
        verbose_name = "Customer Role Profile"
        verbose_name_plural = "Customer Role Profiles"


class CustomerDetailed(models.Model):
    name = models.CharField(max_length=100, help_text="Customer's full name")
    address = models.CharField(max_length=100, help_text="Customer's address")
    email = models.EmailField(help_text="Customer's email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Optional phone number")
    company = models.CharField(max_length=100, blank=True, help_text="Optional company name")
    team = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        help_text="Team responsible for this customer"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_customers',
        help_text="User who created this customer record"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customer Detail"
        verbose_name_plural = "Customer Details"

