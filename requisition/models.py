from django.db import models
from django.contrib.auth.models import User
from project.models import Project

# Role list for requisition app
ROLE_CHOICES = [
    ('pr-manager', 'PR-Manager'),
]

# Profile model to assign roles to users
class RequisitionProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='requisition_profile'
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='pr-manager',
        help_text="Defines the user's role in requisition manage"
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        ordering = ['user__username']
        verbose_name = "Requisition Role Profile"
        verbose_name_plural = "Requisition Role Profiles"

class RequisitionItem(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    project_name_fpr = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='requisition_project_name_fpr',
        verbose_name="Project Name"
    )
    PR_date = models.DateField()
    PR_no = models.CharField(max_length=50)
    name_of_resource = models.CharField(max_length=200)
    resource_unit = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    team = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        help_text="Team responsible for this requisition"
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
        related_name='created_requisitions',
        help_text="User who created this requisition record"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the record was created"
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_requisitions',
        help_text="User who last updated this requisition record"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the record was last updated"
    )

    @property
    def total_amount(self):
        return (self.quantity or 0) * (self.unit_price or 0)

    def __str__(self):
        return f"{self.PR_no} - {self.name_of_resource}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Requisition Detail"
        verbose_name_plural = "Requisition Details"
