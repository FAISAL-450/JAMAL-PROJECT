from django.db import models
from django.contrib.auth.models import User
from customerdetailed.models import CustomerDetailed
from project.models import Project  # Assuming Project is defined in project.models

# Role list
ROLE_CHOICES = [
    ('sm', 'SM'),
]

class CustomerbillProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='Customerbill_profile'
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='sm',
        help_text="Defines the user's role in customerbill operations"
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        ordering = ['user__username']
        verbose_name = "CustomerBill Role Profile"
        verbose_name_plural = "CustomerBill Role Profiles"


class Customerbill(models.Model):
    project_name = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='Customerbill_project_name',
        verbose_name="Project Name"
    )
    customer_name = models.ForeignKey(
        CustomerDetailed,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='Customerbill_customer_name',
        verbose_name="Customer Name"
    )
    description_bill = models.CharField(max_length=100, blank=True)
    bill_date = models.DateField(editable=True)
    bill_no = models.CharField(max_length=20, blank=True)
    bill_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    team = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        help_text="Team responsible for this customerbill"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_customerbill',
        help_text="User who created this customerbill record"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project_name} ({self.customer_name})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Customerbill Detail"
        verbose_name_plural = "Customerbill Details"

