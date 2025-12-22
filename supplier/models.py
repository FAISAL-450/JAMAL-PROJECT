from django.db import models
from django.contrib.auth.models import User

# Role list for supplier app
ROLE_CHOICES = [
    ('pm', 'PM'),
]

# Profile model to assign roles to users
class SupplierProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='supplier_profile'
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='pm',
        help_text="Defines the user's role in supplier operations"
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        ordering = ['user__username']
        verbose_name = "Supplier Role Profile"
        verbose_name_plural = "Supplier Role Profiles"

# Main model for storing supplier details
class Supplier(models.Model):
    name_of_supplier = models.CharField(
        max_length=100,
        help_text="Name of the supplier"
    )
    supplier_address = models.CharField(
        max_length=100,
        help_text="Supplier address"
    )
    supplier_contact_person = models.CharField(
        max_length=100,
        help_text="Supplier contact person"
    )
    supplier_contact_number = models.CharField(
        max_length=100,
        help_text="Supplier contact number"
    )

    team = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='pm',
        help_text="Team responsible for this supplier"
    )
    allow_team_edit = models.BooleanField(
        default=False,
        help_text="If True, allows the team member who created this record to edit/delete it"
    )
    edit_request_pending = models.BooleanField(
        default=False,
        help_text="If True, indicates the team member has requested edit/delete access"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_suppliers',
        help_text="User who created this supplier"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_suppliers',
        help_text="User who last updated this supplier record"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the record was last updated"
    )

    def __str__(self):
        return self.name_of_supplier

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"

