# A - Import Required Modules
from django.contrib import admin
from .models import ChloridetestProfile, ChlorideTest

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

# E - ChlorideTest Admin
@admin.register(ChlorideTest)
class ChlorideTestAdmin(AzureAdminOnlyMixin, admin.ModelAdmin):
    list_display = [
        'time_interval_min',
        'current_ma',
        'created_by',
        'team',
        'created_at'
    ]
    list_filter = ['team', 'created_by']
    search_fields = [
        'time_interval_min',
        'current_ma',
        'created_by__username'
    ]
    ordering = ['-created_at']

