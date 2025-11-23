# A - Import Required Modules
from django.contrib import admin
from .models import RequisitionProfile, RequisitionItem

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

# D - RequisitionProfile Admin
@admin.register(RequisitionProfile)
class RequisitionProfileAdmin(AzureAdminOnlyMixin, admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username']
    ordering = ['user__username']

# E - RequisitionItem Admin
@admin.register(RequisitionItem)
class RequisitionItemAdmin(AzureAdminOnlyMixin, admin.ModelAdmin):
    list_display = [
        'PR_no', 'project_name_fpr', 'team',
        'created_by', 'created_at'
    ]
    list_filter = ['team', 'created_by']
    search_fields = ['PR_no', 'project_name_fpr', 'created_by__username']
    ordering = ['-created_at']
