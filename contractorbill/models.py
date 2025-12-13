from django.db import models
from django.contrib.auth.models import User
from project.models import Project

# Role list
ROLE_CHOICES = [
    ('cm', 'CM'),
]

# Work unit choices
WORK_UNIT_CHOICES = [
    ('cft', 'Cft'),
    ('sft', 'Sft'),
]

class ContractorbillProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='contractorbill_profile'
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='cm',
        help_text="Defines the user's role in contractorbill operations"
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        ordering = ['user__username']
        verbose_name = "Contractorbill Role Profile"
        verbose_name_plural = "Contractorbill Role Profiles"


class Contractorbill(models.Model):
    project_name_cb = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contractorbill_project_name_cb',
        verbose_name="Project Name"
    )
    project_address_cb = models.CharField(max_length=200, blank=True)
    contractor_company_name = models.CharField(max_length=100, blank=True)
    name_of_work = models.CharField(max_length=100, blank=True)
    work_unit = models.CharField(
        max_length=20,
        choices=WORK_UNIT_CHOICES,   # ✅ choices added
        help_text="Unit of measurement for the work"
    )
    bill_date = models.DateTimeField(
        verbose_name="Bill Date",
        help_text="Date of the bill",
        blank=True,
        null=True
    )
    bill_no = models.CharField(max_length=20, blank=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    bill_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        editable=False,
        default=0,
        help_text="Auto-calculated as Quantity × Unit Price"
    )
    team = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        help_text="Team responsible for this contractorbill"
    )
    allow_team_edit = models.BooleanField(
        default=False,
        help_text="If True, allows the team member who created this record to edit/delete it"
    )
    edit_request_pending = models.BooleanField(  # ✅ NEW FIELD
        default=False,
        help_text="If True, indicates the team member has requested edit/delete access"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_contractorbill',
        help_text="User who created this contractorbill record"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_contractorbill',
        help_text="User who last updated this contractorbill record"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the record was last updated"
    )

    def save(self, *args, **kwargs):
        # Auto-calculate bill_amount
        if self.quantity and self.unit_price:
            self.bill_amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.project_name_cb} ({self.project_address_cb})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contractorbill Detail"
        verbose_name_plural = "Contractorbill Details"
