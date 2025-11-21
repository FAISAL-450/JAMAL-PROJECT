# A - Import Required Modules
from django.contrib import admin
from .models import ChloridetestProfile, ChlorideTestReading

# B - Azure Admin Email
AZURE_ADMIN_EMAIL = 'admin@dzignscapeprofessionals.onmicrosoft.com'

# C - Mixin: Restrict Admin Access to Azure Admin
class AzureAdminOnlyMixin:
    def has_module_permission(self, request):
        return request.user.email == AZURE_ADMIN_EMAIL

    def has_view_permission(self, request, obj=None):
        return request.user.email == AZURE_ADMIN_EMAIL

    def has_change_permission(self, request, obj=None):
        return request.user.email == AZURE_ADMIN_EMAIL

    def has_delete_permission(self, request, obj=None):
        return request.user.email == AZURE_ADMIN_EMAIL

# D - ChloridetestProfile Admin
@admin.register(ChloridetestProfile)
class ChloridetestProfileAdmin(AzureAdminOnlyMixin, admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']
    ordering = ['user__username']

# E - ChlorideTestReading Admin
@admin.register(ChlorideTestReading)
class ChlorideTestReadingAdmin(AzureAdminOnlyMixin, admin.ModelAdmin):
    list_display = [
        'time_interval_min',
        'chloride_ion_permeability',
        'created_by',
        'team',
        'created_at'
    ]
    list_filter = ['team', 'created_by', 'chloride_ion_permeability']
    search_fields = [
        'chloride_ion_permeability',
        'remarks',
        'created_by__username'
    ]
    ordering = ['-created_at']
