# A - Import Required Modules
from django.contrib import admin
from .models import ContractorProfile, Contractor

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

# D - ContractorProfile Admin
@admin.register(ContractorProfile)
class ContractorProfileAdmin(AzureAdminOnlyMixin, admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']
    ordering = ['user__username']

# E - Contractor Admin
@admin.register(Contractor)
class ContractorAdmin(AzureAdminOnlyMixin, admin.ModelAdmin):
    list_display = ['contractor_company', 'name_of_contractor', 'created_by', 'team', 'created_at']
    list_filter = ['team', 'created_by']
    search_fields = ['contractor_company', 'name_of_contractor', 'created_by__username']
    ordering = ['-created_at']

