# A - Import Required Modules
from django.contrib import admin
from .models import LeadProfile, Lead

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

# D - LeadProfile Admin
@admin.register(LeadProfile)
class LeadProfileAdmin(AzureAdminOnlyMixin, admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']
    ordering = ['user__username']

# E - Lead Admin
@admin.register(Lead)
class LeadAdmin(AzureAdminOnlyMixin, admin.ModelAdmin):
    list_display = ['customer_name', 'customer_email', 'created_by', 'team', 'created_at']
    list_filter = ['team', 'created_by', 'status', 'source']
    search_fields = ['customer_name', 'customer_email', 'customer_company', 'created_by__username']
    ordering = ['-created_at']

