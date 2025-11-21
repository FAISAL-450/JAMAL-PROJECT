from django.db import models
from django.contrib.auth.models import User

# Role list for chloridetest app
ROLE_CHOICES = [
    ('research-manager', 'Research Manager'),
]

# Profile model to assign roles to users
class ChloridetestProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='chloridetest_profile'
    )
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default='research-manager',
        help_text="Defines the user's role in chloride test operations"
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    class Meta:
        ordering = ['user__username']
        verbose_name = "Chloride Test Role Profile"
        verbose_name_plural = "Chloride Test Role Profiles"


# Main model for storing chloride test readings
class ChlorideTestReading(models.Model):
    time_interval_min = models.IntegerField(
        help_text="Time interval in minutes"
    )
    current_ma = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Measured current in milliamperes (mA)"
    )
    voltage_v = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Applied voltage in volts (V)"
    )
    charge_passed_coulombs = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Total charge passed in coulombs"
    )
    specimen_diameter_in = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        help_text="Specimen diameter in inches"
    )
    chloride_ion_permeability = models.CharField(
        max_length=100,
        help_text="Classification of chloride ion permeability"
    )
    remarks = models.TextField(
        blank=True,
        help_text="Optional remarks or observations"
    )
    team = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        help_text="Team responsible for this chloride test"
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
        related_name='created_chloride_tests',
        help_text="User who created this test record"
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
        related_name='updated_chloride_tests',
        help_text="User who last updated this test record"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the record was last updated"
    )

    def __str__(self):
        return f"{self.time_interval_min} min | {self.chloride_ion_permeability}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Chloride Test Reading"
        verbose_name_plural = "Chloride Test Readings"




